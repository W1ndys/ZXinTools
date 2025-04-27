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

    def scan_homework(self, days_threshold=3):
        """
        扫描快截止的作业，并发送提醒

        Args:
            days_threshold: 提前多少天提醒，默认7天
        """
        self.logger.info("开始扫描作业")
        course_data = self.fetch_course_data()
        if not course_data:
            self.logger.error("没有可处理的课程数据")
            return

        # 使用无时区的now
        now = datetime.datetime.now(datetime.timezone.utc)
        upcoming_homework = []

        for course in course_data["data"]:
            self.logger.info(f"开始扫描课程：{course['course']['name']}")

            for homework in course["homework"]:
                # 解析截止时间
                end_time_str = homework["endtime"]
                end_time = datetime.datetime.fromisoformat(
                    end_time_str.replace("Z", "+00:00")
                )

                # 计算距离截止还有多少天
                days_remaining = (end_time - now).days

                # 检查是否已提交
                is_submitted = False
                if homework["studenthomework"]:
                    is_submitted = True

                # 如果快截止且未提交
                if (
                    days_remaining <= days_threshold
                    and days_remaining >= 0
                    and not is_submitted
                ):
                    homework_info = {
                        "course_name": course["course"]["name"],
                        "teacher": course["teacher"]["user"]["nickname"],
                        "title": homework["title"],
                        "category": homework["category"],
                        "end_time": end_time_str,
                        "days_remaining": days_remaining,
                    }
                    upcoming_homework.append(homework_info)
                    self.logger.warning(
                        f"发现即将截止作业：《{homework['title']}》, "
                        f"课程：{course['course']['name']}, "
                        f"剩余天数：{days_remaining}"
                    )
                    
                else:
                    # 显示所有作业的状态
                    status = ""
                    if days_remaining < 0:
                        status = "已过期"
                    elif is_submitted:
                        status = "已提交"
                    else:
                        status = f"剩余{days_remaining}天"

                    self.logger.info(
                        f"作业：《{homework['title']}》, "
                        f"课程：{course['course']['name']}, "
                        f"状态：{status}"
                    )

        # 保存即将截止的作业数据
        if upcoming_homework:
            self.save_json(
                {"upcoming_homework": upcoming_homework}, "upcoming_homework.json"
            )
            return upcoming_homework
        else:
            self.logger.info("没有即将截止的作业")
            return []


if __name__ == "__main__":
    reminder = HomeworkReminder()
    reminder.scan_homework()
