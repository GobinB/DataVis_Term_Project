import PySimpleGUI as sg
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.dates as mdates

# Constants
BASE_DIRECTORY = 'Dataset'
BACKGROUND_COLOR = '#AAB6D3'
CHART_TYPES = ['plot', 'scatter', 'bar']
TIMEZONES = ['UTC', 'US/Eastern', 'Europe/London']  # Add more timezones as needed

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

# Function to draw a Matplotlib figure on a canvas
def draw_figure(canvas, figure):
    if hasattr(canvas, 'figure_agg'):
        canvas.figure_agg.get_tk_widget().forget()
        plt.close(canvas.figure_agg.figure)
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    canvas.figure_agg = figure_canvas_agg

# Function to plot data
def plot_data(handler, file_location, columns, chart_type, timezone):
    df = handler.load_data(file_location, timezone)

    fig, axs = plt.subplots(2, 2, figsize=(15, 3), facecolor=BACKGROUND_COLOR, sharex=True)
    for ax in axs.flat:
        ax.set_facecolor(BACKGROUND_COLOR)
        ax.tick_params(colors='black')
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))

    plot_func = getattr(axs[0, 0], chart_type)

    for sensor, ax in zip(columns, axs.flat):
        if columns[sensor]:
            ax.plot(df['Datetime (UTC)'], df[sensor], label=sensor)

    for ax in axs.flat:
        ax.legend()

    return fig

# Function to show statistics window
def show_statistics(df):
    stats = df.describe().T
    layout = [[sg.Text(str(stats))]]
    sg.Window('Statistics', layout, modal=True).read(close=True)

# Main function
def main():
    sg.theme('LightBlue2')
    data_handler = DataHandler()

    # UI layout
    layout = [
        [sg.Text('Welcome to Data Analysis App')],
        [sg.Text('Select Date:'), sg.Combo(['2020-01-18', '2020-01-19', '2020-01-20', '2020-01-21'], key='-DATE-')],
        [sg.Text('Select Option:'), sg.Combo(['310', '311', '312'], key='-OPTION-')],
        [sg.Text('Select Timezone:'), sg.Combo(TIMEZONES, default_value='UTC', key='-TIMEZONE-')],
        [sg.Frame('Data Columns:', [[sg.Checkbox('Acc magnitude avg', key='-ACC-', default=True),
                                     sg.Checkbox('Eda avg', key='-EDA-'),
                                     sg.Checkbox('Temp avg', key='-TEMP-'),
                                     sg.Checkbox('Movement intensity', key='-MOVEMENT-'),
                                     sg.Checkbox('On Wrist', key='-ON WRIST-')]], size=(300, 150))],
        [sg.Text('Chart Type:'), sg.Combo(CHART_TYPES, key='-CHART TYPE-', default_value='plot')],
        [sg.Button('Show Graph'), sg.Button('Show Statistics')],
        [sg.Canvas(key='-CANVAS-')]
    ]

    window = sg.Window('Data Analysis App', layout)

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break

        if event == 'Show Graph':
            selected_date = values['-DATE-']
            selected_option = values['-OPTION-']
            timezone = values['-TIMEZONE-']
            if selected_date and selected_option:
                file_location = data_handler.generate_file_location(selected_date, selected_option)
                fig = plot_data(data_handler, file_location, values, values['-CHART TYPE-'], timezone)
                draw_figure(window['-CANVAS-'].TKCanvas, fig)

        if event == 'Show Statistics':
            selected_date = values['-DATE-']
            selected_option = values['-OPTION-']
            if selected_date and selected_option:
                file_location = data_handler.generate_file_location(selected_date, selected_option)
                df = data_handler.load_data(file_location, values['-TIMEZONE-'])
                show_statistics(df)

    window.close()

if __name__ == '__main__':
    main()
