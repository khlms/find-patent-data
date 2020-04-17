#! python3

from tkinter import *
from tkinter import ttk
from tkhtmlview import HTMLScrolledText ## insert HTML
from PIL import ImageTk,Image  ## show png, jpg, for python3: pip install pillow
from pathlib import Path
import mammoth ## convert docx to html
from pdf2image import convert_from_path # pdf to imagea
from tkinter import filedialog


from PatentGoogleScraper import PatentGoogleScrape

##TODO include pdf option: if no images, then download pdf and display instead
## otherweise, download pdf if activated and display as third tab next to description and claims
## when checking folder, also check for pdf and run pdf download instead, if selected

##TODO logging

##if PatentGoogleScraper raises exception, then pass on tab


class GUIBescheid(Tk):
    '''make GUI to compare patents'''
    ''' akte = [string(Aktenzeichen), Path(PDF file for images), Path(DOCX file for description/claims)] '''
    ''' (optional) compPatents =string or list of strings of patents names to compare to '''
    def __init__(self,akte=None, compPatents = []):
        if akte==None:
            root.withdraw()
            self.ww = PopupGUIInput(root)
            root.wait_window(self.ww.InsertAppl)
            akte = self.ww.akte
            try:
                compPatents.extend(self.ww.compPatents)
            except:
                pass
            root.deiconify()
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
            TabPriorArt(root,TabControlPA,self.UserPatent,w/2,5/12*h)

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
        Application(root,content,akte,w/2,5/12*h)
        #############################

        #############################
        '''make prior art part (right hand side) using tabs'''
        TabControlPA = ttk.Notebook(content)
        TabControlPA.grid(column=1, row=0, rowspan=3, sticky = N+E+S+W)

        '''the function AddPriorArt adds tabs using the class TabsPriorArt here'''
        for patentString in compPatents:
            try:
                TabPriorArt(root,TabControlPA,str(patentString),w/2,5/12*h)
            except FileNotFoundError:
                pass
        #############################

        # root.mainloop()



class PopupGUIInput(Toplevel):
    '''get inupt data for GUIBescheid'''
    def __init__(self, parent):
        self.InsertAppl = Toplevel(parent)
        self.InsertAppl.title = "Insert patent info to compare documents"
        # content = ttk.Frame(self.InsertAppl)
        # content.pack()

        label1 = ttk.Label(self.InsertAppl,text="Enter the Aktenzeichen:")
        label1.pack()
        self.userappl = ttk.Entry(self.InsertAppl)
        self.userappl.pack()
        self.userappl.focus()

        BttnFig = ttk.Button(self.InsertAppl,text="Choose pdf file for figures", command=self.browsePDF)
        BttnFig.pack()
        self.LblFig = ttk.Label(self.InsertAppl,text = "Chosen PDF: None")
        self.LblFig.pack()

        BttnText = ttk.Button(self.InsertAppl,text="Choose docx file for application", command=self.browseDOCX)
        BttnText.pack()
        self.LblText = ttk.Label(self.InsertAppl,text = "Chosen docx: None")
        self.LblText.pack()

        label2 = ttk.Label(self.InsertAppl,text="Comma-separated list of patent numbers:")
        label2.pack()
        self.userpatents = ttk.Entry(self.InsertAppl)
        self.userpatents.pack()

        bttnDone = Button(self.InsertAppl,text='Ok',command=self.cleanup)
        bttnDone.pack()


    def browsePDF(self):
        # Allow user to select a PDF file and store it
        self.PDFname = filedialog.askopenfilename(filetypes = (("PDF files", "*.pdf;*.PDF"),("All files", "*.*") ))
        self.LblFig.config(text = "Chosen PDF: " + str(self.PDFname))

    def browseDOCX(self):
        # Allow user to select a PDF file and store it
        self.DOCXname = filedialog.askopenfilename(filetypes = (("DOCX files", "*.docx;*.DOCX"),("All files", "*.*") ))
        self.LblText.config(text = "Chosen DOCX: " + str(self.DOCXname))


    def cleanup(self):

        self.akte=[self.userappl.get(),Path(self.PDFname),Path(self.DOCXname)]
        self.compPatents = [pat.strip() for pat in self.userpatents.get().split(",")]

        self.InsertAppl.destroy()



class PopupPatentEntry(object):
    def __init__(self,parent):
        self.top = Toplevel(parent)
        self.label1 = ttk.Label(self.top,text="Enter the patent number:")
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




