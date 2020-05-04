# My12306
![](https://img.shields.io/badge/license-MIT-blue.svg)
![](https://img.shields.io/badge/language-python3.7-green.svg)
![](https://img.shields.io/badge/encoding-utf--8-yellow.svg)
## Preview
![](img/example.png)
## Description
本项目为人工智能程序设计第8周实验课作业，采用 [tkinter](https://docs.python.org/3/library/tkinter.html) 标准图形库，支持在 Windows 下的高 dpi 下自适应。
![](img/theme.jpg)

## Prerequisites
无第三方库，包含 `tkinter 8.6+` 的 `python3` 均可。

直接运行`main.py`。

## Notice
- `sample/` 中包含一些可以用于测试的数据。这里感谢[StellarDragon](https://github.com/StellarDragon)提供的 12306 官网的高铁数据。
- 从文件导入信息时不检查数据合法性，因此不符合规范的数据可能会导致意料之外的错误发生。
- 所有信息以 `json` 格式保存在`data/`中，但从文件载入车次信息的格式依然为作业所提供的字符串格式。
