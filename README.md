# ZXinTools - 知新 2.0 脚本工具集

这是一个用于获取知新 2.0 数据的工具集，采用面向对象的方式进行了重构，使代码更加模块化、系统化和易于维护。

## 特性

- 获取用户个人信息
- 获取课程数据和作业详情
- 获取成绩信息
- 交互式菜单操作
- 数据导出为 JSON 和 TXT 格式
- [新作业、作业截止提醒功能](https://github.com/W1ndys/ZXinTools/blob/main/HomeworkReminder.py)

## 项目结构

- `zxin_client.py` - 基础客户端类，处理认证和基本 API 请求
- `course_manager.py` - 课程管理类，处理课程数据相关功能
- `score_manager.py` - 成绩管理类，处理成绩数据相关功能
- `main.py` - 主程序，提供交互式菜单

## 使用方法

1. 创建`.env`文件，包含以下内容：

```
ZXIN_USERNAME=你的账号
ZXIN_PASSWORD=你的密码
FEISHU_BOT_URL=飞书机器人 webhook 地址
FEISHU_BOT_SECRET=飞书机器人 secret
```

2. 运行主程序：

```bash
python main.py
```

3. 从交互式菜单中选择需要的功能：
   - 1: 获取用户信息
   - 2: 获取课程数据
   - 3: 获取成绩信息
   - 0: 退出程序

### 作业提醒功能

```bash
python HomeworkReminder.py
```

## 数据输出

所有输出文件将保存在`output`目录下：

- `course_data.json` - 原始课程数据（JSON 格式）
- `course_data.txt` - 格式化课程数据（文本格式）
- `score_data.json` - 原始成绩数据（JSON 格式）
- `score_info.txt` - 格式化成绩数据（文本格式）

## 开发说明

### 类层次结构

- `ZXinClient` - 基础客户端类
  - `CourseManager` - 课程管理类（继承自`ZXinClient`）
  - `ScoreManager` - 成绩管理类（继承自`ZXinClient`）
  - `HomeworkManager` - 作业管理类（继承自`ZXinClient`）

### 扩展

如需添加新功能，可以：

1. 创建新的管理类，继承自`ZXinClient`
2. 在`main.py`中添加对应的菜单选项和处理逻辑

## 联系

有疑问请联系 QQ，点击链接加我为 QQ 好友：https://qm.qq.com/q/unUcwC0eyG

## 免责声明

本项目为辅助脚本，只读不写，仅可用于成绩查看作业查看，所有内容都可以通过浏览器手动获取，无越权获取数据等行为，请在下载后 24 小时内删除。仅供学习和交流使用，禁止用于任何商业用途，否则后果自负，作者不承担任何责任。

## 使用截图

<div align="center">
  <div style="display: flex; justify-content: space-between; margin-bottom: 20px;">
    <img src="https://github.com/user-attachments/assets/7b503fab-9ac3-4c17-8f07-391338c04b5a"   width="30%" />
    <img src="https://github.com/user-attachments/assets/b63768d8-1cbc-4637-9fbe-977495ca3a7b"   width="30%" />
    <img src="https://github.com/user-attachments/assets/565f2f32-f73a-4cf1-aa8d-a4493df04709"   width="30%" />
  </div>
</div>

## 开源协议

本项目采用 [MIT 开源协议](LICENSE)，请遵守开源协议

本项目的 token 获取函数来自 [AuroBreeze](https://github.com/AuroBreeze) 的 [Z-xinAnswerAutomatic](https://github.com/AuroBreeze/Z-xinAnswerAutomatic) 项目，感谢开源
