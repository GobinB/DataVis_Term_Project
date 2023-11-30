import pandas as pd
import tkinter as tk
from tkinter import filedialog

class DataImporter:
    def __init__(self, root):
        self.root = root
        self.root.title("Data Importer")
        
        self.participant_label = tk.Label(root, text="Select Participant:")
        self.participant_label.pack()
        
        self.participant_var = tk.StringVar()
        self.participant_dropdown = tk.OptionMenu(root, self.participant_var, "Participant 1", "Participant 2")
        self.participant_dropdown.pack()
        
        self.import_button = tk.Button(root, text="Import Data", command=self.load_data)
        self.import_button.pack()
        
    def load_data(self):
        participant = self.participant_var.get()
        
        # Open a file dialog to select summary.csv and metadata.csv files
        summary_filename = filedialog.askopenfilename(title="Select Summary Data File")
        metadata_filename = filedialog.askopenfilename(title="Select Metadata File")
        
        try:
            summary_data = pd.read_csv(summary_filename)
            metadata_data = pd.read_csv(metadata_filename)
            
            # Now you have summary_data and metadata_data for further processing
            # You can proceed with implementing the next steps.
            # For now, you can print the loaded data to verify it's working.
            
            print("Summary Data:")
            print(summary_data.head())
            
            print("\nMetadata Data:")
            print(metadata_data.head())
            
        except FileNotFoundError:
            print("File not found. Please check the file paths.")
        
if __name__ == "__main__":
    root = tk.Tk()
    app = DataImporter(root)
    root.mainloop()
