import PySimpleGUI as sg
import pandas as pd
import matplotlib
import pytz
matplotlib.use("TkAgg")

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.dates as mdates
from datetime import datetime  # Add this import

import numpy as np
import math
from tkinter import ttk  


# Constants
BASE_DIRECTORY = 'Dataset'
BACKGROUND_COLOR = '#AAB6D3'
CHART_TYPES = ['plot', 'scatter', 'bar']
TIMEZONES = ['UTC', 'US/Eastern', 'Europe/London']  # Add more timezones as needed
selected_timezone = 'UTC'

# Function to convert UTC to local time

def convert_to_local_time(df, timezone):
    df['Datetime (UTC)'] = pd.to_datetime(df['Datetime (UTC)'])
    if timezone != 'UTC':
        selected_tz = pytz.timezone(timezone)
        df['Datetime (UTC)'] = df['Datetime (UTC)'].dt.tz_convert(selected_tz)
    return df

#fixing x axis labels 
def update_x_axis_labels(fig, timezone):
    for ax in fig.axes:
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))
        ax.xaxis.get_major_formatter().set_tzinfo(timezone)
        ax.figure.canvas.draw_idle()

        
def generate_file_location(date, option):
    base_directory = 'Dataset'
    formatted_date = date.replace('-', '')
    file_location = f"{base_directory}/{formatted_date}/{option}/summary.csv"
    return file_location


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
    widget = figure_canvas_agg.get_tk_widget()
    widget.pack(side='top', fill='both', expand=True)

    # Update idletasks before configuring the scrollregion
    widget.update_idletasks()

    # Calculate the figure size in pixels, which is needed for the scrollregion
    dpi = figure.get_dpi()
    fig_width, fig_height = figure.get_size_inches()
    scrollregion = (0, 0, fig_width * dpi, fig_height * dpi)

    # Set the scroll region to the size of the figure in pixels
    canvas.configure(scrollregion=scrollregion)

    # Create scrollbars and attach them to the figure canvas
    vscrollbar = ttk.Scrollbar(canvas, orient='vertical', command=widget.yview)
    vscrollbar.pack(side='right', fill='y')
    widget.configure(yscrollcommand=vscrollbar.set)

    hscrollbar = ttk.Scrollbar(canvas, orient='horizontal', command=widget.xview)
    hscrollbar.pack(side='bottom', fill='x')
    widget.configure(xscrollcommand=hscrollbar.set)

    canvas.figure_agg = figure_canvas_agg

def plot_data(file_location, columns, chart_type, timezone):
    try:
        df = pd.read_csv(file_location)
    except FileNotFoundError:
        print(f"File not found: {file_location}")
        return None

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

    fig, axs = plt.subplots(num_attributes, 1, figsize=(15, 3 * num_rows), sharex=False)

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

    # Update the DateFormatter for x-axis
    x_axis_format = mdates.DateFormatter('%Y-%m-%d %H:%M')
    for ax in fig.axes:
        ax.xaxis.set_major_formatter(x_axis_format)

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

    def convert_to_local_time(df, timezone):
        df['Datetime (UTC)'] = pd.to_datetime(df['Datetime (UTC)'])
        if timezone != 'UTC':
            selected_tz = pytz.timezone(timezone)
            df['Datetime (UTC)'] = df['Datetime (UTC)'].dt.tz_convert(selected_tz)
        return df


    def generate_file_location(self, date, option):
        formatted_date = date.replace('-', '')
        return f"{self.base_directory}/{formatted_date}/{option}/summary.csv"

    def load_data(self, file_location, timezone):
        df = pd.read_csv(file_location)
        return self.convert_to_local_time(df, timezone)

# Function to show statistics window
def show_statistics(df, timezone):   
    df = convert_to_local_time(df, timezone)    #ensuring statistics is correctly showing selcted time

    # Here, calculate statistical summaries
    stats_summary = df.describe()
    data_for_table = stats_summary.reset_index().values.tolist()
    headings = [''] + list(stats_summary.columns)

    layout = [
        [sg.Table(values=data_for_table, headings=headings, max_col_width=25,
                  auto_size_columns=True, display_row_numbers=True, justification='right', num_rows=10, key='-TABLE-',
                  row_height=35, tooltip='Statistical Summaries')],
    ]

    stats_window = sg.Window('Statistics Summary', layout, modal=True)

    while True:
        event, values = stats_window.read()
        if event == sg.WINDOW_CLOSED:
            break

    stats_window.close()

def show_raw_data(df, timezone): #ensuring time box is correctly showing selcted time
    df = convert_to_local_time(df, timezone)


    data_for_table = df.values.tolist()
    headings = list(df.columns)

    layout = [
        [sg.Table(values=data_for_table, headings=headings, max_col_width=35,
                  auto_size_columns=True, display_row_numbers=True, justification='right', num_rows=10, key='-RAW-TABLE-',
                  row_height=25, tooltip='Raw Data')],
    ]

    raw_data_window = sg.Window('Raw Data View', layout, modal=True)

    while True:
        event, values = raw_data_window.read()
        if event == sg.WINDOW_CLOSED:
            break

    raw_data_window.close()


