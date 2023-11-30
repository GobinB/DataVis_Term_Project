import datetime as dt
import tkinter as tk
import tkinter.font as tkFont
import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from pandas.tseries.offsets import DateOffset

mpl.use('TkAgg')

# Global theme colors
THEME_BACKGROUND = "#000000"  # Black
THEME_FOREGROUND = "#FFA500"  # Orange

clicked = []
clicked2 = []

class windows(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        # Adding a title to the window
        self.wm_title("Main Screen")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        width = 700
        height = 700

        screenWidth = self.winfo_screenwidth()
        screenHeight = self.winfo_screenheight()
        align = '%dx%d+%d+%d' % (width, height, (screenWidth - width) / 2, (screenHeight - height) / 2)
        self.geometry(align)
        
        container = tk.Frame(self)
        self.configure(background="#c7d6ed")
        container.grid(row=0, column=0)

        # We will now create a dictionary of frames
        self.frames = {}

        for F in (MainScreen, Participant, SelectDataAttributes, ShowGraph):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
            frame.configure(background="#c7d6ed")

        # Using a method to switch frames
        self.show_frame(MainScreen)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class MainScreen(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, background=THEME_BACKGROUND)

        label = tk.Label(self, text="Data Visualization\nPress Start To Begin", bg=THEME_BACKGROUND, fg=THEME_FOREGROUND)
        ft1 = tkFont.Font(family='Times', size=32)
        label["font"] = ft1
        label["justify"] = "center"
        label.pack(padx=200, pady=100)

        StartButton = tk.Button(
            self,
            text="Start",
            bg=THEME_BACKGROUND, 
            fg=THEME_FOREGROUND, 
            activebackground=THEME_FOREGROUND,
            command=lambda: controller.show_frame(Participant),
        )
        StartButton["activebackground"] = "#00ced1"  
        ft2 = tkFont.Font(family='Times', size=20)
        StartButton["font"] = ft2
        StartButton["justify"] = "center"
        StartButton["text"] = "Start"
        StartButton["relief"] = "ridge"
        StartButton.pack()

class Participant(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        global clicked
        global clicked2

        print("data is : ", clicked)
        self.tclicked = ''
        SelectAttriutesPage = tk.Button(
            self,
            command=lambda: controller.show_frame(SelectDataAttributes),
        )
        SelectAttriutesPage["activebackground"] = "#9b60ad"
        SelectAttriutesPage["bg"] = "#c71585"
        ft8 = tkFont.Font(family='Times', size=20)
        SelectAttriutesPage["font"] = ft8
        SelectAttriutesPage["justify"] = "center"
        SelectAttriutesPage["text"] = "Select Data Attributes"
        SelectAttriutesPage["relief"] = "ridge"
        SelectAttriutesPage.grid(row=1, column=0, padx=1, pady=5, sticky=EW,
                                 columnspan=4)  # pack(side=BOTTOM,expand=True, fill=BOTH,  anchor=S)

        # def dates1(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.frame1 = Frame(self, highlightbackground="blue", highlightthickness=2)
        self.frame1.grid(row=0, column=0)  # pack(side=LEFT,fill=Y)
        self.frame2 = Frame(self, highlightbackground="blue", highlightthickness=2)
        self.frame2.grid(row=0, column=1)  # pack(side=RIGHT, fill=Y)
        self.participant310 = tk.Button(self.frame1, text="Participant 310")
        self.participant310.config(command=lambda btn1=self.participant310: self.get_fname(btn1))
        self.participant311 = tk.Button(self.frame1, text="Participant 311")
        self.participant311.config(command=lambda btn1=self.participant311: self.get_fname(btn1))
        self.participant312 = tk.Button(self.frame1, text="Participant 312")
        self.participant312.config(command=lambda btn1=self.participant312: self.get_fname(btn1))
        self.participant310["activebackground"] = ["#00ced1"]
        self.participant310["bg"] = "#00ced1"
        ft2 = tkFont.Font(family='Times', size=20)
        self.participant310["font"] = ft2
        self.participant310["fg"] = "#393d49"
        self.participant310["justify"] = "center"
        self.participant310["relief"] = "ridge"

        self.participant311["activebackground"] = ["#00ced1"]
        self.participant311["bg"] = "#00ced1"
        ft2 = tkFont.Font(family='Times', size=20)
        self.participant311["font"] = ft2
        self.participant311["fg"] = "#393d49"
        self.participant311["justify"] = "center"
        self.participant311["relief"] = "ridge"

        self.participant312["activebackground"] = ["#00ced1"]
        self.participant312["bg"] = "#00ced1"
        ft2 = tkFont.Font(family='Times', size=20)
        self.participant312["font"] = ft2
        self.participant312["fg"] = "#393d49"
        self.participant312["justify"] = "center"
        self.participant312["relief"] = "ridge"

        self.Jan18_2020 = tk.Button(self.frame1, text="2020-01-18", bg=THEME_BACKGROUND, fg=THEME_FOREGROUND, activebackground=THEME_FOREGROUND)
        self.Jan18_2020.config(command=lambda btn=self.Jan18_2020: self.showall(btn))
        self.Jan18_2020.grid(row=1, column=1, padx=10, pady=5)

        self.Jan19_2020 = tk.Button(self.frame1, text="2020-01-19", bg=THEME_BACKGROUND, fg=THEME_FOREGROUND, activebackground=THEME_FOREGROUND)
        self.Jan19_2020.config(command=lambda btn=self.Jan19_2020: self.showall(btn))
        self.Jan19_2020.grid(row=2, column=1, padx=10, pady=5)

        self.Jan20_2020 = tk.Button(self.frame1, text="2020-01-20", bg=THEME_BACKGROUND, fg=THEME_FOREGROUND, activebackground=THEME_FOREGROUND)
        self.Jan20_2020.config(command=lambda btn=self.Jan20_2020: self.parts(btn))
        self.Jan20_2020.grid(row=3, column=1, padx=10, pady=5)

        self.Jan21_2020 = tk.Button(self.frame1, text="2020-01-21", bg=THEME_BACKGROUND, fg=THEME_FOREGROUND, activebackground=THEME_FOREGROUND)
        self.Jan21_2020.config(command=lambda btn=self.Jan21_2020: self.parts(btn))
        self.Jan21_2020.grid(row=4, column=1, padx=10, pady=5)
        self.Jan21_2020["activebackground"] = "#00ced1"
        self.Jan21_2020["bg"] = "#00ced1"
        self.Jan21_2020["font"] = ft2
        self.Jan21_2020["fg"] = "#393d49"
        self.Jan21_2020["justify"] = "center"
        self.Jan21_2020["relief"] = "ridge"

        self.Jan20_2020["activebackground"] = "#00ced1"
        self.Jan20_2020["bg"] = "#00ced1"
        self.Jan20_2020["font"] = ft2
        self.Jan20_2020["fg"] = "#393d49"
        self.Jan20_2020["justify"] = "center"
        self.Jan20_2020["relief"] = "ridge"

        self.Jan19_2020["activebackground"] = "#00ced1"
        self.Jan19_2020["bg"] = "#00ced1"
        self.Jan19_2020["font"] = ft2
        self.Jan19_2020["fg"] = "#393d49"
        self.Jan19_2020["justify"] = "center"
        self.Jan19_2020["relief"] = "ridge"

        self.Jan18_2020["activebackground"] = "#00ced1"
        self.Jan18_2020["bg"] = "#00ced1"
        self.Jan18_2020["font"] = ft2
        self.Jan18_2020["fg"] = "#393d49"
        self.Jan18_2020["justify"] = "center"
        self.Jan18_2020["relief"] = "ridge"

    def remove(self, widget1):
        widget1.grid_remove()

    def display(self, widget1, widget2, widget3):
        widget1.grid(row=1, column=2, padx=10, pady=5)
        widget2.grid(row=2, column=2, padx=10, pady=5)
        widget3.grid(row=3, column=2, padx=10, pady=5)

    def display2(self, widget1, widget2):
        widget1.grid(row=1, column=2, padx=10, pady=5)
        widget2.grid(row=3, column=2, padx=10, pady=5)

    
    def parts(self, btn):
        global clicked
        global clicked
        text = btn.cget("text")
        text = text.replace('-', '')
        clicked.append(text)
        if (len(clicked) > 1):
            clicked.pop(0)
        print("clicked:", clicked)
        if (text == "20200120" or text == "20200121"):
            self.display2(self.participant310, self.participant312)
        if (bool(self.participant311.winfo_exists()) == True):
            self.remove(self.participant311)

    def showall(self, btn):
        global clicked
        global clicked2
        text = btn.cget("text")
        text = text.replace('-', '')
        clicked.append(text)
        if (len(clicked) > 1):
            clicked.pop(0)
        # prclicked:", text)
        print("clicked:", clicked)
        if (text == "20200118" or text == "20200119"):
            self.display(self.participant310, self.participant311, self.participant312)

    def get_fname(self, btn1):
        text = btn1.cget("text")
        if (text == "Participant 310"):
            text = "310"
        elif (text == "Participant 311"):
            text = "311"
        elif (text == "Participant 312"):
            text = "312"

        text = text.replace('-', '')
        clicked2.append(text)
        if (len(clicked2) > 1):
            clicked2.pop(0)
        print("here", clicked, " : ", clicked2)

    @classmethod
    def ttfd():
        return clicked, clicked2

    @staticmethod
    # @classmethod
    def g1234():
        global clicked
        global clicked2
        global file
        clicked = clicked
        clicked2 = clicked2
        # Participaclicked
        print(clicked)
        date_t = clicked
        participant = (clicked2)
        de = "".join(date_t)
        pe = "".join(participant)
        de1 = ("r'/", de)
        
        if (clicked and clicked2):
            file = open("Dataset/" + "".join(clicked) + "/" + "".join(clicked2) + "/summary.csv")
           

        else:
            file = open("Dataset/" + "20200118" + "/" + "310" + "/summary.csv")
        return file



class SelectDataAttributes(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        frame1 = Frame(self, highlightbackground=THEME_FOREGROUND, highlightthickness=2)
        frame1.grid(padx=10, pady=50, row=0, column=0)  # pack(side=LEFT,fill=Y)
        label1 = tk.Label(frame1, text="Select Attribute(s)")
        ft1 = tkFont.Font(family='Times', size=14)
        label1["font"] = ft1
        label1["justify"] = "center"
        label1.grid(padx=10, pady=5, row=0, column=0)


        # Create a dictionary to hold the BooleanVars for each attribute
        self.attribute_vars = {
            "Acc Magnitude Avg": tk.BooleanVar(),
            "Eda Avg": tk.BooleanVar(),
            "Temp Avg": tk.BooleanVar(),
            "Movement intensity": tk.BooleanVar(),
            "Step Count": tk.BooleanVar(),
            "Rest": tk.BooleanVar(),
            "On Wrist": tk.BooleanVar(),
            # Add more attributes here if needed
        }

        # Create the checkboxes for the attributes
        row_offset = 1
        for attribute, var in self.attribute_vars.items():
            tk.Checkbutton(
                frame1,
                text=attribute,
                variable=var,
                onvalue=True,
                offvalue=False
            ).grid(padx=10, pady=5, row=row_offset, column=0)
            row_offset += 1

        ShowData = tk.Button(
            self,
            text="Show Data",
            command=lambda: controller.show_frame(ShowGraph),
        )
        ShowData["activebackground"] = "#9b60ad"
        ShowData["bg"] = "#c71585"
        ft3 = tkFont.Font(family='Times', size=20)
        ShowData["font"] = ft3
        ShowData["fg"] = "#393d49"
        ShowData["justify"] = "center"
        ShowData["text"] = "Show Data"
        ShowData["relief"] = "ridge"
        ShowData.grid(row=7, column=0, padx=1, pady=5, sticky=EW, columnspan=6)



filename = ''
df = pd.read_csv


def remove(widget1):
    widget1.pack_forget()


local_time = False


def update_button_value():
    global local_time
    local_time = not local_time
    print(local_time)


class ShowGraph(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.canvas = None
        self.toolbar = None
        self.scroll_y = None
        self.graph()
        global filename
        global clicked
        global local_time

 
        print("been here:", clicked)

        redo1 = tk.Button(
            self,
            text="Show Data",
            command=lambda: controller.show_frame(MainScreen),
        )
        redo1["activebackground"] = "#9b60ad"
        redo1["bg"] = "#c71585"
        ft3 = tkFont.Font(family='Times', size=20)
        redo1["font"] = ft3
        redo1["fg"] = "#393d49"
        redo1["justify"] = "center"
        redo1["text"] = "redo"
        redo1["relief"] = "ridge"
        redo1.pack(side=BOTTOM, fill="x")  # .grid(row= 7,column=0,padx=1, pady=1, sticky=EW, columnspan=6)

   
    def showit(self):
        # First, clear the existing graph and toolbar if they exist
        if self.canvas:
            self.canvas.get_tk_widget().pack_forget()
        if self.toolbar:
            self.toolbar.pack_forget()

        # Retrieve the filename or data
        global filename
        if filename:
            try:
                df = pd.read_csv(filename, skiprows=[1])  # Customize as per your CSV format
                fig, ax = plt.subplots(figsize=(7, 7), dpi=100)

                # Example: Plotting
                x = df['Datetime (UTC)']  # Change these column names as per your CSV
                y = df['Acc magnitude avg']  # Change these column names as per your CSV
                ax.plot(x, y, label='Acc magnitude avg', color='blue')

                ax.set_xlabel('Datetime (UTC)')
                ax.set_ylabel('Acc magnitude avg')
                ax.set_title('Customized Graph')
                ax.legend(loc='upper right')

                self.canvas = FigureCanvasTkAgg(fig, master=self)
                self.canvas.get_tk_widget().pack(side=LEFT, fill=BOTH, expand=True)
                self.toolbar = NavigationToolbar2Tk(self.canvas, self)
                self.toolbar.pack(side=TOP, fill=X)

                self.canvas.draw()

            except Exception as e:
                print(f"Error loading or plotting data: {e}")
        else:
            print("No data file selected.")


    def graph(self):
        # Creating a frame to hold graph-related controls and information
        frame1 = Frame(self, highlightbackground="blue", highlightthickness=2)
        frame1["bg"] = "#00ced1"
        frame1.pack(side=LEFT, fill=BOTH, expand=True)

        # Example of adding labels for user instructions or info
        me1 = ["Home/Reset  ", "h or r or home"]
        me2 = ["Back  ", "c or left arrow or backspace"]
        me3 = ["Forward  ", "v or right arrow"]
        me4 = ["Pan/Zoom  ", " p"]
        me5 = ["Zoom-to-rect  ", " o"]
        me6 = ["Save  ", "  ctrl + s"]

        label_instructions = [me1, me2, me3, me4, me5, me6]
        for instruction in label_instructions:
            label = tk.Label(frame1, text=instruction)
            label.pack(anchor="w", pady=2)  # Adjust padding as needed

        # Add a button to trigger the graph display
        show_graph_button = tk.Button(
            self,
            text="Show Selected Graph",
            command=self.showit  # Method to execute when button is pressed
        )
        show_graph_button.pack(side=TOP, pady=10)  # Adjust padding as neede

        
    def convertDate(zuluDate):
        input_format = '%Y-%m-%d %H%MZ'  # input example: 2020-01-17T23:48:00Z
        output_format = '%m-%d:%H%M'
        date = dt.strptime(zuluDate, input_format)  # convert String zuluDate into Datetime, format it
        return dt.strftime(date, output_format)  # convert back to String and return it


if __name__ == "__main__":
    testObj = windows()


    testObj.mainloop()