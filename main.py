from zxin_client import ZXinClient
from course_manager import CourseManager
from score_manager import ScoreManager


def print_banner():
    """打印程序banner"""
    print("智新教学平台工具集")
    print("https://github.com/W1ndys")
    print("--------------------------------")


def main():
    """主函数"""
    print_banner()

    # 创建客户端并获取token
    client = ZXinClient()
    if not client.login():
        print("[-]程序退出: 获取token失败")
        return

    while True:
        print("\n请选择要执行的操作:")
        print("1. 获取用户信息")
        print("2. 获取课程数据")
        print("3. 获取成绩信息")
        print("0. 退出程序")

        choice = input("请输入选项 [0-3]: ")
        print("--------------------------------")

        if choice == "1":
            client.get_user_info()
        elif choice == "2":
            course_mgr = CourseManager(client.username, client.password)
            course_mgr.token = client.token  # 共享token避免重复登录
            course_mgr.process_course_data()
        elif choice == "3":
            score_mgr = ScoreManager(client.username, client.password)
            score_mgr.token = client.token  # 共享token避免重复登录
            score_mgr.process_score_data()
        elif choice == "0":
            print("[+]程序已退出")
            break
        else:
            print("[-]无效选项，请重新输入")


if __name__ == "__main__":
    main()
