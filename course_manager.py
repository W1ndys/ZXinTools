from zxin_client import ZXinClient
from log_config import setup_logger


class CourseManager:
    """知新2.0课程管理类，处理课程数据相关功能"""

    def __init__(self, client: ZXinClient):
        """初始化课程管理器"""
        self.client = client
        self.logger = setup_logger(self.__class__.__name__)

    def fetch_course_data(self):
        """获取已加入的课程数据"""
        self.logger.info("开始获取课程数据")
        course_data = self.client.api_request("/stu/course/getJoinedCourse2")

        if course_data and course_data.get("msg") == "成功":
            self.logger.info("课程数据获取成功")
            return course_data
        else:
            self.logger.error("课程数据获取失败")
            return None

    def process_course_data(self, course_data=None):
        """处理课程数据并保存结果"""
        if not course_data:
            course_data = self.fetch_course_data()

        if not course_data:
            self.logger.error("没有可处理的课程数据")
            return False

        self.client.save_json(course_data, "course_data.json")

        if course_data["msg"] == "成功":
            self.logger.info("即将开始解析课程数据")

            formatted_data = self._format_course_data(course_data)

            self.client.save_text(formatted_data, "course_data.txt")

            self.logger.info("课程数据解析完成")
            self.logger.info("课程数据程序运行结束")
            self.logger.info("--------------------------------")
            return True
        else:
            self.logger.error("课程数据获取失败")
            return False

    def _format_course_data(self, course_data):
        """将课程数据格式化为文本格式"""
        formatted_text = ""

        for course in course_data["data"]:
            for homework in course["homework"]:
                formatted_text += f"课程名称: {course['course']['name']}\n"
                formatted_text += f"课程老师: {course['teacher']['user']['nickname']}\n"
                formatted_text += f"作业标题: {homework['title']}\n"
                formatted_text += f"作业类型: {homework['category']}\n"
                formatted_text += f"开始时间: {homework['starttime']}\n"
                formatted_text += f"截止时间: {homework['endtime']}\n"

                if homework["studenthomework"]:
                    student_hw = homework["studenthomework"][0]
                    formatted_text += f"作答次数: {student_hw['answerProgress']}\n"
                    formatted_text += f"正确次数: {student_hw['correctProgress']}\n"
                    formatted_text += f"最终得分: {student_hw['finalScore']} (若已提交显示0分可能是教师未评分)\n"
                    formatted_text += f"最后作答时间: {student_hw['lastAnswerTime']}\n"
                else:
                    formatted_text += "暂未作答，无相关数据\n"

                formatted_text += (
                    "----------------------------------------------------------------\n"
                )

        return formatted_text
