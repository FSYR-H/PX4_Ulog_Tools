import tkinter as tk
from tkinter import ttk
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib.animation import FuncAnimation
import configparser

# 创建 Tkinter 窗口
root = tk.Tk()
root.geometry("800x600")

# 创建 matplotlib figure
fig1 = Figure(figsize=(5, 4), dpi=100)
fig2 = Figure(figsize=(5, 4), dpi=100)

# 在 Tkinter 窗口中显示 matplotlib figure
canvas1 = FigureCanvasTkAgg(fig1, root)
canvas1.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
canvas2 = FigureCanvasTkAgg(fig2, root)
canvas2.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# 创建下拉栏
combobox1 = ttk.Combobox(root)
combobox1["values"] = ["Figure 1", "Figure 2"]
combobox1.pack()

combobox2 = ttk.Combobox(root)
combobox2["values"] = ["Figure 1", "Figure 2"]
combobox2.pack()

# 创建 configparser 对象
config = configparser.ConfigParser()

# 加载配置
def load_config(combobox1, combobox2):
    # 如果 "Settings" 节不存在，则创建它
    if not config.has_section("Settings"):
        config.add_section("Settings")
        config["Settings"]["combobox1_value"] = "Figure 1"
        config["Settings"]["combobox2_value"] = "Figure 1"

    # 从 config.json 文件中加载配置
    config.read("config.json")

    # 获取下拉栏的值
    combobox1_value = config["Settings"]["combobox1_value"]
    combobox2_value = config["Settings"]["combobox2_value"]

    # 设置下拉栏的值
    combobox1.set(combobox1_value)
    combobox2.set(combobox2_value)

# 保存配置
def save_config(combobox1, combobox2):
    # 设置下拉栏的值
    config["Settings"]["combobox1_value"] = combobox1.get()
    config["Settings"]["combobox2_value"] = combobox2.get()

    # 将配置写入 config.json 文件
    with open("config.json", "w") as f:
        config.write(f)

# 更新 matplotlib figure
def update_figure(i):
    # 获取当前下拉栏的值
    combobox1_value = combobox1.get()
    combobox2_value = combobox2.get()

    # 更新 matplotlib figure
    if combobox1_value == "Figure 1":
        fig1.clear()
        ax1 = fig1.add_subplot(111)
        ax1.plot([1, 2, 3], [4, 5, 6])
    elif combobox1_value == "Figure 2":
        fig1.clear()
        ax1 = fig1.add_subplot(111)
        ax1.plot([7, 8, 9], [10, 11, 12])

    if combobox2_value == "Figure 1":
        fig2.clear()
        ax2 = fig2.add_subplot(111)
        ax2.plot([1, 2, 3], [4, 5, 6])
    elif combobox2_value == "Figure 2":
        fig2.clear()
        ax2 = fig2.add_subplot(111)
        ax2.plot([7, 8, 9], [10, 11, 12])

    # 重绘 figure
    canvas1.draw()
    canvas2.draw()

# 加载配置
load_config(combobox1, combobox2)

# 创建 FuncAnimation 对象
ani = FuncAnimation(fig1, update_figure, interval=50)

# 启动 Tkinter 窗口
root.mainloop()
