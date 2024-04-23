from tkinter import *
import configparser
from tkinter import ttk  #导入ttk模块，因为Combobox下拉菜单控件在ttk中
import sys
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
def creat_combobox(com=None):

    str = "请点击下拉框选择："
    label = ttk.Label(root, text=str)
    label.pack(side=LEFT)

    combobox = ttk.Combobox(root)
    combobox.pack(side=LEFT)

    # 设置下拉菜单中的值
    combobox['value'] = ("北京","上海","广州","深圳")
    combobox['state'] = "readonly"
    # 设置下拉菜单的默认值,默认值索引从0开始
    combobox.current(2)

    combobox.pack(side=TOP, anchor=NW)
    label.pack(side=TOP, anchor=NW)

    return combobox,label

def xFunc1(event,combobox):
    print(combobox.get())
    # flag = combobox.get()
    
    # fig = mat_plot_demo(flag)
    # canvas = FigureCanvasTkAgg(fig, master = root)
    # canvas.draw()
    # canvas.get_tk_widget().pack()

def mat_plot_demo(flag):
    fig, ax = plt.subplots()
    if flag == '深圳':
        ax.plot([1,2,3,5],[4,5,6,9])
    elif flag == '上海':
        ax.plot([1,2,3,4],[4,5,6,7])
    return fig


def callback(a):

    print('退出',a)
    sys.exit()




if __name__ == '__main__':


    root = Tk()
    root.title("combobox demo")
    root.geometry("1300x500")

    com1, label1 = creat_combobox()
    
    com2, label2 = creat_combobox()
    com2.bind("<<ComboboxSelected>>", lambda event: xFunc1(event, com2))
    com3, label3 = creat_combobox()
    

    but1=Button(root,text='退出',command=lambda : callback(' ')) 
    but1.pack(side=TOP, anchor=NW)
    

    mainloop()