from tkinter import *
from tkinter import ttk  #导入ttk模块，因为Combobox下拉菜单控件在ttk中

def creat_com(com=None):

    str = "请点击下拉框选择："
    label = ttk.Label(root, text=str)
    label.pack(side=LEFT)

    combobox = ttk.Combobox(root)
    combobox.pack(side=LEFT)

    # 设置下拉菜单中的值
    combobox['value'] = ("北京","上海","广州","深圳")

    # 设置下拉菜单的默认值,默认值索引从0开始
    combobox.current(2)

    combobox.pack(side=TOP, anchor=NW)
    label.pack(side=TOP, anchor=NW)
    return combobox,label


if __name__ == '__main__':

    root = Tk()
    root.title("combobox demo")
    root.geometry("1300x500")

    com1, label1 = creat_com()
    com2, label2 = creat_com()
    com3, label3 = creat_com()


    mainloop()