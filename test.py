import PySimpleGUI as sg
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Function to convert UTC to local time
def convert_to_local_time(df, timezone='America/New_York'):
    df['Datetime (UTC)'] = pd.to_datetime(df['Datetime (UTC)'])
    df = df.set_index('Datetime (UTC)')
    df.index = df.index.tz_convert(timezone)
    return df.reset_index()

def generate_file_location(date, option):
    base_directory = 'Dataset'
    formatted_date = date.replace('-', '')
    file_location = f"{base_directory}/{formatted_date}/{option}/summary.csv"
    return file_location

def draw_figure(canvas, figure, loc=(0, 0)):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg

def plot_data(file_location, columns):
    df = pd.read_csv(file_location)
    df = convert_to_local_time(df)  # Convert UTC to local time

    background_color = '#AAB6D3'
    fig, axs = plt.subplots(2, 2, figsize=(10, 8), facecolor=background_color, sharex=True)

    for ax in axs.flat:
        ax.set_facecolor(background_color)
        ax.tick_params(colors='black')

    if columns['-ACC-']:
        df.plot(x='Datetime (UTC)', y='Acc magnitude avg', ax=axs[0, 0])
    if columns['-EDA-']:
        df.plot(x='Datetime (UTC)', y='Eda avg', ax=axs[0, 1])
    if columns['-TEMP-']:
        df.plot(x='Datetime (UTC)', y='Temp avg', ax=axs[1, 0])
    if columns['-MOVEMENT-']:
        df.plot(x='Datetime (UTC)', y='Movement intensity', ax=axs[1, 1])

    return fig

def main():
    sg.theme('LightBlue2')

    layout = [
        [sg.Text('Welcome')],
        [
            sg.Combo(['2020-01-18', '2020-01-19', '2020-01-20', '2020-01-21'], key='-DATE-', default_value='2020-01-18'),
            sg.Combo(['310', '311', '312'], key='-OPTION-', default_value='310')
        ],
        [sg.Checkbox('Acc magnitude avg', key='-ACC-', default=True),
         sg.Checkbox('Eda avg', key='-EDA-', default=True),
         sg.Checkbox('Temp avg', key='-TEMP-', default=True),
         sg.Checkbox('Movement intensity', key='-MOVEMENT-', default=True)],
        [sg.Button('Show Graph')],
        [sg.Column([[sg.Canvas(key='-CANVAS-')]])]
    ]

    window = sg.Window('Data Analysis App', layout)

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break
        elif event == 'Show Graph':
            selected_date = values['-DATE-']
            selected_option = values['-OPTION-']
            file_location = generate_file_location(selected_date, selected_option)

            fig = plot_data(file_location, values)
            fig_agg = draw_figure(window['-CANVAS-'].TKCanvas, fig)

    window.close()

if __name__ == '__main__':
    main()