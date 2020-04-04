from tkinter import *
from tkinter import ttk
from tkhtmlview import HTMLLabel
import tkinter as tk

root = tk.Tk()

root.title("Patent Tool")

tab_control = ttk.Notebook(root)
tab1 = ttk.Frame(tab_control)
tab2 = ttk.Frame(tab_control)

tab_control.add(tab1, text='First')
tab_control.add(tab2, text='Second')

html_label = HTMLLabel(tab1, html='<h1 style="color: red; text-align: center"> Hello World </H1>')
html_label.grid(column=0, row=0)

lbl2 = Label(tab2, text= 'label2')
lbl2.grid(column=0, row=0)

tab_control.pack(expand=1, fill='both')

root.mainloop()
