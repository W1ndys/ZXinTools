import requests
import base64


def user_pass_base64(username, password):
    username_to_encode = username.encode("utf-8")
    password_to_encode = password.encode("utf-8")
    encoded_data_username = base64.b64encode(username_to_encode)
    encoded_data_password = base64.b64encode(password_to_encode)
    base64_username = encoded_data_username.decode("utf-8")
    base64_password = encoded_data_password.decode("utf-8")
    return base64_username, base64_password


def get_token(username, password):
    try:
        url = "https://v2.api.z-xin.net/auth/login"
        base64_username, base64_password = user_pass_base64(username, password)
        data = {"username": str(base64_username), "password": str(base64_password)}
        response = requests.post(url, data=data).json()
        code = response["code"]
        msg = response["msg"]
        if code == 2000:
            print("[+]登录成功")
            token = response["data"]["token"]
            print("[+]获取token成功")
            print("--------------------------------")
            return token
        else:
            print("[-]登录失败")
            print(f"错误信息: {msg}")
            print("--------------------------------")
            return None
    except requests.exceptions.RequestException as e:
        print(f"[-]请求失败: {e}，请检查网络连接")
        return None
    except KeyError as e:
        print(f"[-]响应中缺少预期的键: {e}，请检查账号密码是否正确")
        return None
