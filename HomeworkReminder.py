from zxin_client import ZXinClient
from course_manager import CourseManager
import datetime
from feishu import feishu


class HomeworkReminder(ZXinClient):
    def __init__(self):
        """
        初始化作业提醒器
        """
        super().__init__()
        # 初始化课程管理器
        self.course_manager = CourseManager(self)
        # 加载已知的作业ID
        self.known_homework_ids = self._load_known_homework_ids()

    def _generate_homework_id(self, homework_item, course_name):
        """
        为作业生成唯一ID。
        优先使用作业数据中的 'id' 字段，如果不存在，则创建一个合成ID。
        """
        if "id" in homework_item and homework_item["id"]:
            return str(homework_item["id"])
        else:
            # 如果没有直接的ID，则根据其他信息创建合成ID
            # 注意：合成ID的稳定性取决于这些字段的不变性
            title = homework_item.get("title", "untitled")
            endtime = homework_item.get("endtime", "no_endtime")
            self.logger.warning(
                f"作业《{title}》(课程：{course_name})缺少 'id' 字段，将使用合成ID。"
            )
            return f"{course_name}_{title}_{endtime}"

    def _load_known_homework_ids(self):
        """从文件中加载已知的作业ID"""
        self.logger.info("开始加载已知作业ID")
        try:
            # 假设 ZXinClient 基类有 load_json 方法
            data = self.load_json("known_homework_ids.json")
            if data and "ids" in data:
                self.logger.info(f"成功加载 {len(data['ids'])} 个已知作业ID")
                return set(data["ids"])
            self.logger.info("未找到已知的作业ID文件或内容为空，将创建新的ID列表")
        except FileNotFoundError:
            self.logger.info("known_homework_ids.json 文件未找到，将创建新的ID列表")
        except Exception as e:
            self.logger.error(f"加载已知作业ID失败: {e}")
        return set()

    def _save_known_homework_ids(self):
        """将当前已知的作业ID保存到文件"""
        self.logger.info(f"开始保存 {len(self.known_homework_ids)} 个作业ID")
        try:
            # 假设 ZXinClient 基类有 save_json 方法
            self.save_json(
                {"ids": list(self.known_homework_ids)}, "known_homework_ids.json"
            )
            self.logger.info("作业ID保存成功")
        except Exception as e:
            self.logger.error(f"保存作业ID失败: {e}")

    def get_homework_data(self):
        """获取作业数据"""
        self.logger.info("开始获取作业数据")
        homework_data = self.api_request("/stu/homework/getHomeworkList")
        self.logger.info("作业数据获取成功")
        return homework_data

    def fetch_course_data(self):
        """获取已加入的课程数据"""
        self.logger.info("开始获取课程数据")
        return self.course_manager.fetch_course_data()

    def format_time_delta(self, delta):
        """
        将时间差格式化为易读的字符串

        Args:
            delta: datetime.timedelta对象

        Returns:
            格式化后的字符串，如"3天5小时30分钟15秒"
        """
        total_seconds = int(delta.total_seconds())

        if total_seconds < 0:
            return "已过期"

        days, remainder = divmod(total_seconds, 86400)
        hours, remainder = divmod(remainder, 3600)
        minutes, seconds = divmod(remainder, 60)

        parts = []
        if days > 0:
            parts.append(f"{days}天")
        if hours > 0:
            parts.append(f"{hours}小时")
        if minutes > 0:
            parts.append(f"{minutes}分钟")
        if seconds > 0 or not parts:  # 如果没有更大的单位，至少显示秒
            parts.append(f"{seconds}秒")

        return "".join(parts)

    def scan_homework(self, days_threshold=5):
        """
        扫描快截止的作业，并发送提醒

        Args:
            days_threshold: 提前多少天提醒，默认5天
        """
        self.logger.info("开始扫描作业")
        course_data = self.fetch_course_data()
        if not course_data:
            self.logger.error("没有可处理的课程数据")
            return

        # 定义北京时区
        beijing_tz = datetime.timezone(datetime.timedelta(hours=8))
        # 获取北京时区的当前时间
        now = datetime.datetime.now(beijing_tz)
        upcoming_homework = []
        all_homework = []
        current_homework_ids = set()  # 用于存储本次扫描到的所有作业ID

        # 转换天数阈值为秒数
        seconds_threshold = days_threshold * 86400

        for course in course_data["data"]:
            self.logger.info(f"开始扫描课程：{course['course']['name']}")

            for homework in course["homework"]:
                # 为作业生成唯一ID (使用原始 unparsed endtime)
                homework_id = self._generate_homework_id(
                    homework, course["course"]["name"]
                )
                current_homework_ids.add(homework_id)

                # 解析截止时间 (来自API，通常是UTC)
                end_time_str_utc = homework["endtime"]
                parsed_end_time_utc = datetime.datetime.fromisoformat(
                    end_time_str_utc.replace("Z", "+00:00")
                )
                # 转换为北京时间
                end_time_beijing = parsed_end_time_utc.astimezone(beijing_tz)

                # 检测是否为新作业
                if homework_id not in self.known_homework_ids:
                    self.logger.info(
                        f"发现新作业：《{homework['title']}》, "
                        f"课程：{course['course']['name']}"
                    )
                    feishu(
                        "发现新作业提醒",
                        f"作业：《{homework['title']}》\n"
                        f"课程：{course['course']['name']}\n"
                        f"教师：{course['teacher']['user']['nickname']}\n"
                        f"截止时间：{end_time_beijing.strftime('%Y-%m-%d %H:%M:%S')} (北京时间)",
                    )

                # 计算时间差 (基于北京时间)
                time_delta = end_time_beijing - now
                days_remaining = time_delta.days
                seconds_remaining = time_delta.total_seconds()

                # 格式化剩余时间
                remaining_time_str = self.format_time_delta(time_delta)

                # 检查是否已提交
                is_submitted = False
                if homework["studenthomework"]:
                    is_submitted = True

                # 创建作业信息对象
                homework_info = {
                    "course_name": course["course"]["name"],
                    "teacher": course["teacher"]["user"]["nickname"],
                    "title": homework["title"],
                    "category": homework["category"],
                    "end_time_utc": end_time_str_utc,  # 保留原始UTC时间字符串
                    "end_time_beijing": end_time_beijing.isoformat(),  # 存储北京时间ISO格式字符串
                    "days_remaining": days_remaining,
                    "seconds_remaining": seconds_remaining,
                    "remaining_time": remaining_time_str,
                    "is_submitted": is_submitted,
                }

                # 添加到所有作业列表
                all_homework.append(homework_info)

                # 如果快截止且未提交
                if (
                    seconds_remaining <= seconds_threshold
                    and seconds_remaining >= 0
                    and not is_submitted
                ):
                    upcoming_homework.append(homework_info)
                    self.logger.warning(
                        f"发现即将截止作业：《{homework['title']}》, "
                        f"课程：{course['course']['name']}, "
                        f"剩余时间：{remaining_time_str}, "
                        f"截止时间：{end_time_beijing.strftime('%Y-%m-%d %H:%M:%S')} (北京时间)"
                    )
                    # 发送飞书消息
                    feishu(
                        "发现即将截止作业",
                        f"作业：《{homework['title']}》, "
                        f"课程：{course['course']['name']}, "
                        f"剩余时间：{remaining_time_str}, "
                        f"截止时间：{end_time_beijing.strftime('%Y-%m-%d %H:%M:%S')} (北京时间)",
                    )
                else:
                    # 显示所有作业的状态
                    status = ""
                    if seconds_remaining < 0:
                        status = "已过期"
                    elif is_submitted:
                        status = "已提交"
                    else:
                        status = f"剩余时间：{remaining_time_str}"

                    self.logger.info(
                        f"作业：《{homework['title']}》, "
                        f"课程：{course['course']['name']}, "
                        f"状态：{status}"
                    )

        # 保存所有作业数据
        self.save_json({"all_homework": all_homework}, "all_homework.json")

        # 更新并保存已知的作业ID
        self.known_homework_ids = current_homework_ids
        self._save_known_homework_ids()

        # 保存即将截止的作业数据
        if upcoming_homework:
            self.save_json(
                {"upcoming_homework": upcoming_homework}, "upcoming_homework.json"
            )
            self.logger.info(f"发现 {len(upcoming_homework)} 个即将截止的作业")
            return upcoming_homework
        else:
            self.logger.info("没有即将截止的作业")
            return []


if __name__ == "__main__":
    reminder = HomeworkReminder()
    reminder.scan_homework()
