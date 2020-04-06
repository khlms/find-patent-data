#! python3

from tkinter import *
from tkinter import ttk
from tkhtmlview import HTMLScrolledText # insert HTML
from PIL import ImageTk,Image  # to be able to show png, jpg, for python3: pip install pillow


class GUIBescheid:
    def __init__(self):
        # maximize window
        #TODO: maximize
        w, h = root.winfo_screenwidth(), root.winfo_screenheight()
        root.geometry("%dx%d+0+0" % (w, h))

        # make title
        root.title("Patent Tool") #TODO:better title

        #############################
        # make menu
        def AddPriorArt():
            print("Test")
        def About():
            print("Test")

        menu = Menu(root)
        root.config(menu=menu)
        filemenu = Menu(menu,tearoff=0)
        menu.add_cascade(label="Stand der Technik", menu=filemenu)
        filemenu.add_command(label="Hinzufügen", command=AddPriorArt)
        filemenu.add_separator()
        filemenu.add_command(label="Beenden", command=root.quit)
        helpmenu = Menu(menu,tearoff=0)
        menu.add_cascade(label="Hilfe", menu=helpmenu)
        helpmenu.add_command(label="Über...", command=About)
        #############################

        # make content frame
        content = ttk.Frame(root)

        #############################
        # make application part (left side)
        # Appl: insert figure(s)
        self.OpenImage(content,"sample-picture.jpg")
        ApplDesc = HTMLScrolledText(content, html='<h1 style="color: red; text-align: center"> Hello World </H1><p>asfa</p><p>asfa</p><p>asfa</p><p>asfa</p><p>asfa</p><p>asfa</p><p>asfa</p><p>asfa</p><p>asfa</p><p>asfa</p><p>asfa</p><p>asfa</p>')
        #############################

        #############################
        # make prior art (D1 to Dn) part (right side)

        # make tabs
        TabControlPA = ttk.Notebook(content)
        tabD1 = ttk.Frame(TabControlPA)
        tabD2 = ttk.Frame(TabControlPA)
        TabControlPA.add(tabD1, text='D1')
        TabControlPA.add(tabD2, text='D2')

        # D1: insert figure(s)
        self.OpenImage(tabD1,"sample-picture.jpg")
        # D1Fig = ttk.Label(tabD1, image = img)
        # D1Fig.grid(column=0, row=0)

        # D1: insert description
        D1Desc = HTMLScrolledText(tabD1, html='<h1 style="color: red; text-align: center"> Hello World </H1><p>asfa</p><p>asfa</p><p>asfa</p><p>asfa</p><p>asfa</p><p>asfa</p><p>asfa</p><p>asfa</p><p>asfa</p><p>asfa</p><p>asfa</p><p>asfa</p>')
        D1Desc.grid(column=0, row=1)
        #############################

        # search field
        EntrySearch = ttk.Entry(content)
        ButtonSearch = ttk.Button(content, text="Suchen")

        #############################
        # positioning
        content.grid(column=0, row=0)
        # ApplFig.grid(column=0, row=0)
        ApplDesc.grid(column=0, row=1)
        TabControlPA.grid(column=1, row=0, rowspan = 2)

        #EntrySearch.grid(column=0, row=0, rowspan=2)
        #ButtonSearch.grid(column=0, row=1)
        #############################


    def OpenImage(self,frame,PathToImage):
        # load, resize and render
        imgload = Image.open(PathToImage)
        imgload.thumbnail((880, 380), Image.ANTIALIAS)
        imgrender = ImageTk.PhotoImage(imgload)
        # add rendered image as label
        img = ttk.Label(frame, image = imgrender)
        img.pack()

        # # add rendered image as canvas
        # img = Canvas(frame,width=1000, height=500)
        # img.pack()
        # img.create_image(20,20,anchor=NW,image = imgrender)

        # save rendered image so that it survives the garbage collector
        img.image = imgrender
        # positioning
        img.grid(column=0,row=0)



if __name__ == '__main__':
    # make root widget
    root = Tk()

    GUIBescheid()

    # make mainloop
    root.mainloop()
