from tkinter import *
from tkinter import filedialog

root = Tk()
root.withdraw()

file_path = filedialog.asksaveasfilename(defaultextension='.pkl', filetypes=[('pikle Files', '*.pkl'), ('All Files', '*.*')])

print('Selected file:', file_path)