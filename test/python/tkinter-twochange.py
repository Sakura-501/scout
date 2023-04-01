from tkinter import *

def open_second_window():
    # 隐藏主窗口
    root.withdraw()

    # 创建第二个窗口
    second_window = Toplevel()
    second_window.title("第二个窗口")
    second_window.geometry("300x200")
    second_window.resizable(False, False)

    # 添加关闭事件
    second_window.protocol("WM_DELETE_WINDOW", lambda: close_second_window(second_window))

def close_second_window(second_window):
    # 销毁第二个窗口
    second_window.destroy()

    # 显示主窗口
    root.deiconify()

root = Tk()

# 添加打开子窗口的按钮
open_button = Button(root, text="打开子窗口", command=open_second_window)
open_button.pack(pady=20)

root.mainloop()