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
    # Convert the descriptive statistics into a list of lists, suitable for the Table Element
    data_for_table = df.describe().reset_index().values.tolist()
    headings = [''] + list(df.describe().columns)  # Add an empty string for the index column header

    # Define the layout for the new window
    layout = [
        [sg.Table(values=data_for_table, headings=headings, max_col_width=25,
                  auto_size_columns=True, display_row_numbers=True, justification='right', num_rows=10, key='-TABLE-',
                  row_height=35, tooltip='This is a table')],
    ]

    # Create a new window to display the statistics
    stats_window = sg.Window('Time Box', layout, modal=True)

    # Event loop for the new window
    while True:
        event, values = stats_window.read()
        if event == sg.WINDOW_CLOSED:
            break

    stats_window.close()


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




def main():
    sg.theme('LightBlue2')
    chart_types = ['plot', 'scatter', 'bar']
    date_combobox_choices = ['2020-01-18', '2020-01-19', '2020-01-20', '2020-01-21']
    option_combobox_choices = ['310', '311', '312']

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
        [sg.Text('Select Timezone:'), sg.Combo(TIMEZONES, default_value='UTC', key='-TIMEZONE-')],
        [sg.Button('Show Graph'), sg.Button('Show Statistics'), sg.Button('Open Time Box')], 
        [sg.Canvas(key='-CANVAS-')],
        [sg.Button('Zoom In'), sg.Button('Zoom Out'), sg.Button('Reset Zoom')]

    ]


    window = sg.Window('Data Analysis App', layout)
    current_timezone = 'UTC'  # Default time zone

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

        if event == 'Show Graph':
            selected_date = values['-DATE-']
            start_date = values['-STARTDATE-']
            end_date = values['-ENDDATE-']
            selected_option = values['-OPTION-']

            if (selected_date or (start_date and end_date)) and selected_option:
                if start_date and end_date:
                    aggregated_data = aggregate_data_from_range(start_date, end_date, selected_option, current_timezone)
                    if aggregated_data is not None:
                        fig = plot_data(generate_file_location(start_date, selected_option), values, values['-CHART TYPE-'], current_timezone)
                        draw_figure(window['-CANVAS-'].TKCanvas, fig)
                    else:
                        sg.popup('No data available for the selected date range.')
                elif selected_date:
                    file_location = generate_file_location(selected_date, selected_option)
                    fig = plot_data(file_location, values, values['-CHART TYPE-'], current_timezone)
                    if fig is not None:
                        draw_figure(window['-CANVAS-'].TKCanvas, fig)
                    else:
                        sg.popup(f'No data found for the selected date: {selected_date}')

            if fig is not None:
                original_xlim = [ax.get_xlim() for ax in fig.axes]
                original_ylim = [ax.get_ylim() for ax in fig.axes]

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

            if selected_date and selected_option:
                file_location = generate_file_location(selected_date, selected_option)
                df = pd.read_csv(file_location)
                df = convert_to_local_time(df, values['-TIMEZONE-'])  # Convert to selected timezone
                show_statistics(df)


        if event == 'Open Time Box':
            selected_date = values['-DATE-']
            selected_option = values['-OPTION-']

            if selected_date and selected_option:
                file_location = generate_file_location(selected_date, selected_option)
                try:
                    df = pd.read_csv(file_location)
                    df = convert_to_local_time(df, values['-TIMEZONE-'])
                    show_statistics(df)  # This function will show the statistics in a table format as a separate window
                except FileNotFoundError:
                    sg.popup(f"No data found for the selected date: {selected_date}")

    window.close()

if __name__ == '__main__':
    main()
