import tkinter
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import mplcursors

root = tkinter.Tk()  # 创建tkinter的主窗口
root.title("在tkinter中使用matplotlib")

f = Figure(figsize=(5, 4), dpi=100)
a = f.add_subplot(111)  # 添加子图:1行1列第1个

# 生成用于绘sin图的数据
x = np.arange(0, 3, 0.01)
y = np.sin(2 * np.pi * x)

# 在前面得到的子图上绘图
a.plot(x, y)

# 将绘制的图形显示到tkinter:创建属于root的canvas画布,并将图f置于画布上
canvas = FigureCanvasTkAgg(f, master=root)
canvas.draw()  # 注意show方法已经过时了,这里改用draw
canvas.get_tk_widget().pack(side=tkinter.TOP,  # 上对齐
                            fill=tkinter.BOTH,  # 填充方式
                            expand=tkinter.YES)  # 随窗口大小调整而调整

mplcursors.cursor(canvas.figure.axes[0], hover=True)  # 将mplcursors添加到图形上

# matplotlib的导航工具栏显示上来(默认是不会显示它的)
toolbar = NavigationToolbar2Tk(canvas, root)
toolbar.update()
canvas._tkcanvas.pack(side=tkinter.TOP,  # get_tk_widget()得到的就是_tkcanvas
                      fill=tkinter.BOTH,
                      expand=tkinter.YES)


def on_key_event(event):
    """键盘事件处理"""
    print("你按了%s" % event.key)
    key_press_handler(event, canvas, toolbar)


# 绑定上面定义的键盘事件处理函数
canvas.mpl_connect('key_press_event', on_key_event)


def _quit():
    """点击退出按钮时调用这个函数"""
    root.quit()  # 结束主循环
    root.destroy()  # 销毁窗口


# 创建一个按钮,并把上面那个函数绑定过来
button = tkinter.Button(master=root, text="退出", command=_quit)
# 按钮放在下边
button.pack(side=tkinter.BOTTOM)

# 主循环
root.mainloop()
