#! python3

from tkinter import *
from tkinter import ttk
from tkhtmlview import HTMLScrolledText ## insert HTML
from tkinter import filedialog
from PIL import ImageTk,Image  ## show png, jpg, for python3: pip install pillow
from pathlib import Path


from PatentGoogleScraper import PatentGoogleScrape


class GUIBescheid(Tk):
    '''make GUI to compare patents'''
    def __init__(self):
        '''maximize window'''
        #TODO: maximize
        w, h = root.winfo_screenwidth(), root.winfo_screenheight()
        root.geometry("%dx%d+0+0" % (w, h))
        root.resizable(True, True) #TODO also resize content?
        '''make title'''
        root.title("Compare Patents") #TODO:better title

        #############################
        '''make menu'''
        def AddPriorArt():
            self.w=PopupPatentEntry(root)
            root.wait_window(self.w.top)
            self.UserPatent = self.w.value
            print(self.UserPatent)
            TabPriorArt(TabControlPA,self.UserPatent)

        def About():
            #TODO still useless
            print("Test")

        menu = Menu(root,tearoff=0)
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

        '''make content frame'''
        content = ttk.Frame(root)
        content.grid(column=0, row=0)

        #############################
        '''make application part (left side)'''
        ApplFig = ttk.Frame(content)
        ApplFig.grid(column=0,row=0,pady=(22,0)) #TODO hardcoded heigth of TabControlPA
        '''Appl: insert figure(s)'''
        LoadImage(root,ApplFig,"sample-picture1.jpg")
        #self.OpenImage(ApplFig,"sample-picture1.jpg")
        '''Appl: insert description'''
        ApplDesc = HTMLScrolledText(content, html=open("desc.html", 'r', encoding='utf8').read())
        ApplDesc.grid(column=0, row=1)
        #############################

        #############################
        '''make prior art part (right side) using tabs'''
        TabControlPA = ttk.Notebook(content)
        TabControlPA.grid(column=1, row=0, rowspan = 2)

        TabPriorArt(TabControlPA,"US20190313022A1")
        TabPriorArt(TabControlPA,"US10397476B2")
        #############################

        '''search field'''
        EntrySearch = ttk.Entry(content)
        ButtonSearch = ttk.Button(content, text="Suchen")

        #############################
        #EntrySearch.grid(column=0, row=0, rowspan=2)
        #ButtonSearch.grid(column=0, row=1)
        #############################


    def OpenImage(self,frame,PathToImage):
        '''load, resize and render'''
        imgload = Image.open(PathToImage)
        imgload.thumbnail((880, 380), Image.ANTIALIAS)
        imgrender = ImageTk.PhotoImage(imgload)
        '''add rendered image as label'''
        img = ttk.Label(frame, image = imgrender)
        '''save rendered image so that it survives the garbage collector'''
        img.image = imgrender
        '''positioning'''
        img.grid(column=0,row=0)


class PopupPatentEntry(object):
    def __init__(self,parent):
        self.top = Toplevel(parent)
        self.label1 = ttk.Label(self.top,text="Enther the patent number:")
        self.label1.pack()
        self.userpatent = ttk.Entry(self.top)
        self.userpatent.pack()
        self.userpatent.focus()

        self.label2 = ttk.Label(self.top,text="(Optional) Change default path:")
        self.label2.pack()
        self.userpath = ttk.Entry(self.top)
        self.userpath.pack()
        # self.userpath = filedialog.askdirectory()
        #TODO Pfad auswählen klappt noch nicht. Eingegebener Pfad wird derzeit noch ignoriert.

        self.bttnDone = Button(self.top,text='Ok',command=self.cleanup)
        self.bttnDone.pack()

    def cleanup(self):
        self.value=self.userpatent.get()
        self.top.destroy()