class Application():
    def __init__(self,root,parent,akte,maxwidth,maxheight):
        '''Appl: insert Aktenzeichen'''
        self.ApplName = ttk.Label(parent,text = akte[0])
        self.ApplName.grid(column=0,row=0,sticky = N+W)

        '''Appl: insert figure(s) via pdf'''
        Figures(root,parent,akte[1],maxwidth,maxheight,1)

        '''Appl: insert description'''
        with open(akte[2], "rb") as docx_file:
            htmlResult = mammoth.convert_to_html(docx_file)
            htmlDoc = htmlResult.value
        self.ApplDesc = HTMLScrolledText(parent, html=htmlDoc)
        self.ApplDesc.grid(column=0, row=2, sticky = N+E+S+W)


class TabPriorArt(ttk.Frame):
    '''generates a new tab on the right using PatentNumber (string that identifies patent on patents.google.com, i.e. name of folder with data)'''
    def __init__(self,root,notebook,PatentNumber ,maxwidth,maxheight, PathToFiles = ""):
        ## TODO include root in options?
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
        Figures(root,self.tabD,PathToFiles,maxwidth,maxheight,0)

        '''insert tabs for description/claims (html)'''
        self.TabText = ttk.Notebook(self.tabD)
        self.TabText.grid(column=0, row=1)

        self.DDesc = HTMLScrolledText(self.TabText, html=open(PathToFiles / (PatentNumber + "-description.html"), 'r', encoding='utf8').read())
        self.DDesc.grid()
        self.TabText.add(self.DDesc, text="Description")

        self.DClaims = HTMLScrolledText(self.TabText, html=open(PathToFiles / (PatentNumber + "-claims.html"), 'r', encoding='utf8').read())
        self.DClaims.grid()
        self.TabText.add(self.DClaims, text="Claims")


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
        root.img = self.img
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




class Figures(ttk.Frame):
    def __init__(self,root,parent,PathToFile,maxwidth,maxheight,rownumber):
        self.PatentFig = ttk.Frame(parent)
        self.PatentFig.grid(column=0,row=rownumber)

        ##TODO might make a better gallery with https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/ttk-Label.html -> change state of label to display a different image. Probably doesn't work because we will lose zooming.
        '''container for image frames'''
        self.container = ttk.Frame(self.PatentFig)
        self.container.pack(side="top", fill="both", expand=True)
        # self.container.grid_rowconfigure(0, weight=1)
        # self.container.grid_columnconfigure(0, weight=1)

        '''list of figures'''
        self.ListofFigures = []
        if Path.is_dir(PathToFile):
            for currentFile in PathToFile.glob("*.jpg"):
                self.ListofFigures.append(currentFile)
            try:
                del(self.ListofFigures[0])
            except:
                pass
        elif Path.is_file(PathToFile):
            self.ApplPages = convert_from_path(PathToFile)
            for currentFile in self.ApplPages:
                self.ListofFigures.append(currentFile)

        self.ListofFigures.append("None")
        self.ListofFigures.insert(0,"None")

        self.ListofFrames = []
        for i in range(len(self.ListofFigures)-2):
            self.TempFrame = FigsBttns(root,self.container,self,i,len(self.ListofFigures)-2,self.ListofFigures[i+1],maxwidth,maxheight)
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


class FigsBttns(ttk.Frame):
    def __init__(self,root,parent,controller,indexInt,maxInt,currentImage,maxwidth,maxheight):
        ttk.Frame.__init__(self, parent)
        self.controller = controller
        LoadImage(root,self,currentImage,maxwidth,maxheight,4)

        '''make buttons'''
        self.prevBtn = ttk.Button(self, text="previous", command=lambda: self.controller.show_frame(indexInt-1))
        self.prevBtn.grid(column=0,row=1)

        self.PageLbl = ttk.Entry(self, width=5)
        self.PageLbl.insert(0,str(indexInt+1))
        self.PageLbl.grid(column=1,row=1, sticky=E)
        self.PageLbl.bind('<Return>', (lambda event: self.onReturn(self.PageLbl.get(),indexInt,maxInt)))

        self.OutOfLbl = ttk.Label(self, text= str( "/" + str(maxInt)))
        self.OutOfLbl.grid(column=2,row=1, sticky=W)

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

    def onReturn(self,UserPage,indexInt, maxInt):
        try:
            indexUserPage = int(UserPage) -1
            if indexUserPage >= 0 and indexUserPage <= maxInt:
                self.controller.show_frame(indexUserPage)
            else:
                self.Pagebl.delete(0,END)
                self.PageLbl.insert(0,str(indexInt+1))
        except:
            self.PageLbl.delete(0,END)
            self.PageLbl.insert(0,str(indexInt+1))





if __name__ == '__main__':
    root = Tk()
    GUIBescheid()
    # akte = ["Beispielaktenzeichen",Path("samplepdf.pdf"),Path("sampleantext.docx")]
    # compPatents = ["US10397476B2"]
    # GUIBescheid(akte,compPatents)
    root.mainloop()
