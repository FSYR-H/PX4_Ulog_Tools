from tkinter import *
from tkinter import ttk  #导入ttk模块，因为Combobox下拉菜单控件在ttk中

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

def xFunc(event,combobox):
    print(str(combobox)[-1])
    print(combobox.get())            # #获取选中的值方法1





if __name__ == '__main__':

    root = Tk()
    root.title("combobox demo")
    root.geometry("1300x500")

    com1, label1 = creat_combobox()
    
    com2, label2 = creat_combobox()
    com2.bind("<<ComboboxSelected>>", lambda event: xFunc(event, com2))
    com3, label3 = creat_combobox()


    mainloop()