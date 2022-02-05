import tkinter as tk
import Functions

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
        self.state = False
        self.scrolled_frame.bind("<F11>", self.toggle_fullscreen)
        self.scrolled_frame.bind("<Escape>", self.end_fullscreen)

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
            
    def toggle_fullscreen(self, event=None):
        self.state = not self.state  # Just toggling the boolean
        self.attributes("-fullscreen", self.state)
        return "break"

    def end_fullscreen(self, event=None):
        self.state = False
        self.attributes("-fullscreen", False)
        return "break"



class App(tk.Tk):
    def __init__(self):
        super().__init__()

        sbf = ScrollbarFrame(self)
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