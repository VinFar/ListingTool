import tkinter as tk
from tkinter import  ttk
import tkinter.simpledialog
import os.path
import csv
import sys
import configparser
import fnmatch

IgnoreSkuError=True

def ConfigParserCreate(ConfigFile):
    ConfigParser = configparser.RawConfigParser()
    ConfigParser.optionxform=str
    ConfigParser.read(ConfigFile)
    return ConfigParser
    
def ButtonCloseCallback():
    print("Button Close Callback")
    sys.exit()
    
def ConfigParserIsDropDown(ConfigElement:str):
    return fnmatch.fnmatch(ConfigElement,"{*}")

def ConfigParserGetElementsOfDropDown(DropDownElement:str):
    return DropDownElement[1:-1].split(',')

def GuiAddLabel(Zeile:int,Spalte:int,Frame:ttk.Frame,Text:str):
    TextLabelCurrent = ttk.Label(Frame,text=Text)
    TextLabelCurrent.grid(column=Spalte,row=Zeile)
    
def GuiAddDropDown(Zeile:int,Spalte:int,Frame:ttk.Frame,DropDownContent:list[str]):
    StrVar = tkinter.StringVar(Frame)
    StrVar.set(DropDownContent[0])
    TmpEntry = ttk.OptionMenu(Frame,StrVar,*DropDownContent)
    TmpEntry.grid(row=Zeile,column=Spalte, padx='5', pady='5', sticky='ew')
    return StrVar
    
def GuiAddTextInput(Zeile:int,Spalte:int,Frame:ttk.Frame,DefaultText:str):
    StrVar = tk.StringVar()
    TmpEntry = ttk.Entry(master=Frame,textvariable=StrVar)
    TmpEntry.grid(row=Zeile,column=Spalte, padx='5', pady='5', sticky='ew')
    return StrVar
    
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
        
def CheckSkuWithFile(FullSkuPath,SkuFromGUI):
    if SkuFromGUI != '':
        with open(FullSkuPath,'r',newline="") as f:
            CsvReader = csv.reader(f,delimiter=';')
            for line in CsvReader:
                if line[0] != '':
                    if line[0] == SkuFromGUI:
                        FoundSku = True
                        global IgnoreSkuError
                        IgnoreSkuError= True
                        PopUpSkuFound(SkuFromGUI)
                        if IgnoreSkuError:
                            return True
                        else:
                            return False
    return True
                    
def WriteSkuToFile(FullSkuPath,SkuFromGUI):
    if SkuFromGUI != '':
        with open(FullSkuPath,'a+',newline="") as f:
            CsvWriter = csv.writer(f,delimiter=';')
            CsvWriter.writerow([SkuFromGUI])

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
