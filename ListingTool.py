import tkinter as tk
import Functions


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        sbf = Functions.ScrollbarFrame(self)
        #root.geometry('400x300')
        #root.title(ConfigParser['General']['WindowTitle'])

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        sbf.grid(row=0, column=0, sticky='nsew')
        #sbf.canvas.config(width=800,height=600)
        
        FileNameSku = "SKU_File.csv"
        ConfigFileName = "Config.txt"

        ConfigParser = Functions.ConfigParserCreate(ConfigFileName)

        # Some data, layout into the sbf.scrolled_frame
        content = sbf.scrolled_frame
        
        AllSections = ConfigParser.sections()
        RegisterFrames = AllSections[1]
        #self.geometry(ConfigParser['General']['WindowSize'])
        #self.attributes('-zoomed')
        w, h = self.winfo_screenwidth()-20, self.winfo_screenheight()-100
        self.geometry("%dx%d+0+0" % (w, h))

        for Ctr,Section in enumerate(ConfigParser[RegisterFrames]):
            Functions.GuiAddLabel(Ctr,0,content,Section)
            
            ConfigContentCurrent = ConfigParser[RegisterFrames][Section]
            
            if Functions.ConfigParserIsDropDown(ConfigContentCurrent):
                print("ConfigElement {:s} is Dropdown".format(Section))
                DropDownList = Functions.ConfigParserGetElementsOfDropDown(ConfigContentCurrent)
                Functions.GuiAddDropDown(Ctr,1,content,DropDownList)
            else:
                print("ConfigElement {:s} is Text Input".format(Section))
                Functions.GuiAddTextInput(Ctr,1,content,'')



if __name__ == "__main__":
    App().mainloop()