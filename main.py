import PySimpleGUI as sg
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def generate_file_location(date, option):
    base_directory = 'Dataset'
    # Remove hyphens from the date string
    formatted_date = date.replace('-', '')
    file_location = f"{base_directory}/{formatted_date}/{option}/summary.csv"
    return file_location

def draw_figure(canvas, figure, loc=(0, 0)):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg

def plot_data(file_location):
    df = pd.read_csv(file_location)
    fig, axs = plt.subplots(4, 1, figsize=(6, 11))  # Adjust the size as needed

    # Example: Plotting four different columns, modify as per your CSV structure
    df.plot(x='Datetime (UTC)', y='Acc magnitude avg', ax=axs[0])
    df.plot(x='Datetime (UTC)', y='Eda avg', ax=axs[1])
    df.plot(x='Datetime (UTC)', y='Temp avg', ax=axs[2])
    df.plot(x='Datetime (UTC)', y='Movement intensity', ax=axs[3])

    return fig

def main():
    sg.theme('LightBlue2')
    
    layout = [
        [sg.Text('Welcome')],
        [
            sg.Combo(['2020-01-18', '2020-01-19', '2020-01-20', '2020-01-21'], key='-DATE-', default_value='2020-01-18'),
            sg.Combo(['310', '311', '312'], key='-OPTION-', default_value='310')
        ],
        [sg.Button('Select Data Attributes')],
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

            # Plotting data
            fig = plot_data(file_location)
            fig_agg = draw_figure(window['-CANVAS-'].TKCanvas, fig)

    window.close()

if __name__ == '__main__':
    main()
