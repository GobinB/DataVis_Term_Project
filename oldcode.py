import datetime as dt
import tkinter as tk
import tkinter.font as tkFont
from tkinter import *
import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from pandas.tseries.offsets import DateOffset

import matplotlib.dates as mdates

import matplotlib.pyplot as plt
from datetime import datetime
import pytz

mpl.use('TkAgg')


class windows(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        # Adding a title to the window
        self.wm_title("Main Screen")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        width = 700
        height = 700
        # creating a frame and assigning it to container

        screenWidth = self.winfo_screenwidth()
        screenHeight = self.winfo_screenheight()
        align = '%dx%d+%d+%d' % (width, height, (screenWidth - width) / 2, (screenHeight - height) / 2)
        self.geometry(align)
        #
        container = tk.Frame(self)
        self.configure(background="#c7d6ed")
        # specifying the region where the frame is packed in root
        # container.pack(side="top", fill="both", expand=True)
        container.grid(row=0, column=0)
        # configuring the location of the container using grid
        # container.grid_rowconfigure(0, weight=1)
        # container.grid_columnconfigure(0, weight=1)

        # We will now create a dictionary of frames
        self.frames = {}
        # we'll create the frames themselves later but let's add the components to the dictionary.
        for F in (MainScreen, Paricipant, SelectDataAttributes, ShowGraph):
            frame = F(container, self)

            # the windows class acts as the root window for the frames.
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
            frame.configure(background="#c7d6ed")

        # Using a method to switch frames
        self.show_frame(MainScreen)

    def show_frame(self, cont):
        frame = self.frames[cont]
        # raises the current frame to the top
        frame.tkraise()


class MainScreen(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text="Welcome\nPlease Press the Button to\nStart Data Visualization")
        ft1 = tkFont.Font(family='Times', size=32)
        label["font"] = ft1
        label["justify"] = "center"
        # label.place(x=50,y=50,width=515,height=147)
        label.pack(padx=100, pady=50)
        # label.pack()

        # We use the switch_window_button in order to call the show_frame() method as a lambda function
        StartButton = tk.Button(
            self,
            text="Start",
            command=lambda: controller.show_frame(Paricipant),
        )
        StartButton["activebackground"] = "#00ced1"
        StartButton["bg"] = "#00ced1"
        ft2 = tkFont.Font(family='Times', size=20)
        StartButton["font"] = ft2
        StartButton["fg"] = "#393d49"
        StartButton["justify"] = "center"
        StartButton["text"] = "Start"
        StartButton["relief"] = "ridge"
        # StartButton.place(x=140,y=260,width=310,height=342)
        # StartButton.pack(side="bottom", fill=tk.X)
        StartButton.pack()


clicked = []
clicked2 = []


class Paricipant(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        global clicked
        global clicked2
        # self.dates1()
        # clicked=[]
        # clicked2=[]
        # self.showff()
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
        # SelectAttriutesPage["fg"] = "#3S93d49"
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

        self.Jan18_2020 = tk.Button(self.frame1, text="2020-01-18")
        self.Jan18_2020.config(command=lambda btn=self.Jan18_2020: self.showall(btn))
        self.Jan18_2020.grid(row=1, column=1, padx=10, pady=5)

        self.Jan19_2020 = tk.Button(self.frame1, text="2020-01-19")
        self.Jan19_2020.config(command=lambda btn=self.Jan19_2020: self.showall(btn))
        self.Jan19_2020.grid(row=2, column=1, padx=10, pady=5)

        self.Jan20_2020 = tk.Button(self.frame1, text="2020-01-20")
        self.Jan20_2020.config(command=lambda btn=self.Jan20_2020: self.parts(btn))
        self.Jan20_2020.grid(row=3, column=1, padx=10, pady=5)

        self.Jan21_2020 = tk.Button(self.frame1, text="2020-01-21")
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

    # def exist(self,widget):
    #     print("Checking for existence = ", bool(widget.winfo_exists()))
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
            # print("removing 311")
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
        # c,c2 = Paricipant.ttfd()
        clicked = clicked
        clicked2 = clicked2
        # Participaclicked
        print(clicked)
        date_t = clicked
        participant = (clicked2)
        de = "".join(date_t)
        pe = "".join(participant)
        de1 = ("r'/", de)
        # file = open("Dataset/"+de+"/"+pe+"/summary.csv")
        if (clicked and clicked2):
            file = open("Dataset/" + "".join(clicked) + "/" + "".join(clicked2) + "/summary.csv")
            # df = pd.read_csv('Dataset/20200121/310/summary.csv', skiprows=[1])

        else:
            file = open("Dataset/" + "20200118" + "/" + "310" + "/summary.csv")
        return file

        # return(file)


#        print("".join(date_t),"".join(participant))


class SelectDataAttributes(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        frame1 = Frame(self, highlightbackground="blue", highlightthickness=2)
        frame1.grid(padx=10, pady=50, row=0, column=0)  # pack(side=LEFT,fill=Y)
        label1 = tk.Label(frame1, text="Select Attribute(s)")
        ft1 = tkFont.Font(family='Times', size=14)
        label1["font"] = ft1
        label1["justify"] = "center"
        label1.grid(padx=10, pady=5, row=0, column=0)

        label2 = tk.Label(frame1, text="Query Operator(s)")
        ft1 = tkFont.Font(family='Times', size=14)
        label2["font"] = ft1
        label2["justify"] = "center"
        label2.grid(padx=10, pady=5, row=0, column=1)

        label3 = tk.Label(frame1, text="Input(s)")
        ft1 = tkFont.Font(family='Times', size=14)
        label3["font"] = ft1
        label3["justify"] = "center"
        label3.grid(padx=10, pady=5, row=0, column=2)

        MagnitudeAvg = tk.Button(
            frame1,
            text="Acc Magnitude Avg",
            #   command=lambda: controller.show_frame(Paricipant),
        )
        MagnitudeAvg["activebackground"] = "#1e90ff"
        MagnitudeAvg["bg"] = "#00ced1"
        ft3 = tkFont.Font(family='Times', size=20)
        MagnitudeAvg["font"] = ft3
        MagnitudeAvg["fg"] = "#393d49"
        MagnitudeAvg["justify"] = "center"
        MagnitudeAvg["text"] = "Acc Magnitude Avg"
        MagnitudeAvg["relief"] = "ridge"
        MagnitudeAvg.grid(padx=10, pady=5, row=1, column=0)

        mag_avg_operators = OptionMenu(frame1, StringVar(), "Null", ">", ">", "=")
        mag_avg_operators.grid(padx=10, pady=5, row=1, column=1)

        mag_avg_input = tk.Text(frame1, height=2, width=20)
        mag_avg_input.grid(padx=10, pady=5, row=1, column=2)

        EdaAvg = tk.Button(
            frame1,
            text="Eda Avg",
            #    command=lambda: controller.show_frame(Paricipant),
        )
        EdaAvg["activebackground"] = "#1e90ff"
        EdaAvg["bg"] = "#00ced1"
        ft3 = tkFont.Font(family='Times', size=20)
        EdaAvg["font"] = ft3
        EdaAvg["fg"] = "#393d49"
        EdaAvg["justify"] = "center"
        EdaAvg["text"] = "Eda Avg"
        EdaAvg["relief"] = "ridge"
        EdaAvg.grid(padx=10, pady=5, row=2, column=0)

        eda_avg_operators = OptionMenu(frame1, StringVar(), "Null", ">", ">", "=")
        eda_avg_operators.grid(padx=10, pady=5, row=2, column=1)

        eda_avg_input = tk.Text(frame1, height=2, width=20)
        eda_avg_input.grid(padx=10, pady=5, row=2, column=2)

        TempAvg = tk.Button(
            frame1,
            text="Temp Avg",
            #   command=lambda: controller.show_frame(Paricipant),
        )
        TempAvg["activebackground"] = "#1e90ff"
        TempAvg["bg"] = "#00ced1"
        ft3 = tkFont.Font(family='Times', size=20)
        TempAvg["font"] = ft3
        TempAvg["fg"] = "#393d49"
        TempAvg["justify"] = "center"
        TempAvg["text"] = "Temp Avg"
        TempAvg["relief"] = "ridge"
        TempAvg.grid(padx=10, pady=5, row=3, column=0)

        temp_avg_operators = OptionMenu(frame1, StringVar(), "Null", ">", ">", "=")
        temp_avg_operators.grid(padx=10, pady=5, row=3, column=1)

        temp_avg_input = tk.Text(frame1, height=2, width=20)
        temp_avg_input.grid(padx=10, pady=5, row=3, column=2)

        Movement = tk.Button(
            frame1,
            text="Movement",
            #   command=lambda: controller.show_frame(Paricipant),
        )
        Movement["activebackground"] = "#1e90ff"
        Movement["bg"] = "#00ced1"
        ft3 = tkFont.Font(family='Times', size=20)
        Movement["font"] = ft3
        Movement["fg"] = "#393d49"
        Movement["justify"] = "center"
        Movement["text"] = "Movement"
        Movement["relief"] = "ridge"
        Movement.grid(padx=10, pady=5, row=4, column=0)

        movement_operators = OptionMenu(frame1, StringVar(), "Null", ">", ">", "=")
        movement_operators.grid(padx=10, pady=5, row=4, column=1)

        movement_input = tk.Text(frame1, height=2, width=20)
        movement_input.grid(padx=10, pady=5, row=4, column=2)

        StepCount = tk.Button(
            frame1,
            text="Step Count",
            #   command=lambda: controller.show_frame(Paricipant),
        )
        StepCount["activebackground"] = "#1e90ff"
        StepCount["bg"] = "#00ced1"
        ft3 = tkFont.Font(family='Times', size=20)
        StepCount["font"] = ft3
        StepCount["fg"] = "#393d49"
        StepCount["justify"] = "center"
        StepCount["text"] = "Step Count"
        StepCount["relief"] = "ridge"
        StepCount.grid(padx=10, pady=5, row=5, column=0)

        step_operators = OptionMenu(frame1, StringVar(), "Null", ">", ">", "=")
        step_operators.grid(padx=10, pady=5, row=5, column=1)

        step_input = tk.Text(frame1, height=2, width=20)
        step_input.grid(padx=10, pady=5, row=5, column=2)

        Rest = tk.Button(
            frame1,
            text="Rest",
            # command=lambda: controller.show_frame(Paricipant),
        )
        Rest["activebackground"] = "#1e90ff"
        Rest["bg"] = "#00ced1"
        ft3 = tkFont.Font(family='Times', size=20)
        Rest["font"] = ft3
        Rest["fg"] = "#393d49"
        Rest["justify"] = "center"
        Rest["text"] = "Rest"
        Rest["relief"] = "ridge"
        Rest.grid(padx=10, pady=5, row=6, column=0)

        rest_operators = OptionMenu(frame1, StringVar(), "Null", ">", ">", "=")
        rest_operators.grid(padx=10, pady=5, row=6, column=1)

        rest_input = tk.Text(frame1, height=2, width=20)
        rest_input.grid(padx=10, pady=5, row=6, column=2, columnspan=4)

        # Rest = tk.Button(
        #     frame1,
        #     text="Rest",
        #     # command=lambda: controller.show_frame(Paricipant),
        # )

        convertTime = tk.Button(
            frame1,
            text="Local Time",
            command=update_button_value
        )

        convertTime["activebackground"] = "#1e90ff"
        convertTime["bg"] = "#00ced1"
        ft3 = tkFont.Font(family='Times', size=20)
        convertTime["font"] = ft3
        convertTime["fg"] = "#393d49"
        convertTime["justify"] = "center"
        convertTime["text"] = "Local Time"
        convertTime["relief"] = "ridge"
        convertTime.grid(padx=10, pady=5, row=7, column=0)

        # return self.d11,self.dpar

        ShowData = tk.Button(
            self,
            text="Show Data",
            command=lambda: (controller.show_frame(ShowGraph))
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


# -----------------------------------------------------------------------------------------------------------------------------------------ShowGraph
filename = ''
# df = pd.DataFrame()
# df = pd.read_csv(filename, skiprows=[1])
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

        # self.filename
        # global file
        print("been here:", clicked)

        # print(file)

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

        # convertTime = tk.Button(
        #     self,
        #     text="Show Data",
        #     command=update_button_value
        # )
        # convertTime["activebackground"] = "#9b60ad"
        # convertTime["bg"] = "#c71585"
        # ft3 = tkFont.Font(family='Times', size=20)
        # convertTime["font"] = ft3
        # convertTime["fg"] = "#393d49"
        # convertTime["justify"] = "center"
        # convertTime["text"] = "Convert Time"
        # convertTime["relief"] = "ridge"
        # convertTime.pack(side=BOTTOM, fill="x")  # .grid(row= 7,column=0,padx=1, pady=1, sticky=EW, columnspan=6)

    def showit(self):
        
        global filename
        global df
        global local_time
        try:
            self.scroll_y.pack_forget()
            self.canvas.get_tk_widget().pack_forget()
            self.toolbar.pack_forget()
            self.frame1.pack_forget()
        except AttributeError:
            pass

        self.frame1 = Frame(self, highlightbackground="blue", highlightthickness=2)
        self.frame1.pack(side=TOP)
        if not clicked:
            fw = Paricipant.g1234()
            # filename = open("Dataset"+date_t+participant+"/summary.csv")
            print("not clicked", fw)
            filename = fw
        else:
            fw = Paricipant.g1234()
            # filename = filename = Paricipant.g1234()
            print("it is clicked: file name:", fw.name)
            filename = fw.name
        if filename == '':
            df = pd.read_csv('Dataset/20200121/310/summary.csv', skiprows=[1])
        else:
            df = pd.read_csv(filename, skiprows=[1])
        print("this is global fn: ", filename)
        # return fw.name
        x = "Datetime (UTC)"

        row, cols = 7, 1
        fig, ax = plt.subplots(figsize=(7, 7), dpi=100, nrows=row, ncols=cols, sharex=True)
        fig.subplots_adjust(hspace=1, wspace=.5, bottom=.1, top=1)
        p1 = ax[0]
        p2 = ax[1]
        p3 = ax[2]
        p4 = ax[3]
        p5 = ax[4]
        p6 = ax[5]
        p7 = ax[6]
        fromx = 0
        tox1 = 1405
        # df = pd.read_csv(filename, skiprows=[1])
        df.iloc[fromx:tox1].plot(x, "Acc magnitude avg", ax=p1)
        df.iloc[fromx:tox1].plot(x, "Eda avg", ax=p2)
        df.iloc[fromx:tox1].plot(x, "Temp avg", ax=p3)
        df.iloc[fromx:tox1].plot(x, "Movement intensity", ax=p4)
        df.iloc[fromx:tox1].plot(x, "Steps count", ax=p5)
        df.iloc[fromx:tox1].plot(x, "Rest", ax=p6)
        if local_time:
            if df.loc[0, 'Timezone (minutes)'] == -300:
                plt.gca().xaxis.set_major_formatter(
                    mdates.DateFormatter("%b-%d %H:%M", pytz.timezone("America/New_York")))
            else:
                plt.gca().xaxis.set_major_formatter(
                    mdates.DateFormatter("%b-%d %H:%M", pytz.timezone("US/Central")))
        else:
            plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%b-%d %H:%M"))
        fig.tight_layout()
        self.canvas = FigureCanvasTkAgg(fig, master=self.frame1)
        # self.canvas[Scale]
        self.canvas.get_tk_widget().pack(side=LEFT)  # .grid(row= 1,column=0,padx=10, pady=5, sticky=N, columnspan=6)
        self.toolbar = NavigationToolbar2Tk(self.canvas, self)  # pack_toolbar=False)
        self.toolbar.pack(side=TOP)  # .grid(row= 0,column=0,padx=10, pady=5, sticky=N, columnspan=6)
        self.toolbar.update()
        self.scroll_y = tk.Scrollbar(self.frame1, orient="vertical", command=self.canvas.get_tk_widget().yview)
        self.scroll_y.pack(side=RIGHT, fill="both",
                           expand=True)  # grid(row= 0,column=6,padx=10, pady=10, sticky="ns", columnspan=6)
        # self.scroll_y.update()

        # need the below to display graph.
        # if self.canvas > 1:
        #     self.canvas.pack_forget()

    def graph(self):
        frame1 = Frame(self, highlightbackground="blue", highlightthickness=2)
        frame1["bg"] = "#00ced1"
        frame1.pack(side=LEFT)  # .grid(row=0,column=0)#pack(side=LEFT,fill=Y)
        global filename

        me1 = ["Home/Reset  ", "h or r or home"]
        me2 = ["Back  ", "c or left arrow or backspace"]
        me3 = ["Forward  ", "v or right arrow"]
        me4 = ["Pan/Zoom  ", " p"]
        me5 = ["Zoom-to-rect  ", " o"]
        me6 = ["Save  ", "  ctrl + s"]
        label = tk.Label(frame1, text=me1)
        # Place the label in the root window
        label["bg"] = "#00d17d"
        label.pack(anchor="w")
        label = tk.Label(frame1, text=me2)
        # Place the label in the root window
        label["bg"] = "#00ced1"
        label.pack(anchor="w")
        label = tk.Label(frame1, text=me3)
        # Place the label in the root window
        label["bg"] = "#00d17d"
        label.pack(anchor="w")
        label = tk.Label(frame1, text=me4)
        # Place the label in the root window
        label["bg"] = "#00ced1"
        label.pack(anchor="w")
        label = tk.Label(frame1, text=me5)
        # Place the label in the root window
        label["bg"] = "#00d17d"
        label.pack(anchor="w")
        label = tk.Label(frame1, text=me6)
        label["bg"] = "#00ced1"
        # Place the label in the root window
        label.pack(anchor="w")

        rcp = mpl.rcParams
        rcp['lines.linewidth'] = 2.0
        rcp['lines.markeredgewidth'] = 1.0
        rcp['axes.labelsize'] = 2
        rcp['font.size'] = 7
        rcp['patch.linewidth'] = .7
        rcp['figure.facecolor'] = '#c7d6ed'
        rcp['figure.edgecolor'] = '#c7d6ed'

        # rcp['toolbar']= True
        date_t = r'/20200118'
        participant = r'/310'

        bnt = tk.Button(self,
                        text="Show Selected Graph",
                        command=lambda: self.showit()
                        )
        bnt["activebackground"] = "#00ced1"
        bnt["bg"] = "#00ced1"
        ft2 = tkFont.Font(family='Times', size=20)
        bnt["font"] = ft2
        bnt["fg"] = "#393d49"
        bnt["justify"] = "center"
        # bnt["text"] = "Start"
        bnt["relief"] = "ridge"
        bnt.pack(side=TOP)  # .grid(row=0,column=0,sticky=NE)
        # pack(side=BOTTOM, fill='both', expand=True)

    # canvas.draw()

    # toolbar = NavigationToolbar2Tk(canvas, self)
    # toolbar.update()
    # canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)

    # Convert an input zulu (UTC) time string into something more readable. Returning it:
    # Didn't end up using this, but it may be helpful?
    def convertDate(zuluDate):
        input_format = '%Y-%m-%d %H%MZ'  # input example: 2020-01-17T23:48:00Z
        output_format = '%m-%d:%H%M'
        date = dt.strptime(zuluDate, input_format)  # convert String zuluDate into Datetime, format it
        return dt.strftime(date, output_format)  # convert back to String and return it


if __name__ == "__main__":
    testObj = windows()

    # testObj.geometry("1200x1200")
    #     testObj.rowconfigure(0, weight=1)
    #     testObj.columnconfigure(0, weight=1)
    # =======
    # testObj.geometry("1200x1200")
    testObj.mainloop()