import PySimpleGUI as sg
import pandas as pd
import matplotlib
matplotlib.use("TkAgg")

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.dates as mdates
import numpy as np
import math
from tkinter import ttk  


# Constants
BASE_DIRECTORY = 'Dataset'
BACKGROUND_COLOR = '#AAB6D3'
CHART_TYPES = ['plot', 'scatter', 'bar']
TIMEZONES = ['UTC', 'US/Eastern', 'Europe/London']  # Add more timezones as needed

# Function to convert UTC to local time
def convert_to_local_time(df, timezone='UTC'):
    df['Datetime (UTC)'] = pd.to_datetime(df['Datetime (UTC)'])
    df = df.set_index('Datetime (UTC)')
    if timezone != 'UTC':
        df.index = df.index.tz_convert(timezone)
    return df.reset_index()

def generate_file_location(date, option):
    base_directory = 'Dataset'
    formatted_date = date.replace('-', '')
    file_location = f"{base_directory}/{formatted_date}/{option}/summary.csv"
    return file_location

def draw_figure(canvas, figure, loc=(0, 0)):
    if hasattr(canvas, 'figure_agg'):
        canvas.figure_agg.get_tk_widget().forget()
        plt.close(canvas.figure_agg.figure)
        # Remove the old scrollbar
        for child in canvas.winfo_children():
            if isinstance(child, ttk.Scrollbar):
                child.destroy()

    # Create a FigureCanvasTkAgg object
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
def draw_figure(canvas, figure, loc=(0, 0)):
    if hasattr(canvas, 'figure_agg'):
        canvas.figure_agg.get_tk_widget().forget()
        plt.close(canvas.figure_agg.figure)
        # Remove the old scrollbars
        for child in canvas.winfo_children():
            if isinstance(child, ttk.Scrollbar):
                child.destroy()

    # Create a FigureCanvasTkAgg object
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()

    # Pack the FigureCanvasTkAgg widget to fill both the X and Y axes
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)

    # Create vertical scrollbar and attach it to the canvas
    vscrollbar = ttk.Scrollbar(canvas, orient='vertical', command=canvas.yview)
    vscrollbar.pack(side='right', fill='y')
    canvas.configure(yscrollcommand=vscrollbar.set)

    # Create horizontal scrollbar and attach it to the canvas
    hscrollbar = ttk.Scrollbar(canvas, orient='horizontal', command=canvas.xview)
    hscrollbar.pack(side='bottom', fill='x')
    canvas.configure(xscrollcommand=hscrollbar.set)

    # Set the canvas scrolling region
    canvas.config(scrollregion=canvas.bbox("all"))

    canvas.figure_agg = figure_canvas_agg

def plot_data(file_location, columns, chart_type, timezone):
    df = pd.read_csv(file_location)
    df = convert_to_local_time(df, timezone)

    # Assuming you want to plot these attributes based on checkbox selections
    attributes_to_plot = [
        ('Acc magnitude avg', columns['-ACC-']),
        ('Eda avg', columns['-EDA-']),
        ('Temp avg', columns['-TEMP-']),
        ('Movement intensity', columns['-MOVEMENT-']),
        ('On Wrist', columns['-ON WRIST-']),
    ]

    num_attributes = sum(1 for _, is_checked in attributes_to_plot if is_checked)

    if num_attributes == 0:
        return None  # No attributes selected, so no plot to create

    # Calculate the number of rows and columns for the subplots
    num_rows = int(math.ceil(num_attributes / 2))
    num_cols = min(2, num_attributes)

    fig, axs = plt.subplots(num_attributes, 1, figsize=(15, 3 * num_rows), sharex=True)

    if num_attributes == 1:
        axs = np.array([axs])  # Make sure axs is always a numpy array, even for a single subplot

    current_subplot = 0  # Track the current subplot index

    for i, (attr, is_checked) in enumerate(attributes_to_plot):
        if is_checked:
            ax = axs[current_subplot]
            current_subplot += 1

            if chart_type == 'plot':
                ax.plot(df['Datetime (UTC)'], df[attr], label=attr)
            elif chart_type == 'scatter':
                ax.scatter(df['Datetime (UTC)'], df[attr], label=attr)
            elif chart_type == 'bar':
                ax.bar(df['Datetime (UTC)'], df[attr], label=attr)

            ax.set_ylabel(attr)
            ax.legend()

    for ax in axs:
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))

    # Remove unused subplots
    for i in range(current_subplot, num_attributes):
        fig.delaxes(axs[i])

    fig.tight_layout()
    return fig