class TabPriorArt(ttk.Frame):
    '''generates a new tab on the right using PatentNumber (string that identifies patent on patents.google.com, i.e. name of folder with data)'''
    def __init__(self,notebook,PatentNumber, PathToFiles = ""):
        self.tabD = ttk.Frame(notebook)
        self.tabD.grid(column=0,row=0)
        notebook.add(self.tabD, text=PatentNumber)

        '''download patent'''
        if PathToFiles == "":
            PatentGoogleScrape(PatentNumber)
            PathToFiles = Path.cwd() / "patents" / PatentNumber
        else:
            PatentgoogleScrape(PatentNumber, PathToFiles)
            PathToFiles = PathToFiles / PatentNumber

        '''insert images'''
        PatentFigures(root,self.tabD,PathToFiles)

        '''insert tabs for description/claims (html)'''
        self.TabText = ttk.Notebook(self.tabD)
        self.TabText.grid(column=0, row=1)

        self.DDesc = HTMLScrolledText(self.TabText, html=open(PathToFiles / (PatentNumber + "-description.html"), 'r', encoding='utf8').read())
        self.DDesc.grid()
        self.TabText.add(self.DDesc, text="Description")

        self.DClaims = HTMLScrolledText(self.TabText, html=open(PathToFiles / (PatentNumber + "-claims.html"), 'r', encoding='utf8').read())
        self.DClaims.grid()
        self.TabText.add(self.DClaims, text="Claims")


class PatentFigures(ttk.Frame):
    def __init__(self,root,parent,PathToFiles):
        self.DFig = ttk.Frame(parent)
        self.DFig.grid(column=0,row=0)

        '''container for image frames'''
        self.container = ttk.Frame(self.DFig)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        '''list of figures'''
        self.ListofFigures = []
        for currentFile in PathToFiles.glob("*.jpg"):
            self.ListofFigures.append(currentFile)
        self.ListofFigures.append("None")
        self.ListofFigures.insert(0,"None")

        self.ListofFrames = []
        for i in range(len(self.ListofFigures)-2):
            self.TempFrame = FigsBttns(root,self.container,self,i,len(self.ListofFigures)-2,self.ListofFigures[i+1])
            self.ListofFrames.append(self.TempFrame)
            self.TempFrame.grid(row=0, column=0, sticky="nsew")

        try:
            self.show_frame(0)
        except:
            pass
            #TODO: make empty frame the size of the other frames


    def show_frame(self, FrameNumber):
            '''Show a frame for the given page name'''
            frame = self.ListofFrames[FrameNumber]
            frame.tkraise()

class FigsBttns(ttk.Frame):
    def __init__(self,root,parent,controller,indexInt,maxInt,currentImage):
        ttk.Frame.__init__(self, parent)
        self.controller = controller
        LoadImage(root,self,currentImage)
        # self.OpenImage(DFig,ListofFigures[0])

        '''make buttons'''
        self.prevBtn = ttk.Button(self, text="previous", command=lambda: self.controller.show_frame(indexInt-1))
        self.prevBtn.grid(column=0,row=1)
        self.nextBtn = ttk.Button(self, text="next", command=lambda: self.controller.show_frame(indexInt+1))
        self.nextBtn.grid(column=1,row=1)

        if indexInt == 0:
            self.prevBtn['state'] = 'disabled'
            self.nextBtn['state'] = 'normal'
        elif indexInt < maxInt-1:
            self.prevBtn['state'] = 'normal'
            self.nextBtn['state'] = 'normal'
        elif indexInt == maxInt -1:
            self.prevBtn['state'] = 'normal'
            self.nextBtn['state'] = 'disabled'



class LoadImage(ttk.Frame):
    def __init__(self,root,parent,PathToImage):
        # TODO: zoomen nicht ins thumbnail
        # TODO: hardcoded sizes
        self.canvas = Canvas(parent,width=500,height=380)
        self.canvas.grid(column=0,row=0,columnspan=2)
        self.orig_img = Image.open(PathToImage)
        self.orig_img.thumbnail((500, 380), Image.ANTIALIAS)
        self.img = ImageTk.PhotoImage(self.orig_img)
        self.canvas.create_image(0,0,image=self.img, anchor="nw")

        self.zoomcycle = 0
        self.zimg_id = None

        self.canvas.bind("<MouseWheel>",self.zoomer)
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
    '''make root widget'''
    root = Tk()

    GUIBescheid()

    '''make mainloop'''
    root.mainloop()
