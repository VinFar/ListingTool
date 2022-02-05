import tkinter as tk
from tokenize import Ignore
import Functions
import os
from datetime import datetime

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("ListingTool V1.1")
        self.FileNameSku = "SKU_File.csv"
        ConfigFileName = "Config.txt"
        ConfigParser = Functions.ConfigParserCreate(ConfigFileName)
        self.FilePathSku = ConfigParser['General']['SkuFileDir']
        self.FilePathItem = ConfigParser['General']['FileName']+datetime.now().strftime("%d-%m-%Y_%H-%M")+'.csv'
                
        AllSections = ConfigParser.sections()
        RegisterFrames = AllSections[1]
        
        HeaderForThisFile = [k[0] for k in ConfigParser.items(RegisterFrames)]
        Functions.CreateCsvWithHeader(self.FilePathItem,HeaderForThisFile)

        sbf = Functions.ScrollbarFrame(self)
        self.geometry(ConfigParser['General']['WindowSize'])

        sbf.grid(row=0, column=0)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
    
        self.Frame = sbf.scrolled_frame

        
        self.EntriesList = []
        self.SkuIdx=-1

        for Ctr,Section in enumerate(ConfigParser[RegisterFrames]):
            Functions.GuiAddLabel(Ctr,0,self.Frame,Section)
            
            ConfigContentCurrent = ConfigParser[RegisterFrames][Section]
            if Section == 'SKU':
                self.SkuIdx = Ctr
            
            if Functions.ConfigParserIsDropDown(ConfigContentCurrent):
                print("ConfigElement {:s} is Dropdown".format(Section))
                DropDownList = Functions.ConfigParserGetElementsOfDropDown(ConfigContentCurrent)
                StrVar = Functions.GuiAddDropDown(Ctr,1,self.Frame,DropDownList)
                self.EntriesList.append(StrVar)
            else:
                print("ConfigElement {:s} is Text Input".format(Section))
                StrVar = Functions.GuiAddTextInput(Ctr,1,self.Frame,'')
                self.EntriesList.append(StrVar)
                            
        column, rowGrid = self.Frame.grid_size()

        Button = tk.Button(text="Speichern",master=self.Frame,command=self.ButtonSaveCallback)
        Button.grid(row=rowGrid, column=column-1, padx='5', pady='5', sticky='nsew')
        
        Button = tk.Button(text="Schließen",master=self.Frame,command=Functions.ButtonCloseCallback)
        Button.grid(row=rowGrid, column=0, padx='5', pady='5', sticky='nsew')
        
    def ButtonSaveCallback(self):
        print("Button Save Callback")
        StrVars = self.EntriesList
        InputList = [k.get() for k in StrVars]
        

        if self.SkuIdx != -1:
            FoundSku = False
            SkuFromGUI = StrVars[self.SkuIdx].get()
            
            FullFilePathSku = os.path.join(self.FilePathSku,self.FileNameSku)
            IgnoreSkuError = Functions.CheckSkuWithFile(FullFilePathSku,SkuFromGUI)
            if IgnoreSkuError:
                Functions.WriteSkuToFile(FullFilePathSku,SkuFromGUI)
        Functions.WriteItemToFile(self.FilePathItem,InputList)
        
        return

if __name__ == "__main__":
    App().mainloop()