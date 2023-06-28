from tkinter import *
from tkinter import ttk

root = Tk()
frame1 = ttk.Frame(root)
frame1.grid()

style = ttk.Style()
style.theme_use('classic')

label1 = ttk.Label(
    frame1,
    text='Hello',
    background='#0000aa',
    foreground='#ffffff',
    padding=(5, 10))
label1.grid(row=0, column=0)

label2 = ttk.Label(
    frame1,
    text='World',
    background='#ffffff',
    width=20,
    anchor=E,
    padding=(5, 10))
label2.grid(row=0, column=1)

root.mainloop()