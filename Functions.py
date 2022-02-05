import tkinter as tk
from tkinter import  ttk
import tkinter.simpledialog
import os.path
import csv
import sys
import configparser
import fnmatch

def ConfigParserCreate(ConfigFile):
    ConfigParser = configparser.RawConfigParser()
    ConfigParser.optionxform=str
    ConfigParser.read(ConfigFile)
    return ConfigParser
    
def ButtonCloseCallback():
    sys.exit()
    
def ConfigParserIsDropDown(ConfigElement:str):
    return fnmatch.fnmatch(ConfigElement,"{*}")

def ConfigParserGetElementsOfDropDown(DropDownElement:str):
    return DropDownElement[1:-1].split(',')

def GuiAddLabel(Zeile:int,Spalte:int,Frame:ttk.Frame,Text:str):
    TextLabelCurrent = ttk.Label(Frame,text=Text)
    TextLabelCurrent.grid(column=Spalte,row=Zeile)
    
def GuiAddDropDown(Zeile:int,Spalte:int,Frame:ttk.Frame,DropDownContent:list[str]):
    variable = tkinter.StringVar(Frame)
    variable.set(DropDownContent[0])
    TmpEntry = ttk.OptionMenu(Frame,variable,*DropDownContent)
    TmpEntry.grid(row=Zeile,column=Spalte, padx='5', pady='5', sticky='ew')
    
def GuiAddTextInput(Zeile:int,Spalte:int,Frame:ttk.Frame,DefaultText:str):
    TmpEntry = ttk.Entry(master=Frame)
    TmpEntry.grid(row=Zeile,column=Spalte, padx='5', pady='5', sticky='ew')
    
def ButtonIngoreError(win):
    global IgnoreSkuError
    IgnoreSkuError= True
    win.destroy()

def ButtonCancel(win:tk.Toplevel):
    global IgnoreSkuError
    IgnoreSkuError=False
    win.destroy()

def PopUpSkuFound(SkuFromGUI):
    win = tk.Toplevel()
    win.wm_title("Window")

    Label = tk.Label(win,text="Die SKU "+SkuFromGUI+" wurde bereits verwendet")
    Label.grid(row=0,column=0)

    l = tk.Button(win, text="Ignorieren",command=lambda arg=win:ButtonIngoreError(arg))
    l.grid(row=1, column=0)

    b = ttk.Button(win, text="Abbrechen",command=lambda arg=win:ButtonCancel(arg))
    b.grid(row=1, column=1)
    win.wait_window()
    print("Closing PopUp")
    
def WriteItemToFile(FilePath,Items):
    with open(FilePath,'a+',newline="") as f:
        CsvWriter = csv.writer(f,delimiter=";")
        CsvWriter.writerow(Items)
        
def WriteSkuToFile(SkuFromGUI):
    FilePathSku=os.path.join(SkuFileDir,FileNameSku)
       
    with open(FilePathSku,'a+',newline="") as f:
        CsvWriter = csv.writer(f,delimiter=";")
        CsvWriter.writerow([SkuFromGUI])
        
def ButtonSaveCallback(FilePath,Section:list[tk.Entry],SkuIdx):
    EmptyGUI = all(v.get()=='' for v in Section)
    FoundSku = False
    if not EmptyGUI:
        ItemList = [k.get() for k in Section]
        SkuFromGUI = Section[SkuIdx].get()
        FilePathSku=os.path.join(SkuFileDir,FileNameSku)
        with open(FilePathSku,'r',newline="") as f:
            CsvReader = csv.reader(f,delimiter=';')
            for line in CsvReader:
                if line[0] == SkuFromGUI:
                    FoundSku = True
                    print("Found SKU")
                    break
        for ThisEntry in Section:
            if type(ThisEntry) == tkinter.StringVar:
                pass
            else:
                ThisEntry.delete(0,tk.END)
        if FoundSku:
            PopUpSkuFound(SkuFromGUI)
            if not IgnoreSkuError:
                return
            
        WriteItemToFile(FilePath,ItemList)
        WriteSkuToFile(SkuFromGUI)
        
        print("Wrote Data to " + FilePath)
    else:
        print("Empty GUI. Did not write anything to File")
            
                

def CreateCsvWithHeader(FilePath,Header):
    exists = False
    if os.path.exists(FilePath):
        print("File does exist")
        exists=True
    else:
        print("File does not exist. Creating File")
        exists=False
        
    with open(FilePath,'a+',newline="") as FileDescriptorCsv:
        CsvWriter = csv.writer(FileDescriptorCsv,delimiter=';')
        if exists==False:
            CsvWriter.writerow(Header)
    return

class ScrollbarFrame(tk.Frame):
    """
    Extends class tk.Frame to support a scrollable Frame 
    This class is independent from the widgets to be scrolled and 
    can be used to replace a standard tk.Frame
    """
    def __init__(self, parent, **kwargs):
        tk.Frame.__init__(self, parent, **kwargs)
        
        # The Scrollbar, layout to the right
        vsb = tk.Scrollbar(self, orient="vertical")
        vsb.pack(side="right", fill="y")

        # The Canvas which supports the Scrollbar Interface, layout to the left
        self.canvas = tk.Canvas(self, borderwidth=0)
        self.canvas.pack(side="left", fill="both", expand=True)

        # Bind the Scrollbar to the self.canvas Scrollbar Interface
        self.canvas.configure(yscrollcommand=vsb.set)
        vsb.configure(command=self.canvas.yview)

        # The Frame to be scrolled, layout into the canvas
        # All widgets to be scrolled have to use this Frame as parent
        self.scrolled_frame = tk.Frame(self.canvas, background=self.canvas.cget('bg'))
        self.canvas.create_window((4, 4), window=self.scrolled_frame, anchor="nw")

        # Configures the scrollregion of the Canvas dynamically
        self.scrolled_frame.bind("<Configure>", self._configure_window)
        self.scrolled_frame.bind('<Enter>', self._bound_to_mousewheel)
        self.scrolled_frame.bind('<Leave>', self._unbound_to_mousewheel)

    def _bound_to_mousewheel(self, event):
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)   

    def _unbound_to_mousewheel(self, event):
        self.canvas.unbind_all("<MouseWheel>") 

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")  

    def _configure_window(self, event):
        # update the scrollbars to match the size of the inner frame
        size = (self.scrolled_frame.winfo_reqwidth(), self.scrolled_frame.winfo_reqheight())
        self.canvas.config(scrollregion='0 0 %s %s' % size)
        if self.scrolled_frame.winfo_reqwidth() != self.canvas.winfo_width():
            # update the canvasas's width to fit the inner frame
            self.canvas.config(width = self.scrolled_frame.winfo_reqwidth())
        if self.scrolled_frame.winfo_reqheight() != self.canvas.winfo_height():
            # update the canvasas's width to fit the inner frame
            self.canvas.config(height = self.scrolled_frame.winfo_reqheight())
