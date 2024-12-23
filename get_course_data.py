import requests
import json
import os
from get_token import get_token


# 获取已加入的课程数据
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


def save_course_data_to_json(course_data):
    # 检查并创建目录
    os.makedirs("output", exist_ok=True)
    PATH = os.path.join("output", "course_data.json")
    # 把数据直接保存到文件
    with open(PATH, "w", encoding="utf-8") as file:
        json.dump(course_data, file, ensure_ascii=False, indent=4)
    print(f"[+]保存数据成功，数据已保存到 {PATH} 文件中")


def process_course_data(course_data):
    if course_data:
        save_course_data_to_json(course_data)
        if course_data["msg"] == "成功":
            print("[+]数据获取成功")
            print("[+]即将开始解析数据")
            data = ""
            # 解析数据
            for course in course_data["data"]:
                for homework in course["homework"]:
                    data += f"课程名称: {course['course']['name']}\n"
                    data += f"课程老师: {course['teacher']['user']['nickname']}\n"
                    data += f"作业标题: {homework['title']}\n"
                    data += f"作业类型: {homework['category']}\n"
                    data += f"开始时间: {homework['starttime']}\n"
                    data += f"截止时间: {homework['endtime']}\n"
                    if homework["studenthomework"]:
                        data += f"作答次数: {homework['studenthomework'][0]['answerProgress']}\n"
                        data += f"正确次数: {homework['studenthomework'][0]['correctProgress']}\n"
                        data += f"最终得分: {homework['studenthomework'][0]['finalScore']} (若已提交显示0分可能是教师未评分)\n"
                        data += f"最后作答时间: {homework['studenthomework'][0]['lastAnswerTime']}\n"
                    else:
                        data += "暂未作答，无相关数据\n"
                    data += "----------------------------------------------------------------\n"
            # 检查并创建目录
            os.makedirs("output", exist_ok=True)
            PATH = os.path.join("output", "course_data.txt")
            with open(PATH, "w", encoding="utf-8") as file:
                file.write(data)
            print(f"[+]课程数据解析完成，结果已保存到 {PATH} 文件中")
            print("[+]课程数据程序运行结束")
        else:
            print("[-]课程数据获取失败")
    print("--------------------------------")


# 读取用户信息
def read_user_info(token):
    url = "https://v2.api.z-xin.net/auth/user"
    response = requests.get(url, headers={"Authorization": f"Bearer {token}"})
    response = response.json()
    if response.get("code") == 2000:
        print("[+]用户信息获取成功")
        data = response.get("data", {})

        # 提取用户基本信息
        username = data.get("username", "获取失败")
        nickname = data.get("nickname", "获取失败")
        email = data.get("email", "获取失败")
        sex = data.get("sex", "获取失败")
        userType = data.get("userType", "获取失败")

        # 提取学院信息
        college_info = data.get("college", {})
        college_name = college_info.get("name", "获取失败")

        # 提取位置信息
        location_info = data.get("location", {})
        address = location_info.get("addr", "获取失败")
        city = location_info.get("city", "获取失败")
        district = location_info.get("district", "获取失败")
        location_type = location_info.get("location", {}).get("type", "获取失败")
        location_coordinates = location_info.get("location", {}).get(
            "coordinates", "获取失败"
        )

        # 提取宿舍信息
        dormitory_info = data.get("dormitory", {})
        dormitory_bname = dormitory_info.get("bname", "获取失败")

        # 提取学生信息
        student_info = data.get("student", [{}])[0]
        student_joinedClassrooms = student_info.get("joinedClassrooms", "获取失败")
        student_joinedClassrooms_name = student_joinedClassrooms[0].get(
            "name", "获取失败"
        )
        grade = student_info.get("grade", "获取失败")
        # 打印提取的信息
        print(f"[+]用户名: {username}")
        print(f"[+]昵称: {nickname}")
        print(f"[+]邮箱: {email}")
        print(f"[+]性别: {sex}")
        print(f"[+]用户类型: {userType}")
        print(f"[+]学院名称: {college_name}")
        print(f"[+]地址: {address}")
        print(f"[+]城市: {city}")
        print(f"[+]区: {district}")
        print(f"[+]位置类型: {location_type}")
        print(f"[+]位置坐标: {location_coordinates}")
        print(f"[+]宿舍名称: {dormitory_bname}")
        print(f"[+]班级名称: {student_joinedClassrooms_name}")
        print(f"[+]年级: {grade}")
    else:
        print("[-] 获取用户信息失败")
    print("--------------------------------")


def read_config():
    # 从配置文件中读取账号和密码
    with open("config.json", "r", encoding="utf-8") as config_file:
        config = json.load(config_file)
        username = config["username"]
        password = config["password"]
        print("[+]读取账号密码成功")
        print("[+]账号：" + username)
        print("[+]密码：" + password)
        print("--------------------------------")
        return username, password


if __name__ == "__main__":

    print("https://github.com/W1ndys")
    print("--------------------------------")
    username, password = read_config()
    token = get_token(username, password)
    if token:
        read_user_info(token)
        course_data = fetch_course_data(token)
        process_course_data(course_data)
    else:
        print("[-]获取token失败")
