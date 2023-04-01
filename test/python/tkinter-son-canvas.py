from tkinter import *

root = Tk()

# 创建一个Button，并将其绑定到一个函数上
def open_window():
    # 创建一个新的子窗口
    window = Toplevel(root)
    window.title("子窗口")
    window.geometry("500x300")

    # 创建一个Canvas
    canvas = Canvas(window, width=500, height=300)
    canvas.pack()

    # 在Canvas上添加一个Frame，并将Entry和Button放置在Frame中
    frame = Frame(canvas)
    frame.pack(pady=50)
    entry = Entry(frame)
    entry.pack(side=LEFT, padx=10)
    button = Button(frame, text="点击")
    button.pack(side=LEFT)

    # 将Frame放置在Canvas上
    canvas.create_window(200, 100, anchor=NW, window=frame)

button = Button(root, text="打开子窗口", command=open_window)
button.pack(pady=20)

root.mainloop()