#! python3

from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from pathlib import Path
from GUIBescheid import GUIBescheid

class GUIInput(Tk):
    '''get inupt data for GUIBescheid'''
    def __init__(self):
        InsertAppl = Toplevel(root)

        InsertAppl.title = "Insert patent info to compare documents"
        content = ttk.Frame(InsertAppl)
        content.pack()

        label1 = ttk.Label(content,text="Enter the Aktenzeichen:")
        label1.pack()
        self.userappl = ttk.Entry(content)
        self.userappl.pack()
        self.userappl.focus()

        BttnFig = ttk.Button(content,text="Choose pdf file for figures", command=self.browsePDF)
        BttnFig.pack()
        self.LblFig = ttk.Label(content,text = "Chosen PDF: None")
        self.LblFig.pack()

        BttnText = ttk.Button(content,text="Choose docx file for application", command=self.browseDOCX)
        BttnText.pack()
        self.LblText = ttk.Label(content,text = "Chosen docx: None")
        self.LblText.pack()


        label2 = ttk.Label(content,text="Comma-separated list of patent numbers:")
        label2.pack()
        self.userpatents = ttk.Entry(content)
        self.userpatents.pack()

        bttnDone = Button(content,text='Ok',command=self.cleanup)
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

        akte=[self.userappl.get(),Path(self.PDFname),Path(self.DOCXname)]
        print(akte)
        compPatents = [pat.strip() for pat in self.userpatents.get().split(",")]
        print(compPatents)

        InsertAppl.destroy()




if __name__ == '__main__':
    InsertAppl = Tk()
    GUIInput()
    InsertAppl.mainloop()
