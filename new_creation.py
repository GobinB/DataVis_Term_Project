import PySimpleGUI as sg
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.dates as mdates
import numpy as np

# Function to convert UTC to local time
def convert_to_local_time(df, timezone='UTC'):
    df['Datetime (UTC)'] = pd.to_datetime(df['Datetime (UTC)'])
    df = df.set_index('Datetime (UTC)')
    if timezone != 'UTC':
        df.index = df.index.tz_convert(timezone)
    return df.reset_index()

def generate_file_location(date, participant, option):
    base_directory = 'Dataset'
    formatted_date = date.replace('-', '')
    file_location = f"{base_directory}/{formatted_date}/{participant}/{option}/summary.csv"
    return file_location

def draw_figure(canvas, figure, loc=(0, 0)):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg

def plot_data(file_location, columns, chart_type, timezone):
    df = pd.read_csv(file_location)
    df = convert_to_local_time(df, timezone)

    background_color = '#AAB6D3'
    fig, axs = plt.subplots(2, 2, figsize=(10, 8), facecolor=background_color, sharex=True)

    for ax in axs.flat:
        ax.set_facecolor(background_color)
        ax.tick_params(colors='black')
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))

    plot_func = getattr(axs[0, 0], chart_type)

    if columns['-ACC-']:
        plot_func(df['Datetime (UTC)'], df['Acc magnitude avg'], label='Acc magnitude avg')
    if columns['-EDA-']:
        plot_func(df['Datetime (UTC)'], df['Eda avg'], label='Eda avg')
    if columns['-TEMP-']:
        plot_func(df['Datetime (UTC)'], df['Temp avg'], label='Temp avg')
    if columns['-MOVEMENT-']:
        plot_func(df['Datetime (UTC)'], df['Movement intensity'], label='Movement intensity')

    for ax in axs.flat:
        ax.legend()

    return fig

def main():
    sg.theme('LightBlue2')
    chart_types = ['plot', 'scatter', 'bar']

    layout = [
        [sg.Text('Welcome')],
        [
            sg.Combo(['2020-01-18', '2020-01-19', '2020-01-20', '2020-01-21'], key='-DATE-', default_value='2020-01-18'),
            sg.Combo(['Participant 1', 'Participant 2', 'Participant 3'], key='-PARTICIPANT-', default_value='Participant 1'),
            sg.Combo(['310', '311', '312'], key='-OPTION-', default_value='310')
        ],
        [
            sg.Checkbox('Acc magnitude avg', key='-ACC-', default=True),
            sg.Checkbox('Eda avg', key='-EDA-', default=True),
            sg.Checkbox('Temp avg', key='-TEMP-', default=True),
            sg.Checkbox('Movement intensity', key='-MOVEMENT-', default=True)
        ],
        [sg.Text('Chart Type:'), sg.Combo(chart_types, key='-CHART TYPE-', default_value='plot')],
        [sg.Button('Show Graph'), sg.Button('UTC'), sg.Button('Local')],
        [sg.Slider(range=(0, 100), orientation='h', size=(34, 20), key='-TIME SLIDER-')],
        [sg.Column([[sg.Canvas(key='-CANVAS-')]])]
    ]

    window = sg.Window('Data Analysis App', layout)
    current_timezone = 'UTC'  # Default time zone

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break
        elif event == 'Show Graph':
            selected_date = values['-DATE-']
            selected_participant = values['-PARTICIPANT-']
            selected_option = values['-OPTION-']
            chart_type = values['-CHART TYPE-']

            file_location = generate_file_location(selected_date, selected_participant, selected_option)
            fig = plot_data(file_location, values, chart_type, current_timezone)
            fig_agg = draw_figure(window['-CANVAS-'].TKCanvas, fig)
        elif event == 'UTC':
            current_timezone = 'UTC'
        elif event == 'Local':
            current_timezone = 'America/New_York'  # Modify as needed

    window.close()

if __name__ == '__main__':
    main()
