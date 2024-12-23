# ZXinTools

- 曲阜师范大学某平台作业截止提醒（未开发）
- 曲阜师范大学某平台作业查看成绩（已开发）

## 联系

有疑问请联系QQ，点击链接加我为QQ好友：https://qm.qq.com/q/unUcwC0eyG

## 使用方法

### 查看成绩

1. 修改 `config.json` 中的账号密码
2. 运行 `get_score.py`
3. 结果会保存到 `socre_info/course_summary.txt` 文件中

## 更新日志

### 2024.11.14

- feat: 使用模块化编程
- feat: 分离 `get_token` 函数
- feat: 添加了从 `config.json` 中读取账号密码的功能
- feat: 添加了 `get_score.py` 文件，用于查看成绩（实际上是获取课程数据的子功能）

### 2024.11.12

- feat: 完成了初步的开发

## 免责声明

本项目为辅助完成作业的脚本，请在使用后 24 小时内删除。仅供学习和交流使用，禁止用于任何商业用途，否则后果自负，作者不承担任何责任。

## 使用截图

![image](https://github.com/user-attachments/assets/7b503fab-9ac3-4c17-8f07-391338c04b5a)


## 开源协议

本项目采用 [MIT 开源协议](LICENSE)，请遵守开源协议

本项目的 token 获取函数来自 [AuroBreeze](https://github.com/AuroBreeze) 的 [Z-xinAnswerAutomatic](https://github.com/AuroBreeze/Z-xinAnswerAutomatic) 项目，感谢开源

## 友情链接

[使用python进行对知新网站的内容获取进行自动答题](https://github.com/AuroBreeze/Z-xinAnswerAutomatic)
