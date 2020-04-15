#! python3

from tkinter import *
from tkinter import ttk
from tkhtmlview import HTMLScrolledText ## insert HTML
from tkinter import filedialog
from PIL import ImageTk,Image  ## show png, jpg, for python3: pip install pillow
from pathlib import Path
import mammoth ## convert docx to html
# from tkdocviewer import * ## show pdf documents. Needs ghostscript
from pdf2image import convert_from_path


from PatentGoogleScraper import PatentGoogleScrape

##TODO include pdf option: if no images, then download pdf and display instead
## otherweise, download pdf if activated and display as third tab next to description and claims
## when checking folder, also check for pdf and run pdf download instead, if selected

##TODO logging

class GUIBescheid(Tk):
    '''make GUI to compare patents'''
    def __init__(self):
        # maximize window
        ##TODO: actually maximize
        w, h = root.winfo_screenwidth(), root.winfo_screenheight()
        root.geometry("%dx%d+0+0" % (w, h))
        root.resizable(True, True) ##TODO also resize content? or scroll barss
        '''make title'''
        root.title("Compare Patents") ##TODO:better title

        #############################
        '''make menu'''
        def AddPriorArt():
            self.w=PopupPatentEntry(root)
            root.wait_window(self.w.top)
            self.UserPatent = self.w.value
            TabPriorArt(TabControlPA,self.UserPatent,w/2,5/12*h)

        def About():
            ##TODO still useless
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
        content.grid(column=0, row=0, sticky=N+E+S+W)
        content.grid_columnconfigure(0,weight=1)
        content.grid_columnconfigure(1,weight=1)

        #############################
        '''make application part (left hand side)'''
        ##TODO: show name/Aktenzeichen
        # ApplName = ttk.Label(content, text="Name of patent")
        ApplName = ttk.Label(content,text = "Name of patent")
        ApplName.grid(column=0,row=0,sticky = N+W)

        '''Appl: insert figure(s) via pdf'''
        # ApplFig = ttk.Frame(content)
        # ApplFig.grid(column=0,row=0,pady=(22,0)) ##TODO hardcoded heigth of TabControlPA
        # # ApplFig.grid(column=0,row=1)
        # LoadImage(root,ApplFig,"sample-picture1.jpg")

        # ApplFig = DocViewer(content, use_ttk=True)
        # ApplFig.grid(column=0,row=1,sticky = N+S+E+W)
        # # ApplFig.grid(column=0,row=0,pady=(22,0))
        # ApplFig.display_file("samplepdf.pdf")

        ApplFigures(root,content,"samplepdf.pdf",w/2,5/12*h)

        '''Appl: insert description'''
        with open("sampleantext.docx", "rb") as docx_file:
            htmlResult = mammoth.convert_to_html(docx_file)
            htmlDoc = htmlResult.value
        ApplDesc = HTMLScrolledText(content, html=htmlDoc)
        ApplDesc.grid(column=0, row=2, sticky = N+E+S+W)
        # ApplDesc.grid(column=0, row=2)
        #############################

        #############################
        '''make prior art part (right hand side) using tabs'''
        TabControlPA = ttk.Notebook(content)
        TabControlPA.grid(column=1, row=0, rowspan=3, sticky = N+E+S+W)

        '''the function AddPriorArt adds tabs using the class TabsPriorArt here'''
        TabPriorArt(TabControlPA,"US10397476B2",w/2,5/12*h)
        #############################

        '''search field'''
        EntrySearch = ttk.Entry(content)
        ButtonSearch = ttk.Button(content, text="Suchen")

        #############################
        #EntrySearch.grid(column=0, row=0, rowspan=2)
        #ButtonSearch.grid(column=0, row=1)
        #############################



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
        ##TODO Pfad auswählen klappt noch nicht. Eingegebener Pfad wird derzeit noch ignoriert.

        self.bttnDone = Button(self.top,text='Ok',command=self.cleanup)
        self.bttnDone.pack()

    def cleanup(self):
        self.value=self.userpatent.get()
        self.top.destroy()


