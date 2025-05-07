from zxin_client import ZXinClient
from course_manager import CourseManager
from score_manager import ScoreManager
from log_config import setup_logger

# 创建日志记录器
logger = setup_logger("main")


def print_banner():
    """打印程序banner"""
    logger.info("知新2.0脚本工具 by W1ndys")
    logger.info("https://github.com/W1ndys")
    logger.info("知新2.0 https://stu.z-xin.net/")
    logger.info("--------------------------------")


def main():
    """主函数"""
    try:
        print_banner()

        # 创建客户端并获取token
        client = ZXinClient()
        if not client.login():
            logger.error("程序退出: 获取token失败")
            return

        while True:
            logger.info("\n请选择要执行的操作:")
            logger.info("1. 获取用户信息")
            logger.info("2. 获取课程数据")
            logger.info("3. 获取成绩信息")
            logger.info("0. 退出程序")

            choice = input("请输入选项 [0-3]: \n")
            logger.info("--------------------------------")

            if choice == "1":
                client.get_user_info()
            elif choice == "2":
                course_mgr = CourseManager(client)
                course_mgr.process_course_data()
            elif choice == "3":
                score_mgr = ScoreManager(client)
                score_mgr.process_score_data()
            elif choice == "0":
                logger.info("程序已退出")
                break
            else:
                logger.warning("无效选项，请重新输入")
    except KeyboardInterrupt:
        logger.info("用户主动终止程序")
        logger.info("程序已退出")
    except Exception as e:
        logger.error(f"程序发生错误: {e}")
        logger.error("程序已退出")


if __name__ == "__main__":
    main()
