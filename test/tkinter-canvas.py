from tkinter import *

root = Tk()

# 创建一个Button，并将其绑定到一个函数上
def open_window():
    # 创建一个新的子窗口
    window = Toplevel(root)
    window.title("子窗口")
    window.geometry("500x300")

    # 创建一个Canvas，并添加一张背景图片
    canvas = Canvas(window, width=1000, height=600)
    canvas.pack()
    image = PhotoImage(file="../img/9.png")
    canvas.create_image(0, 0, anchor=NW, image=image)

    # 在Canvas上添加一个Label
    label = Label(canvas, text="这是子窗口中的标签")
    label.place(x=200, y=100)

button = Button(root, text="打开子窗口", command=open_window)
button.pack(pady=20)

root.mainloop()