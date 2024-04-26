import tkinter as tk

def get_input_and_disable():
    # 获取输入框的内容
    input_text = entry.get()
    print("输入的内容是:", input_text)
    # 禁用输入框
    entry.config(state='disabled')
    root.destroy()

# 创建Tkinter窗口
root = tk.Tk()
root.geometry('500x200')



# 创建一个StringVar对象来存储输入框的内容
entry_text1 = tk.StringVar()
# 设置初始的提示词

entry_text1.set("在下方输入数据储存名字")


label = tk.Label(root, textvariable=entry_text1)
# 使用grid布局，将文本标签放在第0行
label.place(relx=0.5, rely=0.4, anchor='center')

entry_text = tk.StringVar()
entry_text.set("在此输入")

# 创建输入框，将StringVar对象设置为输入框的textvariable
entry = tk.Entry(root, textvariable=entry_text)
# entry = tk.Entry(root)
entry.place(relx=0.5, rely=0.5, anchor='center')

# 创建按钮，点击按钮后会调用get_input_and_disable函数
button = tk.Button(root, text="提交", command=get_input_and_disable)
button.place(relx=0.7, rely=0.5, anchor='center')

# 运行Tkinter事件循环
root.mainloop()
