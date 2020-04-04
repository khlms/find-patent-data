from tkinter import *
from tkinter import ttk

root = Tk()

content = ttk.Frame(root)
FrameD1Fig = ttk.Frame(content, borderwidth=5, relief="sunken", width=500, height=200)
FrameD1Desc = ttk.Frame(content, borderwidth=5, relief="sunken", width=500, height=300)

FrameD2Fig = ttk.Frame(content, borderwidth=5, relief="sunken", width=500, height=200)
FrameD2Desc = ttk.Frame(content, borderwidth=5, relief="sunken", width=500, height=300)

LabelD1 = ttk.Label(content, text="D1")
LabelD2 = ttk.Label(content, text="D2")

EntrySearch = ttk.Entry(content)
ButtonSearch = ttk.Button(content, text="Suchen")

content.grid(column=0, row=0)
FrameD1Fig.grid(column=1, row=0, columnspan=3, rowspan=2)
FrameD1Desc.grid(column=1, row=2, columnspan=3, rowspan=2)
LabelD1.grid(column=1, row=4, columnspan=3)

FrameD2Fig.grid(column=4, row=0, columnspan=3, rowspan=2)
FrameD2Desc.grid(column=4, row=2, columnspan=3, rowspan=2)
LabelD2.grid(column=4, row=4, columnspan=3)
EntrySearch.grid(column=0, row=0, rowspan=2)
ButtonSearch.grid(column=0, row=1)

root.mainloop()