# Data Handling Class
class DataHandler:
    def __init__(self, base_directory=BASE_DIRECTORY):
        self.base_directory = base_directory

    def convert_to_local_time(self, df, timezone='UTC'):
        df['Datetime (UTC)'] = pd.to_datetime(df['Datetime (UTC)'])
        df = df.set_index('Datetime (UTC)')
        if timezone != 'UTC':
            df.index = df.index.tz_convert(timezone)
        return df.reset_index()

    def generate_file_location(self, date, option):
        formatted_date = date.replace('-', '')
        return f"{self.base_directory}/{formatted_date}/{option}/summary.csv"

    def load_data(self, file_location, timezone):
        df = pd.read_csv(file_location)
        return self.convert_to_local_time(df, timezone)

# Function to show statistics window
def show_statistics(df):
    stats = df.describe().T
    layout = [[sg.Text(str(stats))]]
    sg.Window('Statistics', layout, modal=True).read(close=True)


def main():
    sg.theme('LightBlue2')
    chart_types = ['plot', 'scatter', 'bar']
    date_combobox_choices = ['2020-01-18', '2020-01-19', '2020-01-20', '2020-01-21']
    option_combobox_choices = ['310', '311', '312']

    layout = [
        [sg.Text('Welcome')],
        [
            sg.Text('Select Date:'),
            sg.Combo(date_combobox_choices, key='-DATE-', default_value='None')
        ],
        [
            sg.Text('Select Option:'),
            sg.Combo(option_combobox_choices, key='-OPTION-', default_value='310')
        ],  # Modified to use a combo box for selecting options
        [
            sg.Checkbox('Acc magnitude avg', key='-ACC-', default=True),
            sg.Checkbox('Eda avg', key='-EDA-', default=True),
            sg.Checkbox('Temp avg', key='-TEMP-', default=True),
            sg.Checkbox('Movement intensity', key='-MOVEMENT-', default=True),
            sg.Checkbox('On Wrist', key='-ON WRIST-')  # Adding checkbox for On Wrist data
        ],
        [sg.Text('Chart Type:'), sg.Combo(chart_types, key='-CHART TYPE-', default_value='plot')],
        [sg.Text('Select Timezone:'), sg.Combo(TIMEZONES, default_value='UTC', key='-TIMEZONE-')],  # Added timezone selection
        [sg.Button('Show Graph'), sg.Button('Show Statistics')],  # Added Show Statistics button
        [sg.Canvas(key='-CANVAS-')]
    ]

    window = sg.Window('Data Analysis App', layout)
    current_timezone = 'UTC'  # Default time zone

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break

        if event == 'Show Graph':
            selected_date = values['-DATE-']
            selected_option = values['-OPTION-']

            if selected_date and selected_option:
                file_location = generate_file_location(selected_date, selected_option)
                fig = plot_data(file_location, values, values['-CHART TYPE-'], current_timezone)
                draw_figure(window['-CANVAS-'].TKCanvas, fig)

        if event == 'Show Statistics':
            selected_date = values['-DATE-']
            selected_option = values['-OPTION-']

            if selected_date and selected_option:
                file_location = generate_file_location(selected_date, selected_option)
                df = pd.read_csv(file_location)
                df = convert_to_local_time(df, values['-TIMEZONE-'])  # Convert to selected timezone
                show_statistics(df)

    window.close()

if __name__ == '__main__':
    main()
