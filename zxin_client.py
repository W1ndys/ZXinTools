import requests
import base64
import json
import os
from log_config import setup_logger


class ZXinClient:
    """知新2.0客户端基类，处理认证和基本API请求"""

    BASE_URL = "https://v2.api.z-xin.net"

    def __init__(self, username=None, password=None, config_file=".env"):
        """初始化客户端，可以直接提供用户名密码或从配置文件读取"""
        self.logger = setup_logger(self.__class__.__name__)
        self.session = requests.Session()  # 初始化 session
        if username and password:
            self.username = username
            self.password = password
        else:
            self.username, self.password = self._read_config(config_file)
        self.token = None
        self.output_dir = "output"
        # 确保输出目录存在
        os.makedirs(self.output_dir, exist_ok=True)

    def _read_config(self, config_file):
        """从配置文件中读取账号和密码"""
        try:
            with open(config_file, "r", encoding="utf-8") as file:
                config = file.read().split("\n")
                username = config[0].split("=")[1]
                password = config[1].split("=")[1]
                self.logger.info("读取账号密码成功")
                self.logger.info("--------------------------------")
                return username, password
        except Exception as e:
            self.logger.error(f"读取配置文件失败: {e}")
            raise

    def _user_pass_base64(self, username, password):
        """将用户名和密码转换为base64编码"""
        username_encoded = base64.b64encode(username.encode("utf-8")).decode("utf-8")
        password_encoded = base64.b64encode(password.encode("utf-8")).decode("utf-8")
        return username_encoded, password_encoded

    def login(self):
        """登录并获取token"""
        try:
            url = f"{self.BASE_URL}/auth/login"
            base64_username, base64_password = self._user_pass_base64(
                self.username, self.password
            )
            data = {"username": base64_username, "password": base64_password}
            response = self.session.post(url, data=data).json()
            code = response["code"]
            msg = response["msg"]

            if code == 2000:
                self.logger.info("登录成功")
                self.token = response["data"]["token"]
                self.logger.info("获取token成功")
                self.logger.info("--------------------------------")
                return self.token
            else:
                self.logger.error("登录失败")
                self.logger.error(f"错误信息: {msg}")
                self.logger.info("--------------------------------")
                return None
        except requests.exceptions.RequestException as e:
            self.logger.error(f"请求失败: {e}，请检查网络连接")
            return None
        except KeyError as e:
            self.logger.error(f"响应中缺少预期的键: {e}，请检查账号密码是否正确")
            return None

    def get_headers(self):
        """获取带有认证信息的请求头"""
        if not self.token:
            self.login()

        return {
            "Authorization": f"Bearer {self.token}",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        }

    def api_request(self, endpoint, method="GET", data=None):
        """发送API请求并处理响应"""
        try:
            url = f"{self.BASE_URL}{endpoint}"
            headers = self.get_headers()

            if method.upper() == "GET":
                response = self.session.get(url, headers=headers)
            elif method.upper() == "POST":
                response = self.session.post(
                    url, headers=headers, json=data if data else {}
                )
            else:
                raise ValueError(f"不支持的请求方法: {method}")

            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            self.logger.error(f"API请求失败: {e}")
            return None

    def get_user_info(self):
        """获取用户信息"""
        response = self.api_request("/auth/user")

        if response and response.get("code") == 2000:
            self.logger.info("用户信息获取成功")
            data = response.get("data", {})

            # 提取用户基本信息
            user_info = {
                "username": data.get("username", "获取失败"),
                "nickname": data.get("nickname", "获取失败"),
                "email": data.get("email", "获取失败"),
                "sex": data.get("sex", "获取失败"),
                "userType": data.get("userType", "获取失败"),
                "college": data.get("college", {}).get("name", "获取失败"),
            }

            # 提取位置信息
            location_info = data.get("location", {})
            user_info.update(
                {
                    "address": location_info.get("addr", "获取失败"),
                    "city": location_info.get("city", "获取失败"),
                    "district": location_info.get("district", "获取失败"),
                }
            )

            # 提取宿舍和学生信息
            user_info["dormitory"] = data.get("dormitory", {}).get("bname", "获取失败")

            student_info = data.get("student", [{}])[0]
            classrooms = student_info.get("joinedClassrooms", [{}])
            user_info.update(
                {
                    "classroom": (
                        classrooms[0].get("name", "获取失败")
                        if classrooms
                        else "获取失败"
                    ),
                    "grade": student_info.get("grade", "获取失败"),
                }
            )

            # 打印用户信息
            for key, value in user_info.items():
                self.logger.info(f"{key}: {value}")

            self.logger.info("--------------------------------")
            return user_info
        else:
            self.logger.error("获取用户信息失败")
            self.logger.info("--------------------------------")
            return None

    def save_json(self, data, filename):
        """保存数据为JSON文件"""
        filepath = os.path.join(self.output_dir, filename)
        with open(filepath, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        self.logger.info(f"保存数据成功，数据已保存到 {filepath} 文件中")
        return filepath

    def save_text(self, text, filename):
        """保存文本到文件"""
        filepath = os.path.join(self.output_dir, filename)
        with open(filepath, "w", encoding="utf-8") as file:
            file.write(text)
        self.logger.info(f"保存文本成功，已保存到 {filepath} 文件中")
        return filepath
