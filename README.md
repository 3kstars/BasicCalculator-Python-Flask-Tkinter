# 薄荷计算器 · 中文版

> 本项目 fork 自 [RayfelO/BasicCalculator-Python-Flask-Tkinter](https://github.com/RayfelO/BasicCalculator-Python-Flask-Tkinter)，上游采用 **MIT License**，允许改造后再分发。
> 本仓库是 GitHub 课程作业成果：Fork → 克隆 → 跑通原版 → 分支改造 → PyInstaller 打包 → 上传到 Releases。

## 一、项目来源

| 项目 | 说明 |
| --- | --- |
| 上游仓库 | https://github.com/RayfelO/BasicCalculator-Python-Flask-Tkinter |
| 许可证 | MIT（见 [LICENSE](LICENSE)） |
| 类型 | Python + Tkinter 桌面计算器（另附 Flask 网页版） |
| 现成构建脚本 | `requirements.txt`、`.github/workflows/ci.yml` |
| 本仓库 | https://github.com/3kstars/BasicCalculator-Python-Flask-Tkinter |

选它的原因：许可宽松、体量小、桌面程序、仓库自带 `requirements.txt` 与 PyInstaller 打包命令，界面文案和配色集中在单文件里，容易改动且容易验证改动是否生效。

## 二、我改了什么

1. **应用名与界面文案中文化**：窗口标题改为「薄荷计算器 · 中文版」，新增中文标题与操作提示标签；按钮 `C` → `清空`、`=` → `计算`，运算符显示为 `×` `÷` `−`，错误提示 `Error` → `输入有误`。
2. **主题色**：`Calculator.COLORS` 由暖棕橙（`#2B2118` / `#F0AD4E`）整体换成薄荷蓝（`#12263A` / `#2DD4BF` / `#38BDF8`），显示屏数字改为薄荷绿 `#5EEAD4`。
3. **兼容性修复（打包必需）**：`calculator_engine.py` 中为兼容 Python 3.8 以下保留的 `ast.Num` 分支，在 Python 3.14 已被移除，会让点击等号直接抛 `AttributeError`。删掉这段旧分支后，已有的 `ast.Constant` 分支即可正常求值。

改动全部在 `feature/my-mod` 分支完成，再通过 PR 合并回 `main`。

## 三、本地运行

环境：Windows 11 / Python 3.14.0（自带 tkinter 8.6）/ Git 2.55。
桌面版只用标准库，无需 pip 安装第三方包；网页版另需 Flask。

```bash
git clone https://github.com/3kstars/BasicCalculator-Python-Flask-Tkinter.git
cd BasicCalculator-Python-Flask-Tkinter
pip install -r requirements.txt      # 网页版 Flask + 打包用 PyInstaller
python TkinterCalculadora.py          # 启动桌面计算器
python app.py                         # 网页版：http://127.0.0.1:5000
python -m unittest test_calculator.py
```

更详细的本机环境记录见 [LOCAL_RUN.md](LOCAL_RUN.md)。

## 四、构建与打包（Windows .exe）

沿用原项目 README 给出的 PyInstaller 方式：单文件、无控制台窗口，并把图标资源一起打进去。

```bash
pyinstaller --noconfirm --onefile --windowed --name MintCalculator \
  --icon static/logo.ico --add-data "static/logo.ico;static" \
  TkinterCalculadora.py
```

产物为 `dist/MintCalculator.exe`（本仓库实际构建时用 `--distpath` 输出到仓库外的交付目录）。双击即可运行，不需要预先安装 Python。

**验证方式**：启动后依次点 `1` `2` `+` `3` `0` `计算`，显示 `42`；点 `清空` 清空显示；输入 `1÷0` 显示「输入有误」。构建产物不进仓库，只作为 Release 附件分发。

## 五、打包遇到的问题与解决

- **`ast.Num` 在 Python 3.14 被移除**：原版点击等号会抛 `AttributeError: module 'ast' has no attribute 'Num'`，窗口能开但算不了。解决：删除旧兼容分支，统一用 `ast.Constant`，并做了 `1+2`、`6*7`、`10/4`、`2**3`、`-5+2` 的回归验证。
- **本机内置 Python 没有 tkinter**：WorkBuddy 内置的 Python 3.13 未编译 `tkinter`，直接运行会 `ModuleNotFoundError`。解决：改用系统 Python 3.14（自带 tkinter 8.6）运行和打包。
- **图标在单文件模式下找不到**：`--onefile` 会把资源解压到临时目录，程序里用 `os.path.dirname(__file__)` 找 `static/logo.ico`。解决：加 `--add-data "static/logo.ico;static"`，让图标随包释放。
- **原仓库误提交构建产物**：`dist/TkinterCalculadora.exe`（约 10 MB）被提交进了仓库，而原 `.gitignore` 没排除 `dist/` 和 `*.exe`。解决：第 3 次提交删除该文件并补齐忽略规则，安装包只走 Releases 和课堂派。

## 六、忽略规则

`.gitignore` 已排除 `dist/`、`build/`、`*.exe`、`*.spec`、`__pycache__/`、`.env` 等。密钥与 `.env` 一律不上传。

## 七、三次提交

| 次序 | 改动内容 | commit message |
| --- | --- | --- |
| 1 | 补充本地运行说明与依赖清单 | `add: 补充本地运行说明` |
| 2 | 应用名、界面中文化、主题色、兼容性修复 | `update: 应用名与界面中文化并更换主题色` |
| 3 | README 构建命令、`.gitignore`、清理误提交的 exe | `fix: 补打包说明与忽略规则` |

## 八、许可证

沿用上游 [MIT License](LICENSE)。