class TabPriorArt(ttk.Frame):
    '''generates a new tab on the right using PatentNumber (string that identifies patent on patents.google.com, i.e. name of folder with data)'''
    def __init__(self,notebook,PatentNumber ,maxwidth,maxheight, PathToFiles = ""):
        ## TODO include root in options
        self.tabD = ttk.Frame(notebook)
        self.tabD.grid(column=0,row=0, sticky = N+S+E+W)
        # self.TabD.
        notebook.add(self.tabD, text=PatentNumber)

        '''download patent'''
        if PathToFiles == "":
            PatentGoogleScrape(PatentNumber)
            PathToFiles = Path.cwd() / "patents" / PatentNumber
        else:
            PatentgoogleScrape(PatentNumber, PathToFiles)
            PathToFiles = PathToFiles / PatentNumber

        '''insert images'''
        PriorArtFigures(root,self.tabD,PathToFiles,maxwidth,maxheight)

        '''insert tabs for description/claims (html)'''
        self.TabText = ttk.Notebook(self.tabD)
        self.TabText.grid(column=0, row=1)

        self.DDesc = HTMLScrolledText(self.TabText, html=open(PathToFiles / (PatentNumber + "-description.html"), 'r', encoding='utf8').read())
        self.DDesc.grid()
        self.TabText.add(self.DDesc, text="Description")

        self.DClaims = HTMLScrolledText(self.TabText, html=open(PathToFiles / (PatentNumber + "-claims.html"), 'r', encoding='utf8').read())
        self.DClaims.grid()
        self.TabText.add(self.DClaims, text="Claims")


class PriorArtFigures(ttk.Frame):
    def __init__(self,root,parent,PathToFiles,maxwidth,maxheight):
        self.DFig = ttk.Frame(parent)
        self.DFig.grid(column=0,row=0)

        ##TODO might make a better gallery with https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/ttk-Label.html -> change state of label to display a different image. Probably doesn't work because we will lose zooming.
        '''container for image frames'''
        self.container = ttk.Frame(self.DFig)
        self.container.pack(side="top", fill="both", expand=True)
        # self.container.grid_rowconfigure(0, weight=1)
        # self.container.grid_columnconfigure(0, weight=1)

        '''list of figures'''
        self.ListofFigures = []
        for currentFile in PathToFiles.glob("*.jpg"):
            self.ListofFigures.append(currentFile)
        try:
            del(self.ListofFigures[0])
        except:
            pass
        self.ListofFigures.append("None")
        self.ListofFigures.insert(0,"None")

        self.ListofFrames = []
        for i in range(len(self.ListofFigures)-2):
            self.TempFrame = PriorArtFigsBttns(root,self.container,self,i,len(self.ListofFigures)-2,self.ListofFigures[i+1],maxwidth,maxheight)
            self.ListofFrames.append(self.TempFrame)
            self.TempFrame.grid(row=0, column=0, sticky="nsew")

        try:
            self.show_frame(0)
        except:
            pass
            ##TODO: download and show pdf


    def show_frame(self, FrameNumber):
            '''Show a frame for the given page name'''
            frame = self.ListofFrames[FrameNumber]
            frame.tkraise()

class PriorArtFigsBttns(ttk.Frame):
    def __init__(self,root,parent,controller,indexInt,maxInt,currentImage,maxwidth,maxheight):
        ttk.Frame.__init__(self, parent)
        self.controller = controller
        LoadImage(root,self,currentImage,maxwidth,maxheight,2)

        '''make buttons'''
        self.prevBtn = ttk.Button(self, text="previous", command=lambda: self.controller.show_frame(indexInt-1))
        self.prevBtn.grid(column=0,row=1)
        self.nextBtn = ttk.Button(self, text="next", command=lambda: self.controller.show_frame(indexInt+1))
        self.nextBtn.grid(column=1,row=1)

        if indexInt == 0:
            self.prevBtn['state'] = 'disabled'
        else:
            self.prevBtn['state'] = 'normal'
        if indexInt == maxInt -1:
            self.nextBtn['state'] = 'disabled'
        else:
            self.nextBtn['state'] = 'normal<'




