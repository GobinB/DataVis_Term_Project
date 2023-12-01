import PySimpleGUI as sg
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.dates as mdates
from datetime import datetime
import os

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

# Function to validate date range
def is_valid_date_range(start_date, end_date):
    try:
        start = datetime.strptime(start_date, '%Y-%m-%d')
        end = datetime.strptime(end_date, '%Y-%m-%d')
        return start <= end
    except ValueError:
        return False

# Function to generate file locations for a date range
def generate_file_locations_for_range(start_date, end_date, option):
    start_datetime = datetime.strptime(start_date, '%Y-%m-%d')
    end_datetime = datetime.strptime(end_date, '%Y-%m-%d')
    date_range = pd.date_range(start_datetime, end_datetime, freq='D')
    
    file_locations = [f"{BASE_DIRECTORY}/{single_date.strftime('%Y%m%d')}/{option}/summary.csv" for single_date in date_range]
    return file_locations

# Function to draw matplotlib figure on PySimpleGUI Canvas
def draw_figure(canvas, figure, loc=(0, 0)):
    if hasattr(canvas, 'figure_agg'):
        canvas.figure_agg.get_tk_widget().forget()
        plt.close(canvas.figure_agg.figure)
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    canvas.figure_agg = figure_canvas_agg

# Updated plot_data function to handle a list of file locations
def plot_data(file_locations, columns, chart_type, timezone):
    all_dfs = []
    for file_location in file_locations:
        if os.path.exists(file_location):  # Check if the file exists
            df = pd.read_csv(file_location)
            df = convert_to_local_time(df, timezone)
            all_dfs.append(df)
    if not all_dfs:  # No data files found for the range
        sg.popup_error('No data found for the selected date range.')
        return None
    
    df = pd.concat(all_dfs, ignore_index=True)

    # Assuming you want to plot these attributes based on checkbox selections
    attributes_to_plot = [
        ('Acc magnitude avg', columns['-ACC-']),
        ('Eda avg', columns['-EDA-']),
        ('Temp avg', columns['-TEMP-']),
        ('Movement intensity', columns['-MOVEMENT-']),
        ('On Wrist', columns['-ON WRIST-']),

    ]

    # Count how many attributes are selected
    num_attributes = sum(1 for _, is_checked in attributes_to_plot if is_checked)

    if num_attributes == 0:
        return None  # No attributes selected, so no plot to create

    fig, axs = plt.subplots(num_attributes, 1, figsize=(15, 3 * num_attributes), sharex=True)

    if num_attributes == 1:
        axs = [axs]  # Make sure axs is always a list, even for a single subplot

    for ax, (attr, is_checked) in zip(axs, attributes_to_plot):
        if is_checked:
            ax.plot(df['Datetime (UTC)'], df[attr], label=attr)
            ax.set_ylabel(attr)
            ax.legend()

    for ax in axs:
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))

    fig.tight_layout()
    return fig

# Function to show statistics window
def show_statistics(df):
    stats = df.describe().T
    layout = [[sg.Text(str(stats))]]
    sg.Window('Statistics', layout, modal=True).read(close=True)

def main():
    sg.theme('LightBlue2')

    layout = [
        [sg.Text('Welcome')],
        [
            sg.Text('Start Date:'),
            sg.Input(key='-START DATE-', default_text='2020-01-18'),
            sg.Text('End Date:'),
            sg.Input(key='-END DATE-', default_text='2020-01-21'),
        ],
        [
            sg.Text('Select Option:'),
            sg.Combo(['310', '311', '312'], key='-OPTION-', default_value='310')
        ],
        [
            sg.Checkbox('Acc magnitude avg', key='-ACC-', default=True),
            sg.Checkbox('Eda avg', key='-EDA-', default=True),
            sg.Checkbox('Temp avg', key='-TEMP-', default=True),
            sg.Checkbox('Movement intensity', key='-MOVEMENT-', default=True),
            sg.Checkbox('On Wrist', key='-ON WRIST-')
        ],
        [
            sg.Text('Chart Type:'),
            sg.Combo(CHART_TYPES, key='-CHART TYPE-', default_value='plot')
        ],
        [
            sg.Text('Select Timezone:'),
            sg.Combo(TIMEZONES, default_value='UTC', key='-TIMEZONE-')
        ],
        [
            sg.Button('Show Graph'),
            sg.Button('Show Statistics')
        ],
        [sg.Canvas(key='-CANVAS-')]
    ]

    window = sg.Window('Data Analysis App', layout, finalize=True)

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break

        if event == 'Show Graph':
            start_date = values['-START DATE-']
            end_date = values['-END DATE-']
            if is_valid_date_range(start_date, end_date):
                selected_option = values['-OPTION-']
                file_locations = generate_file_locations_for_range(start_date, end_date, selected_option)
                fig = plot_data(file_locations, values, values['-CHART TYPE-'], values['-TIMEZONE-'])
                if fig:  # Check if a figure was returned
                    draw_figure(window['-CANVAS-'].TKCanvas, fig)
            else:
                sg.popup_error('Invalid Date Range', 'Please select a valid start and end date.')

        if event == 'Show Statistics':
            start_date = values['-START DATE-']
            end_date = values['-END DATE-']
            if is_valid_date_range(start_date, end_date):
                selected_option = values['-OPTION-']
                file_locations = generate_file_locations_for_range(start_date, end_date, selected_option)
                dfs = [pd.read_csv(file) for file in file_locations if os.path.exists(file)]
                if dfs:
                    df = pd.concat(dfs, ignore_index=True)
                    df = convert_to_local_time(df, values['-TIMEZONE-'])
                    show_statistics(df)
                else:
                    sg.popup_error('No data found for the selected date range.')

    window.close()

if __name__ == '__main__':
    main()
