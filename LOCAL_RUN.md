# 本地运行说明

本文件记录 Fork 之后在本地跑通原版的环境与步骤，作为第 1 次提交的改动内容。

## 一、本机环境

| 项目 | 版本 |
| --- | --- |
| 操作系统 | Windows 11 |
| Git | 2.55.0.windows.3 |
| Python（桌面版） | 3.14.0（自带 tkinter 8.6） |
| PyInstaller | 6.22.3 |

本机同时装有 WorkBuddy 内置 Python 3.13（未编译 tkinter 模块），因此桌面程序必须使用系统 Python 3.14 运行，不能直接用默认的 `python` 命令。

## 二、依赖清单

- 桌面计算器 `TkinterCalculadora.py` + `calculator_engine.py`：只用 Python 标准库（`tkinter`、`ast`、`operator`、`functools`、`os`、`sys`），**无需 pip 安装任何第三方包**。
- 网页版 `app.py`：需要 `Flask>=3.0.0`（见 `requirements.txt`），运行 `pip install -r requirements.txt` 后 `python app.py`，浏览器打开 `http://127.0.0.1:5000`。
- 打包工具：`pyinstaller>=6.0.0`（同样写在 `requirements.txt` 中）。

## 三、跑通原版的步骤

```bash
git clone https://github.com/3kstars/BasicCalculator-Python-Flask-Tkinter.git
cd BasicCalculator-Python-Flask-Tkinter
python TkinterCalculadora.py        # 窗口标题：basic-tkinter-calculator
python -m unittest test_calculator.py   # 需先安装 Flask
```

实测结果：窗口可以正常创建并保持运行，图标 `static/logo.ico` 正常加载；这一步没有修改任何代码。

## 四、跑通过程中发现的问题（留待后续提交处理）

在 Python 3.14 上点击等号会抛出异常：

```
AttributeError: module 'ast' has no attribute 'Num'
```

原因：`calculator_engine.py` 为兼容 Python 3.8 以下版本保留了 `ast.Num` 判断，而该别名已在 Python 3.14 被移除。代码里其实已经先用 `ast.Constant` 做了正确判断，只要去掉这段旧的兼容分支即可恢复计算功能。该问题会在功能分支的改造中一并修正，并在打包后用实际计算验证。
