from zxin_client import ZXinClient


class ScoreManager(ZXinClient):
    """知新2.0成绩管理类，处理成绩数据相关功能"""

    def __init__(self, username=None, password=None, config_file=".env"):
        """初始化成绩管理器"""
        super().__init__(username, password, config_file)

    def fetch_score_data(self):
        """获取成绩数据（使用与课程数据相同的API）"""
        self.logger.info("开始获取成绩数据")
        score_data = self.api_request("/stu/course/getJoinedCourse2")

        if score_data and score_data.get("msg") == "成功":
            self.logger.info("成绩数据获取成功")
            return score_data
        else:
            self.logger.error("成绩数据获取失败")
            return None

    def process_score_data(self, score_data=None):
        """处理成绩数据并保存结果"""
        if not score_data:
            score_data = self.fetch_score_data()

        if not score_data:
            self.logger.error("没有可处理的成绩数据")
            return False

        # 保存原始JSON数据
        self.save_json(score_data, "score_data.json")

        if score_data["msg"] == "成功":
            self.logger.info("即将开始解析成绩数据")

            # 格式化成绩数据
            formatted_data = self._format_score_data(score_data)

            # 保存格式化的文本数据
            self.save_text(formatted_data, "score_info.txt")

            self.logger.info("成绩数据解析完成")
            self.logger.info("成绩数据程序运行结束")
            self.logger.info("--------------------------------")
            self.logger.info("Power by W1ndys")
            self.logger.info("https://github.com/W1ndys")
            return True
        else:
            self.logger.error("成绩数据获取失败")
            return False

    def _format_score_data(self, score_data):
        """将成绩数据格式化为文本格式"""
        formatted_text = ""

        for course in score_data["data"]:
            for homework in course["homework"]:
                formatted_text += f"课程名称: {course['course']['name']}\n"
                formatted_text += f"作业标题: {homework['title']}\n"
                formatted_text += f"课程老师: {course['teacher']['user']['nickname']}\n"

                if homework["studenthomework"]:
                    formatted_text += f"最终得分: {homework['studenthomework'][0]['finalScore']}（若已提交显示0分可能是教师未评分）\n"
                else:
                    formatted_text += "暂未作答，无相关成绩数据\n"

                formatted_text += (
                    "----------------------------------------------------------------\n"
                )

        return formatted_text
