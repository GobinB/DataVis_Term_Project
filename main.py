import PySimpleGUI as sg
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

color1 = '#AAB6D3'

def generate_file_location(date, option):
    base_directory = 'Dataset'
    formatted_date = date.replace('-', '')
    file_location = f"{base_directory}/{formatted_date}/{option}/summary.csv"
    return file_location

def draw_figure(canvas, figure, loc=(0, 0), figure_canvas_agg=None):
    if figure_canvas_agg is not None:
        figure_canvas_agg.get_tk_widget().forget()
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg

def plot_data(file_location):
    df = pd.read_csv(file_location)
    background_color = color1
    fig, axs = plt.subplots(2, 2, figsize=(14, 4), facecolor=background_color)

    for ax in axs.flat:
        ax.set_facecolor(background_color)
        ax.tick_params(colors='black')

    df.plot(x='Datetime (UTC)', y='Acc magnitude avg', ax=axs[0, 0])
    df.plot(x='Datetime (UTC)', y='Eda avg', ax=axs[0, 1])
    df.plot(x='Datetime (UTC)', y='Temp avg', ax=axs[1, 0])
    df.plot(x='Datetime (UTC)', y='Movement intensity', ax=axs[1, 1])

    return fig

def main():
    sg.theme('LightBlue2')

    # Using Radio buttons instead of Checkboxes for exclusive selection
    date_radios = [[sg.Radio('2020-01-18', "DATES", key='2020-01-18', default=True)],
                   [sg.Radio('2020-01-19', "DATES", key='2020-01-19')],
                   [sg.Radio('2020-01-20', "DATES", key='2020-01-20')],
                   [sg.Radio('2020-01-21', "DATES", key='2020-01-21')]]
    
    option_radios = [[sg.Radio('310', "OPTIONS", key='310', default=True)],
                     [sg.Radio('311', "OPTIONS", key='311')],
                     [sg.Radio('312', "OPTIONS", key='312')]]
              

    layout = [
        [sg.Text('Welcome')],
        [sg.Frame('Select Dates', date_radios)],
        [sg.Frame('Select Options', option_radios)],
        [sg.Frame('attributes'.attribute_radios )]
        [sg.Button('Show Graph')],
        [sg.Column([[sg.Canvas(key='-CANVAS-')]])]
    ]

    window = sg.Window('Data Analysis App', layout)
    
    fig_agg = None

    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED:
            break

        # If Radio buttons are used, no need for the additional logic to manage exclusivity

        if event == 'Show Graph':
            selected_date = next((key for key, value in values.items() if value and key.startswith('2020')), None)
            selected_option = next((key for key, value in values.items() if value and key.isdigit()), None)

            if selected_date and selected_option:
                file_location = generate_file_location(selected_date, selected_option)
                fig = plot_data(file_location)
                fig_agg = draw_figure(window['-CANVAS-'].TKCanvas, fig, loc=(0, 0), figure_canvas_agg=fig_agg)

    window.close()

if __name__ == '__main__':
    main()

