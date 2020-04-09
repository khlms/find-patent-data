#! python3

from tkinter import *
from tkinter import ttk
from tkhtmlview import HTMLScrolledText # insert HTML
from PIL import ImageTk,Image  # to be able to show png, jpg, for python3: pip install pillow
from pathlib import Path


from PatentGoogleScraper import PatentGoogleScrape


class GUIBescheid:
    def __init__(self):
        # maximize window
        #TODO: maximize
        w, h = root.winfo_screenwidth(), root.winfo_screenheight()
        root.geometry("%dx%d+0+0" % (w, h))
        root.resizable(True, True) #TODO also resize content
        # make title
        root.title("Compare Patents") #TODO:better title

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
        content.grid(column=0, row=0)

        #############################
        # make application part (left side)
        ApplFig = ttk.Frame(content)
        ApplFig.grid(column=0,row=0,pady=(22,0)) #TODO hardcoded heigth of TabControlPA
        # Appl: insert figure(s)
        LoadImage(root,ApplFig,"sample-picture1.jpg")
        #self.OpenImage(ApplFig,"sample-picture1.jpg")
        # Appl: insert description
        ApplDesc = HTMLScrolledText(content, html=open("desc.html", 'r', encoding='utf8').read())
        ApplDesc.grid(column=0, row=1)
        #############################

        #############################
        # make prior art part (right side) using tabs
        TabControlPA = ttk.Notebook(content)
        TabControlPA.grid(column=1, row=0, rowspan = 2)

        self.TabPriorArt(TabControlPA,"US20190313022A1")
        self.TabPriorArt(TabControlPA,"US10397476B2")
        #############################

        # search field
        EntrySearch = ttk.Entry(content)
        ButtonSearch = ttk.Button(content, text="Suchen")

        #############################
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

        # # add rendered image as canvas
        # img = Canvas(frame,width=1000, height=500)
        # img.pack()
        # img.create_image(20,20,anchor=NW,image = imgrender)

        # save rendered image so that it survives the garbage collector
        img.image = imgrender
        # positioning
        img.grid(column=0,row=0)


    def TabPriorArt(self,notebook,PatentNumber, PathToFiles = ""):
        ## generates a new tab on the right using PatentNumber (string that identifies patent on patents.google.com, i.e. name of folder with data)
        tabD = ttk.Frame(notebook)
        tabD.grid(column=0,row=0)
        notebook.add(tabD, text=PatentNumber)

        ## download patent
        if PathToFiles == "":
            PatentGoogleScrape(PatentNumber)
            PathToFiles = Path.cwd() / "patents" / PatentNumber
        else:
            PatentgoogleScrape(PatentNumber, PathToFiles)
            PathToFiles = PathToFiles / PatentNumber
        ## make list of figures
        ListofFigures = []
        for currentFile in PathToFiles.glob("*.jpg"):
            ListofFigures.append(currentFile)
        DFig = ttk.Frame(tabD)
        DFig.grid(column=0,row=0)
        #LoadImage(root,DFig,"sample-picture3.jpg")
        self.OpenImage(DFig,ListofFigures[0])

        # insert description
        DDesc = HTMLScrolledText(tabD, html=open("desc.html", 'r', encoding='utf8').read())
        DDesc.grid(column=0, row=1)


class LoadImage:
    def __init__(self,root,frame,PathToImage):
        # TODO: größe anpassen, zoomen nicht überall
        # TODO: zoomen nicht ins thumbnail
        # TODO: zoom funktioniert nicht bei doppelter Verwendung (links+rechts)
        # TODO: hardcoded sizes
        self.canvas = Canvas(frame,width=500,height=380)
        self.canvas.grid(column=0,row=0)
        frame.grid(column=0,row=0)
        self.orig_img = Image.open(PathToImage)
        self.orig_img.thumbnail((500, 380), Image.ANTIALIAS)
        self.img = ImageTk.PhotoImage(self.orig_img)
        self.canvas.create_image(0,0,image=self.img, anchor="nw")

        self.zoomcycle = 0
        self.zimg_id = None

        root.bind("<MouseWheel>",self.zoomer)
        self.canvas.bind("<Motion>",self.crop)

    def zoomer(self,event):
        if (event.delta > 0):
            if self.zoomcycle != 4: self.zoomcycle += 1
        elif (event.delta < 0):
            if self.zoomcycle != 0: self.zoomcycle -= 1
        self.crop(event)

    def crop(self,event):
        if self.zimg_id: self.canvas.delete(self.zimg_id)
        if (self.zoomcycle) != 0:
            x,y = event.x, event.y
            xFac = 30
            yFac = 20
            if self.zoomcycle == 1:
                tmp = self.orig_img.crop((x-4*xFac,y-4*yFac,x+4*xFac,y+4*yFac))
            elif self.zoomcycle == 2:
                tmp = self.orig_img.crop((x-3*xFac,y-3*yFac,x+3*xFac,y+3*yFac))
            elif self.zoomcycle == 3:
                tmp = self.orig_img.crop((x-2*xFac,y-2*yFac,x+2*xFac,y+2*yFac))
            elif self.zoomcycle == 4:
                tmp = self.orig_img.crop((x-xFac,y-yFac,x+xFac,y+yFac))
            size = 600,400
            self.zimg = ImageTk.PhotoImage(tmp.resize(size))
            self.zimg_id = self.canvas.create_image(event.x,event.y,image=self.zimg)


if __name__ == '__main__':
    # make root widget
    root = Tk()

    GUIBescheid()

    # make mainloop
    root.mainloop()
