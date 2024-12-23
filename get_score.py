import requests
import json
from get_token import get_token  # 导入get_token函数
import os


def fetch_course_data(token):
    try:
        api_url = "https://v2.api.z-xin.net/stu/course/getJoinedCourse2"
        headers = {
            "Authorization": f"Bearer {token}",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        }
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()  # 检查请求是否成功
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}")
        return None


def process_course_scores(course_data):  # 修改函数名
    if course_data:
        # 把数据直接保存到文件
        with open("course_data.json", "w", encoding="utf-8") as file:
            json.dump(course_data, file, ensure_ascii=False, indent=4)
        print("[+]读取成绩数据成功，数据已保存到 course_data.json 文件中")

        if course_data["msg"] == "成功":
            print("[+]成绩数据获取成功")
            print("[+]即将开始解析成绩数据")
            data = ""
            # 解析数据
            for course in course_data["data"]:
                for homework in course["homework"]:
                    data += f"课程名称: {course['course']['name']}\n"
                    data += f"作业标题: {homework['title']}\n"
                    data += f"课程老师: {course['teacher']['user']['nickname']}\n"
                    if homework["studenthomework"]:
                        data += f"最终得分: {homework['studenthomework'][0]['finalScore']}（若已提交显示0分可能是教师未评分）\n"
                    else:
                        data += "暂未作答，无相关成绩数据\n"
                    data += "----------------------------------------------------------------\n"

            # 检查并创建目录
            os.makedirs("output", exist_ok=True)
            # 修改生成文件名，保存在子目录下
            PATH = os.path.join("output", "score_info.txt")
            with open(PATH, "w", encoding="utf-8") as file:  # 修改文件名
                file.write(data)
            print(f"[+]成绩数据解析完成，结果已保存到 {PATH} 文件中")
            print("[+]成绩数据程序运行结束")
            print("--------------------------------")
            print("Power by W1ndys")
            print("https://github.com/W1ndys")
        else:
            print("[-]成绩数据获取失败")


def read_config():
    # 从配置文件中读取账号和密码
    with open("config.json", "r", encoding="utf-8") as config_file:
        config = json.load(config_file)
        username = config["username"]
        password = config["password"]
        print("--------------------------------")
        print("[+]读取账号密码成功")
        print("[+]账号：" + username)
        print("[+]密码：" + password)
        return username, password


if __name__ == "__main__":
    username, password = read_config()
    token = get_token(username, password)
    if token:
        course_data = fetch_course_data(token)
        process_course_scores(course_data)  # 调用修改后的函数名
    else:
        print("[-]获取token失败")
