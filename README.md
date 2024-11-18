# ZXinTools

- 曲阜师范大学某平台作业截止提醒（未开发）
- 曲阜师范大学某平台作业查看成绩（已开发）
- 曲阜师范大学某平台作业客观题爆破答案（已开发，见 [ZXinAutoAnswer](https://github.com/W1ndys/ZXinAutoAnswer)）

## 使用方法

### 查看成绩

1. 修改 `config.json` 中的账号密码
2. 运行 `get_score.py`
3. 结果会保存到 `socre_info/course_summary.txt` 文件中

## 更新日志

### 2024.11.18

- feat: 开发了客观题爆破答案功能（见 [ZXinAutoAnswer](https://github.com/W1ndys/ZXinAutoAnswer)），暂不开源

### 2024.11.14

- feat: 使用模块化编程
- feat: 分离 `get_token` 函数
- feat: 添加了从 `config.json` 中读取账号密码的功能
- feat: 添加了 `get_score.py` 文件，用于查看成绩（实际上是获取课程数据的子功能）

### 2024.11.12

- feat: 完成了初步的开发

## 开源协议

本项目采用 [MIT 开源协议](LICENSE)，请遵守开源协议

本项目的 token 获取函数来自 [AuroBreeze](https://github.com/AuroBreeze) 的 [Z-xinAnswerAutomatic](https://github.com/AuroBreeze/Z-xinAnswerAutomatic) 项目，感谢开源
