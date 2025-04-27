from zxin_client import ZXinClient
from course_manager import CourseManager
import datetime


class HomeworkReminder(ZXinClient):
    def __init__(self, username=None, password=None, config_file=".env"):
        super().__init__(username, password, config_file)
        self.course_manager = CourseManager(username, password, config_file)

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

    def scan_homework(self, days_threshold=3):
        """
        扫描快截止的作业，并发送提醒

        Args:
            days_threshold: 提前多少天提醒，默认3天
        """
        self.logger.info("开始扫描作业")
        course_data = self.fetch_course_data()
        if not course_data:
            self.logger.error("没有可处理的课程数据")
            return

        # 使用无时区的now
        now = datetime.datetime.now(datetime.timezone.utc)
        upcoming_homework = []
        all_homework = []

        # 转换天数阈值为秒数
        seconds_threshold = days_threshold * 86400

        for course in course_data["data"]:
            self.logger.info(f"开始扫描课程：{course['course']['name']}")

            for homework in course["homework"]:
                # 解析截止时间
                end_time_str = homework["endtime"]
                end_time = datetime.datetime.fromisoformat(
                    end_time_str.replace("Z", "+00:00")
                )

                # 计算时间差
                time_delta = end_time - now
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
                    "end_time": end_time_str,
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
                        f"剩余时间：{remaining_time_str}"
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
