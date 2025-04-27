import logging
import os
import colorlog
from datetime import datetime

# 创建logs文件夹
logs_dir = "logs"
os.makedirs(logs_dir, exist_ok=True)

# 获取当前日期作为日志文件名的一部分
current_date = datetime.now().strftime("%Y-%m-%d")
log_file = os.path.join(logs_dir, f"zxin_tools_{current_date}.log")

# 日志颜色配置
log_colors = {
    "DEBUG": "cyan",
    "INFO": "green",
    "WARNING": "yellow",
    "ERROR": "red",
    "CRITICAL": "red,bg_white",
}

# 创建格式器
file_formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
console_formatter = colorlog.ColoredFormatter(
    "%(log_color)s%(levelname)s: %(message)s", log_colors=log_colors
)

# 创建日志处理器
file_handler = logging.FileHandler(log_file, encoding="utf-8")
file_handler.setFormatter(file_formatter)

console_handler = colorlog.StreamHandler()
console_handler.setFormatter(console_formatter)


# 配置根日志器
def setup_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    return logger
