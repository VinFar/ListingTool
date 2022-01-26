import tkinter as tk
from tkinter import  ttk
import tkinter.simpledialog
import os.path
import csv
import sys
import configparser

def ConfigParserCreate(ConfigFile):
    ConfigParser = configparser.RawConfigParser()
    ConfigParser.optionxform=str
    ConfigParser.read(ConfigFile)
    return ConfigParser
    
def ButtonCloseCallback():
    sys.exit()
    
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