def get_date_range(start_date, end_date):
    """Generate a list of dates between start_date and end_date."""
    start = pd.to_datetime(start_date)
    end = pd.to_datetime(end_date)
    date_range = pd.date_range(start, end)
    return date_range

def aggregate_data_from_range(start_date, end_date, selected_option, timezone):
    """Load and combine data from a range of dates."""
    date_range = get_date_range(start_date, end_date)
    data_frames = []
    for single_date in date_range:
        file_location = generate_file_location(single_date.strftime('%Y-%m-%d'), selected_option)
        try:
            df = pd.read_csv(file_location)
            df = convert_to_local_time(df, timezone)
            data_frames.append(df)
        except FileNotFoundError:
            print(f"No data found for {single_date.strftime('%Y-%m-%d')}")
    return pd.concat(data_frames) if data_frames else None

def zoom_axis(ax, zoom_factor):
    # Calculate the new x and y axis ranges based on the zoom factor
    x_min, x_max = ax.get_xlim()
    x_range = ((x_max - x_min) / 2) * zoom_factor
    y_min, y_max = ax.get_ylim()
    y_range = ((y_max - y_min) / 2) * zoom_factor

    # Set the new axis limits
    ax.set_xlim(x_min + x_range, x_max - x_range)
    ax.set_ylim(y_min + y_range, y_max - y_range)

def reset_zoom(ax, original_xlim, original_ylim):
    # Reset the axis limits to the original values
    ax.set_xlim(original_xlim)
    ax.set_ylim(original_ylim)

def update_x_axis_labels(fig, timezone):
    for ax in fig.axes:
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M', tz=timezone))
        ax.figure.canvas.draw_idle()

# Defining the panning functions
def pan_left(ax, pan_factor=0.1):
    x_min, x_max = ax.get_xlim()
    delta = (x_max - x_min) * pan_factor
    ax.set_xlim(x_min - delta, x_max - delta)

def pan_right(ax, pan_factor=0.1):
    x_min, x_max = ax.get_xlim()
    delta = (x_max - x_min) * pan_factor
    ax.set_xlim(x_min + delta, x_max + delta)

