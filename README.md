# My12306
![](https://img.shields.io/badge/license-MIT-blue.svg)
![](https://img.shields.io/badge/language-python3.7-green.svg)
![](https://img.shields.io/badge/encoding-utf--8-yellow.svg)
## Description
本项目为人工智能程序设计第8周实验课作业，采用 [tkinter](https://docs.python.org/3/library/tkinter.html) 标准图形库，支持高 dpi 缩放。
![](img/theme.jpg)

## Notice
- 从文件导入信息时不检查数据合法性，因此不符合规范的数据可能会导致意料之外的错误发生。
- 任务要求中关于保存与导出信息相关描述不明确，故只支持从文件载入车次信息，不支持将信息导出到任意文件。
- 所有信息以 `json` 格式保存在`data/`中，但从文件载入车次信息的格式依然为作业所提供的字符串格式。

## Usage

## To Do
- [ ] 对 0 特判
- [ ] 改用`tkinter.ttk`
- [ ] 购票界面改为下拉式菜单设计