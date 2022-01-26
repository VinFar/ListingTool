import tkinter as tk
from tkinter import  ttk
import tkinter.simpledialog
import configparser
import os.path
from datetime import datetime
import fnmatch
import Functions

FileNameSku = "SKU_File.csv"
ConfigFileName = "Config.txt"

ConfigParser = Functions.ConfigParserCreate(ConfigFileName)

root = tk.Tk()
#root.geometry('400x300')
root.title(ConfigParser['General']['WindowTitle'])

notebook = ttk.Notebook(root)
notebook.pack(pady=10, expand=True)

SkuFileDir = ConfigParser['General']['SkuFileDir']
IgnoreSkuError=False;

AllSections = ConfigParser.sections()
Sections = AllSections[1:]
FileNameCsv = ConfigParser['General']['FileName']+datetime.now().strftime("%d-%m-%Y_%H-%M")+'.csv'
rootDir = ConfigParser['General']['rootDir']

for Tab,ThisSection in enumerate(Sections):
    Frame = ttk.Frame(notebook)
    Frame.pack(fill='both', expand=True)
    notebook.add(Frame, text=ThisSection)
    Entries = list()
    
    SkuIDX = 0
    
    for row,key in enumerate(ConfigParser[ThisSection]):
        if fnmatch.fnmatch(ConfigParser[ThisSection][key],"{*}"):
            TmpLabel = ttk.Label(master=Frame, text=key)
            TmpLabel.grid(row=row, column=0, padx='5', pady='5', sticky='ew')
            itemList = ConfigParser[ThisSection][key][1:-1].split(',')
            variable = tkinter.StringVar(Frame)
            variable.set(itemList[0])
            TmpEntry = ttk.OptionMenu(Frame,variable,*itemList)
            TmpEntry.grid(row=row,column=1, padx='5', pady='5', sticky='ew')
            Entries.append(variable)
        else:
            TmpLabel = ttk.Label(master=Frame, text=key)
            TmpLabel.grid(row=row, column=0, padx='5', pady='5', sticky='ew')
            TmpEntry = ttk.Entry(master=Frame)
            TmpEntry.grid(row=row,column=1, padx='5', pady='5', sticky='ew')
            Entries.append(TmpEntry)
        if key == 'SKU':
            SkuIDX=row
    column, rowGrid = Frame.grid_size()
    column=column-1
    
    HeaderForThisFile = [k[0] for k in ConfigParser.items(ThisSection)]
    FilePath = os.path.join(rootDir,ThisSection+"_"+FileNameCsv)
    Functions.CreateCsvWithHeader(FilePath,HeaderForThisFile)
    
    Button = ttk.Button(text="Speichern",master=Frame)
    Button.configure(command=lambda Entry=Entries,FilePathFile=FilePath,SKU=SkuIDX: Functions.ButtonSaveCallback(FilePathFile,Entry,SKU))
    Button.grid(row=rowGrid, column=column, padx='5', pady='5', sticky='nsew')
    
    Button = ttk.Button(text="Schließen",master=Frame,command=Functions.ButtonCloseCallback)
    Button.grid(row=rowGrid, column=0, padx='5', pady='5', sticky='nsew')
           
root.mainloop()
