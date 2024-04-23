import tkinter as tk
from tkinter import ttk  # 导入 ttk 模块，因为 Combobox 下拉菜单控件在 ttk 中
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

def xFunc(event, combobox):
    global canvas  # 声明 canvas 为全局变量

    # 删除原有的图形
    canvas.get_tk_widget().destroy()

    # 获取下拉栏中的选择
    flag = combobox.get()

    # 创建新的图形
    fig = mat_plot_demo(flag)

    # 创建新的 FigureCanvasTkAgg 对象
    canvas = FigureCanvasTkAgg(fig, master=root)

    # 将新的 FigureCanvasTkAgg 对象添加到 Tkinter 窗口
    canvas.get_tk_widget().pack()

    # 绘制新的图形
    canvas.draw()

def mat_plot_demo(flag):
    fig, ax = plt.subplots()
    if flag == '深圳':
        ax.plot([1,2,3,5],[4,5,6,9])
    elif flag == '上海':
        ax.plot([1,2,3,4],[4,5,6,7])
    return fig

# 创建一个 Tkinter 窗口
root = tk.Tk()

# 创建一个下拉列表
combobox = ttk.Combobox(root, values=["深圳", "上海"])
combobox.pack()

# 创建一个matplotlib figure
fig, ax = plt.subplots()

# 创建一个 FigureCanvasTkAgg 对象
canvas = FigureCanvasTkAgg(fig, master=root)

# 将 FigureCanvasTkAgg 对象添加到 Tkinter 窗口
canvas.get_tk_widget().pack()

# 当下拉列表中的项目发生更改时调用 xFunc 函数
combobox.bind("<<ComboboxSelected>>", lambda event: xFunc(event, combobox))

# 进入 Tkinter 事件循环
root.mainloop()
