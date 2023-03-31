from tkinter import *
from threading import Thread
import time

def long_running_function():
    # 模拟一个耗时的操作
    time.sleep(5)

def open_second_window():
    # 关闭主窗口
    root.withdraw()

    # 创建第二级窗口
    global second_window
    second_window = Toplevel()
    second_window.title("第二级窗口")
    second_window.geometry("300x200")
    second_window.resizable(False, False)

    # 创建Button并指定command参数
    button = Button(second_window, text="运行程序", command=run_function_and_wait)
    button.pack(pady=20)

def run_function_and_wait():
    # 创建等待提示框
    wait_window = Toplevel(second_window)
    wait_window.title("请稍候...")
    wait_window.geometry("300x100")
    wait_window.resizable(False, False)

    # 将焦点锁定在等待提示框上，禁止用户与其他窗口进行交互
    wait_window.grab_set()

    # 创建等待提示框的Label
    wait_label = Label(wait_window, text="请稍候...", font=("Arial", 20))
    wait_label.pack(pady=20)

    # 禁用等待提示框的关闭按钮
    wait_window.protocol("WM_DELETE_WINDOW", lambda: None)

    # 在新的线程中执行耗时的操作
    thread = Thread(target=long_running_function)
    thread.start()

    # 在等待提示框中显示提示信息
    while thread.is_alive():
        wait_label.config(text="正在处理，请稍候...")
        wait_window.update_idletasks()
        time.sleep(0.1)

    # 关闭等待提示框并释放焦点锁定
    wait_window.destroy()
    second_window.grab_release()

    # 重新打开主窗口
    # root.deiconify()

root = Tk()

# 创建Button并指定command参数
button = Button(root, text="打开第二级窗口", command=open_second_window)
button.pack(pady=20)

root.mainloop()