class LoadImage(ttk.Frame):
    def __init__(self,root,parent,PathToImage,maxwidth,maxheight,ColumnCount):
        ## TODO: hardcoded sizes
        self.canvas = Canvas(parent,width=maxwidth,height=maxheight)
        self.canvas.grid(column=0,row=0,columnspan=ColumnCount)
        try:
            self.orig_img = Image.open(PathToImage)
            self.orig_img.thumbnail((maxwidth, maxheight), Image.ANTIALIAS)
            self.img = ImageTk.PhotoImage(self.orig_img)
        except:
            self.orig_img = PathToImage
            self.orig_img.thumbnail((maxwidth,maxheight), Image.ANTIALIAS)
            self.img = ImageTk.PhotoImage(self.orig_img)
        self.canvas.create_image(maxwidth/2,maxheight/2,image=self.img, anchor=CENTER)


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




class ApplFigures(ttk.Frame):
    def __init__(self,root,parent,PathToPDF,maxwidth,maxheight):
        self.ApplFig = ttk.Frame(parent)
        self.ApplFig.grid(column=0,row=1)

        ##TODO might make a better gallery with https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/ttk-Label.html -> change state of label to display a different image. Probably doesn't work because we will lose zooming.
        '''container for image frames'''
        self.container = ttk.Frame(self.ApplFig)
        self.container.pack(side="top", fill="both", expand=True)
        # self.container.grid_rowconfigure(0, weight=1)
        # self.container.grid_columnconfigure(0, weight=1)

        '''list of figures'''
        self.ListofFigures = []
        # self.ApplPages = convert_from_path(PathToPDF,size=(maxwidth,maxheight))
        self.ApplPages = convert_from_path(PathToPDF)
        for currentFile in self.ApplPages:
            self.ListofFigures.append(currentFile)
        self.ListofFigures.append("None")
        self.ListofFigures.insert(0,"None")

        self.ListofFrames = []
        for i in range(len(self.ListofFigures)-2):
            self.TempFrame = ApplFigsBttns(root,self.container,self,i,len(self.ListofFigures)-2,self.ListofFigures[i+1],maxwidth,maxheight)
            self.ListofFrames.append(self.TempFrame)
            self.TempFrame.grid(row=0, column=0, sticky="nsew")

        try:
            self.show_frame(0)
        except:
            pass


    def show_frame(self, FrameNumber):
            '''Show a frame for the given page name'''
            frame = self.ListofFrames[FrameNumber]
            frame.tkraise()


class ApplFigsBttns(ttk.Frame):
    def __init__(self,root,parent,controller,indexInt,maxInt,currentImage,maxwidth,maxheight):
        ttk.Frame.__init__(self, parent)
        self.controller = controller
        LoadImage(root,self,currentImage,maxwidth,maxheight,4)

        '''make buttons'''
        self.prevBtn = ttk.Button(self, text="previous", command=lambda: self.controller.show_frame(indexInt-1))
        self.prevBtn.grid(column=0,row=1)

        self.OutOfLbl = ttk.Entry(self)
        self.OutOfLbl.insert(0,str(indexInt+1))
        self.OutOfLbl.grid(column=1,row=1)
        root.bind('<Return>',self.onReturn()) ##TODO happens on startup but not on return
        self.OutOfLbl2 = ttk.Label(self, text= str( "/" + str(maxInt)))
        self.OutOfLbl2.grid(column=2,row=1)

        self.nextBtn = ttk.Button(self, text="next", command=lambda: self.controller.show_frame(indexInt+1))
        self.nextBtn.grid(column=3,row=1)

        if indexInt == 0:
            self.prevBtn['state'] = 'disabled'
        else:
            self.prevBtn['state'] = 'normal'
        if indexInt == maxInt -1:
            self.nextBtn['state'] = 'disabled'
        else:
            self.nextBtn['state'] = 'normal'

    def onReturn(self):
        self.newFig = self.OutOfLbl.get()
        try:
            self.controller.show_frame(int(self.newFig)-1)
        except:
            print(self.newFig)
        ## TODO doesn't work yet. Pressing return doesn't do anything




if __name__ == '__main__':
    '''make root widget'''
    root = Tk()

    GUIBescheid()

    '''make mainloop'''
    root.mainloop()
