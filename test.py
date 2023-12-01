import PySimpleGUI as sg
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.dates as mdates
from datetime import datetime as dt

# Function to convert UTC to local time
def convert_to_local_time(df, timezone='UTC'):
    df['Datetime (UTC)'] = pd.to_datetime(df['Datetime (UTC)'])
    df = df.set_index('Datetime (UTC)')
    if timezone != 'UTC':
        df.index = df.index.tz_convert(timezone)
    return df.reset_index()

def draw_figure(canvas, figure, loc=(0, 0)):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg

def plot_data(file_location, columns, timezone, start_date, end_date):
    df = pd.read_csv(file_location)
    df = convert_to_local_time(df, timezone)
    df = df[(df['Datetime (UTC)'] >= start_date) & (df['Datetime (UTC)'] <= end_date)]
    
    background_color = '#AAB6D3'
    fig, axs = plt.subplots(2, 2, figsize=(10, 8), facecolor=background_color, sharex=True)

    for ax in axs.flat:
        ax.set_facecolor(background_color)
        ax.tick_params(colors='black')
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))

    if columns['-ACC-']:
        axs[0, 0].plot(df['Datetime (UTC)'], df['Acc magnitude avg'], label='Acc magnitude avg')
    if columns['-EDA-']:
        axs[0, 1].plot(df['Datetime (UTC)'], df['Eda avg'], label='Eda avg')
    if columns['-TEMP-']:
        axs[1, 0].plot(df['Datetime (UTC)'], df['Temp avg'], label='Temp avg')
    if columns['-MOVEMENT-']:
        axs[1, 1].plot(df['Datetime (UTC)'], df['Movement intensity'], label='Movement intensity')

    for ax in axs.flat:
        ax.legend()

    return fig

def main():
    sg.theme('LightBlue2')

    layout = [
        [sg.Text('Welcome')],
        [
            sg.Text('Start Date:'), sg.Input(key='-START-', size=(10, 1), default_text='2020-01-18'),
            sg.CalendarButton('Pick Start Date', target='-START-', key='-START DATE-', format='%Y-%m-%d'),
            sg.Text('End Date:'), sg.Input(key='-END-', size=(10, 1), default_text='2020-01-21'),
            sg.CalendarButton('Pick End Date', target='-END-', key='-END DATE-', format='%Y-%m-%d')
        ],
        [
            sg.Checkbox('Acc magnitude avg', key='-ACC-', default=True),
            sg.Checkbox('Eda avg', key='-EDA-', default=True),
            sg.Checkbox('Temp avg', key='-TEMP-', default=True),
            sg.Checkbox('Movement intensity', key='-MOVEMENT-', default=True)
        ],
        [sg.Button('Show Graph'), sg.Button('UTC'), sg.Button('Local')],
        [sg.Column([[sg.Canvas(key='-CANVAS-')]])]
    ]

    window = sg.Window('Data Analysis App', layout, finalize=True)
    current_timezone = 'UTC'  # Default time zone
    fig_agg = None

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break
        elif event == 'Show Graph':
            if fig_agg:
                # Remove the previous plot
                plt.close('all')
                fig_agg.get_tk_widget().forget()
                fig_agg = None
            
            selected_option = 'summary'  # Assuming summary.csv is the file to be used
            start_date = dt.strptime(values['-START-'], '%Y-%m-%d')
            end_date = dt.strptime(values['-END-'], '%Y-%m-%d')
            file_location = f"Dataset/{selected_option}.csv"  # Update this path as required
            
            fig = plot_data(file_location, values, current_timezone, start_date, end_date)
            fig_agg = draw_figure(window['-CANVAS-'].TKCanvas, fig)
        elif event == 'UTC':
            current_timezone = 'UTC'
        elif event == 'Local':
            current_timezone = 'America/New_York'  # Modify as needed

    window.close()

if __name__ == '__main__':
    main()
