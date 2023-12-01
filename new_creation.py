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

def generate_file_location(date, option):
    base_directory = 'Dataset'
    formatted_date = date.replace('-', '')
    file_location = f"{base_directory}/{formatted_date}/{option}/summary.csv"
    return file_location

def draw_figure(canvas, figure, loc=(0, 0)):
    if hasattr(canvas, 'figure_agg'):
        canvas.figure_agg.get_tk_widget().forget()
        plt.close(canvas.figure_agg.figure)
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    canvas.figure_agg = figure_canvas_agg

def plot_data(file_location, columns, chart_type, timezone):
    df = pd.read_csv(file_location)
    df = convert_to_local_time(df, timezone)

    background_color = '#AAB6D3'
    fig, axs = plt.subplots(2, 2, figsize=(15, 3), facecolor=background_color, sharex=True)

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
    date_radios = [
        [sg.Radio('2020-01-18', "DATES", key='2020-01-18', default=True)],
        [sg.Radio('2020-01-19', "DATES", key='2020-01-19')],
        [sg.Radio('2020-01-20', "DATES", key='2020-01-20')],
        [sg.Radio('2020-01-21', "DATES", key='2020-01-21')]
    ]

    option_radios = [
        [sg.Radio('310', "OPTIONS", key='310', default=True)],
        [sg.Radio('311', "OPTIONS", key='311')],
        [sg.Radio('312', "OPTIONS", key='312')]
    ]

    layout = [
        [sg.Text('Welcome')],
        [sg.Frame('Select Dates', date_radios)],
        [sg.Frame('Select Options', option_radios)],
        [
            sg.Checkbox('Acc magnitude avg', key='-ACC-', default=True),
            sg.Checkbox('Eda avg', key='-EDA-', default=True),
            sg.Checkbox('Temp avg', key='-TEMP-', default=True),
            sg.Checkbox('Movement intensity', key='-MOVEMENT-', default=True)
        ],
        [sg.Text('Chart Type:'), sg.Combo(chart_types, key='-CHART TYPE-', default_value='plot')],
        [sg.Button('Show Graph')],
        [sg.Canvas(key='-CANVAS-')]
    ]

    window = sg.Window('Data Analysis App', layout)
    current_timezone = 'UTC'  # Default time zone

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break

        # Disable the '311' option for specific dates
        if values['2020-01-20'] or values['2020-01-21']:
            window['311'].update(disabled=True)
        else:
            window['311'].update(disabled=False)

        if event == 'Show Graph':  # Changed from elif to if
            selected_date = next((key for key, value in values.items() if value and key.startswith('2020')), None)
            selected_option = next((key for key, value in values.items() if value and key.isdigit()), None)

            if selected_date and selected_option:
                file_location = generate_file_location(selected_date, selected_option)
                fig = plot_data(file_location, values, values['-CHART TYPE-'], current_timezone)
                draw_figure(window['-CANVAS-'].TKCanvas, fig)

    window.close()

if __name__ == '__main__':
    main()
