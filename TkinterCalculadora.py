import os
import sys
import tkinter as tk
from functools import partial

from calculator_engine import safe_eval


class Calculator:
    """轻量桌面计算器。

    本项目 fork 自 RayfelO/BasicCalculator-Python-Flask-Tkinter（MIT）。
    本分支的改造：应用名与界面文案中文化、主题色由暖棕橙改为薄荷蓝、
    运算符改用中文习惯的 x / ÷ 显示，并在窗口中加入中文提示标签。
    """

    APP_NAME = "薄荷计算器 · 中文版"

    COLORS = {
        "bg": "#12263A",
        "card": "#F2F7FA",
        "title_text": "#1E3A5F",
        "hint_text": "#5B7A99",
        "display_bg": "#0B1B2B",
        "display_text": "#5EEAD4",
        "num_bg": "#FFFFFF",
        "num_text": "#1E3A5F",
        "operator_bg": "#2DD4BF",
        "operator_text": "#0B1B2B",
        "clear_bg": "#FB7185",
        "clear_text": "#FFFFFF",
        "equals_bg": "#38BDF8",
        "equals_text": "#0B1B2B",
    }

    def __init__(self, root):
        self.root = root
        self.root.title(self.APP_NAME)
        self.root.geometry("420x680")
        self.root.configure(bg=self.COLORS["bg"])
        self.root.resizable(False, False)

        if sys.platform.startswith("win"):
            icon_path = os.path.join(os.path.dirname(__file__), "static", "logo.ico")
            if os.path.exists(icon_path):
                self.root.iconbitmap(icon_path)

        self.result_var = tk.StringVar()
        self.create_widgets()

    def create_widgets(self):
        card = tk.Frame(self.root, bg=self.COLORS["card"], bd=0)
        card.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

        tk.Label(
            card,
            text="薄荷计算器",
            font=("Microsoft YaHei", 17, "bold"),
            bg=self.COLORS["card"],
            fg=self.COLORS["title_text"],
        ).pack(pady=(10, 0))

        tk.Label(
            card,
            text="输入算式后点「计算」，支持 + − × ÷",
            font=("Microsoft YaHei", 9),
            bg=self.COLORS["card"],
            fg=self.COLORS["hint_text"],
        ).pack(pady=(2, 8))

        display = tk.Entry(
            card,
            textvariable=self.result_var,
            font=("Segoe UI", 32),
            bg=self.COLORS["display_bg"],
            fg=self.COLORS["display_text"],
            justify="right",
            relief="flat",
            bd=0,
            highlightthickness=0,
            insertbackground=self.COLORS["display_text"],
        )
        display.pack(fill=tk.X, padx=12, pady=(0, 10), ipady=18)

        grid = tk.Frame(card, bg=self.COLORS["card"])
        grid.pack(fill=tk.BOTH, expand=True, padx=12, pady=(0, 12))

        for i in range(4):
            grid.columnconfigure(i, weight=1, uniform="col")
        for i in range(4):
            grid.rowconfigure(i, weight=1, uniform="row")

        # (按钮显示文字, 参与计算的字符, 按钮类型)
        buttons = [
            ("7", "7", "num"),
            ("8", "8", "num"),
            ("9", "9", "num"),
            ("÷", "/", "operator"),
            ("4", "4", "num"),
            ("5", "5", "num"),
            ("6", "6", "num"),
            ("×", "*", "operator"),
            ("1", "1", "num"),
            ("2", "2", "num"),
            ("3", "3", "num"),
            ("−", "-", "operator"),
            ("0", "0", "num"),
            ("清空", "clear", "clear"),
            ("计算", "equals", "equals"),
            ("+", "+", "operator"),
        ]

        row_val = 0
        col_val = 0

        for label, value, kind in buttons:
            self.create_button(grid, label, value, kind, row_val, col_val)
            col_val += 1
            if col_val > 3:
                col_val = 0
                row_val += 1

    def create_button(self, parent, label, value, kind, row, col):
        if kind == "equals":
            cmd = self.calculate_result
        elif kind == "clear":
            cmd = self.clear_result
        else:
            cmd = partial(self.append_value, value)

        bg = self.COLORS.get(f"{kind}_bg", self.COLORS["num_bg"])
        fg = self.COLORS.get(f"{kind}_text", self.COLORS["num_text"])

        font = (
            ("Microsoft YaHei", 13, "bold")
            if len(label) > 1
            else ("Segoe UI", 20, "bold")
        )

        btn = tk.Button(
            parent,
            text=label,
            font=font,
            bg=bg,
            fg=fg,
            activebackground=fg,
            activeforeground=bg,
            relief="flat",
            bd=0,
            cursor="hand2",
            command=cmd,
        )
        btn.grid(row=row, column=col, sticky="nsew", padx=5, pady=5)

    def append_value(self, value):
        current_text = self.result_var.get()
        self.result_var.set(current_text + value)

    def clear_result(self):
        self.result_var.set("")

    def calculate_result(self):
        try:
            result = safe_eval(self.result_var.get())
            self.result_var.set(result)
        except Exception:
            self.result_var.set("输入有误")


if __name__ == "__main__":
    root = tk.Tk()
    calc = Calculator(root)
    root.mainloop()