def main():
    sg.theme('LightBlue2')
    chart_types = ['plot', 'scatter', 'bar']
    date_combobox_choices = ['2020-01-18', '2020-01-19', '2020-01-20', '2020-01-21']
    option_combobox_choices = ['310', '311', '312']
    selected_timezone = 'US/Eastern'  
    df = None  # Initialize df as None

    # Initialize with a default value
    # selected_timezone_var = sg.StringVar(value=selected_timezone)

    layout = [
        [sg.Text('Welcome')],
        [
            sg.Checkbox('Enable Date Range', key='-ENABLERANGE-', enable_events=True),
        ],
        [
            sg.Text('Select Date:'),
            sg.Combo(date_combobox_choices, key='-DATE-', default_value='None'),
            sg.Text('Or Select Date Range:'),
            sg.Text('Start Date:'),
            sg.Input(key='-STARTDATE-', enable_events=True, size=(20,1)),
            sg.CalendarButton('Choose Start Date', target='-STARTDATE-', key='-STARTDATE-BTN-', format='%Y-%m-%d'),
            sg.Text('End Date:'),
            sg.Input(key='-ENDDATE-', enable_events=True, size=(20,1)),
            sg.CalendarButton('Choose End Date', target='-ENDDATE-', key='-ENDDATE-BTN-', format='%Y-%m-%d')
        ],
        [
            sg.Text('Select Option:'),
            sg.Combo(option_combobox_choices, key='-OPTION-', default_value='310')
        ],
        [
            sg.Checkbox('Acc magnitude avg', key='-ACC-', default=True),
            sg.Checkbox('Eda avg', key='-EDA-', default=True),
            sg.Checkbox('Temp avg', key='-TEMP-', default=True),
            sg.Checkbox('Movement intensity', key='-MOVEMENT-', default=True),
            sg.Checkbox('On Wrist', key='-ON WRIST-')
        ],
        [sg.Text('Chart Type:'), sg.Combo(chart_types, key='-CHART TYPE-', default_value='plot')],
        # [sg.Text('Select Timezone:'), sg.Combo(TIMEZONES, default_value='UTC', key='-TIMEZONE-')],
        # [sg.Text('Select Timezone:'), sg.Combo(TIMEZONES, default_value=selected_timezone, key='-TIMEZONE-', enable_events=True, readonly=True, textvariable=selected_timezone_var)],
        [sg.Text('Select Timezone:'), sg.Combo(TIMEZONES, default_value=selected_timezone, key='-TIMEZONE-', enable_events=True)],

        [sg.Button('Show Graph'), sg.Button('Show Statistics'), sg.Button('Open Time Box')], 
        [sg.Canvas(key='-CANVAS-')],
        [sg.Button('Pan Left'), sg.Button('Pan Right'), sg.Button('Zoom In'), sg.Button('Zoom Out'), sg.Button('Reset Zoom')]

    ]


    window = sg.Window('Data Analysis App', layout)
    current_timezone = 'sdd'  # Default time zone


    # Define initial zoom level and current axis limits
    original_xlim = None
    original_ylim = None
    zoom_level = 1.0
    fig = None

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break

        if event == '-ENABLERANGE-':
            enable_range = values['-ENABLERANGE-']
            window['-STARTDATE-'].update(disabled=not enable_range)
            window['-STARTDATE-BTN-'].update(disabled=not enable_range)
            window['-ENDDATE-'].update(disabled=not enable_range)
            window['-ENDDATE-BTN-'].update(disabled=not enable_range)
            window['-DATE-'].update(disabled=enable_range)
            

        if event == '-TIMEZONE-':
            selected_timezone = values['-TIMEZONE-']
            # selected_timezone_var.set(selected_timezone)  # Update the displayed timezone
            if df is not None:
                df = convert_to_local_time(df, selected_timezone)



        if event == 'Show Graph':
            selected_date = values['-DATE-']
            start_date = values['-STARTDATE-']
            end_date = values['-ENDDATE-']
            selected_option = values['-OPTION-']
            if df is not None:
                # Perform DataFrame operations on df
                df = convert_to_local_time(df, selected_timezone)
            

            if (selected_date or (start_date and end_date)) and selected_option:
                if start_date and end_date:
                    aggregated_data = aggregate_data_from_range(start_date, end_date, selected_option, selected_timezone)
                    if aggregated_data is not None:
                        fig = plot_data(generate_file_location(start_date, selected_option), values, values['-CHART TYPE-'], selected_timezone)
                        draw_figure(window['-CANVAS-'].TKCanvas, fig)
                    else:
                        sg.popup('No data available for the selected date range.')
               
                elif selected_date:
                    file_location = generate_file_location(selected_date, selected_option)
                    fig = plot_data(file_location, values, values['-CHART TYPE-'], selected_timezone)
                    if fig is not None:
                        draw_figure(window['-CANVAS-'].TKCanvas, fig)
                    else:
                        sg.popup(f'No data found for the selected date: {selected_date}')
                        
            # Display the selected timezone
            sg.popup(f'Selected Timezone: {selected_timezone}')
            if fig is not None:
                original_xlim = [ax.get_xlim() for ax in fig.axes]
                original_ylim = [ax.get_ylim() for ax in fig.axes]

        if fig is not None:
            if event == 'Pan Left':
                for ax in fig.axes:
                    pan_left(ax)
                fig.canvas.draw_idle()
            elif event == 'Pan Right':
                for ax in fig.axes:
                    pan_right(ax)
                fig.canvas.draw_idle()

        if event == 'Zoom In' and fig is not None:
            zoom_level *= 0.5  # Reduce zoom level for zooming in
            for ax in fig.axes:
                zoom_axis(ax, zoom_level)
            fig.canvas.draw_idle()

        if event == 'Zoom Out' and fig is not None:
            zoom_level *= 2  # Increase zoom level for zooming out
            for ax in fig.axes:
                zoom_axis(ax, zoom_level)
            fig.canvas.draw_idle()

        if event == 'Reset Zoom' and fig is not None and original_xlim is not None and original_ylim is not None:
            zoom_level = 1.0  # Reset zoom level
            for ax, orig_x, orig_y in zip(fig.axes, original_xlim, original_ylim):
                reset_zoom(ax, orig_x, orig_y)
            fig.canvas.draw_idle()


        if event == 'Show Statistics':
            selected_date = values['-DATE-']
            selected_option = values['-OPTION-']
            selected_timezone = values['-TIMEZONE-']

            if selected_date and selected_option:
                file_location = generate_file_location(selected_date, selected_option)
                try:
                    df = pd.read_csv(file_location)
                    show_statistics(df, selected_timezone)
                except FileNotFoundError:
                    sg.popup(f"No data found for {selected_date}")

        if event == 'Open Time Box':
            selected_date = values['-DATE-']
            selected_option = values['-OPTION-']
            selected_timezone = values['-TIMEZONE-']

            if selected_date and selected_option:
                file_location = generate_file_location(selected_date, selected_option)
                try:
                    df = pd.read_csv(file_location)
                    show_raw_data(df, selected_timezone)
                except FileNotFoundError:
                    sg.popup(f"No data found for {selected_date}")

    window.close()

if __name__ == '__main__':
    main()
