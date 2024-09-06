import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import os

def process_data(input_files, output_dir):
    try:
        # Dictionary to store DataFrames
        dfs = {}
        
        # Read input files
        for year, file_path in input_files.items():
            df = pd.read_csv(file_path, sep=';', encoding='LATIN')
            dfs[year] = df
        
        # Process each DataFrame
        for year, df in dfs.items():
            df_rm_resp = filter_rm_resp(df)
            output_file = os.path.join(output_dir, f'df_{year}_rm_resp.csv')
            df_rm_resp.to_csv(output_file, index=False)
        
        messagebox.showinfo("Success", "Data processing completed successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

def filter_rm_resp(df):
    # Implement the filter_rm_resp function here
    # This is a placeholder implementation
    df['CodigoRegion'] = df['IdEstablecimiento'].map(dict_codigo_antiguo)
    df_rm = df.loc[df.CodigoRegion == 13]
    df_rm_resp = df_rm.loc[df_rm.IdCausa.isin(diccionario_causas_au.keys())]
    df_rm_resp['Causa'] = df_rm_resp.IdCausa.map(diccionario_causas_au)
    df_rm_resp['Causa_category'] = df_rm_resp.IdCausa.map(diccionario_causas_categorizada_au)
    columns = ['Total', 'Menores_1', 'De_1_a_4', 'De_5_a_14', 'De_15_a_64', 'De_65_y_mas']
    df_rm_resp = df_rm_resp.groupby(by=['GLOSATIPOESTABLECIMIENTO', 'semana', 'IdCausa', 'Causa'])[columns].sum().reset_index()
    return df_rm_resp

class DataProcessorGUI:
    def __init__(self, master):
        self.master = master
        master.title("Data Processor")
        
        self.input_files = {}
        self.output_dir = ""
        
        # Create GUI elements
        self.create_widgets()
    
    def create_widgets(self):
        # File selection buttons
        years = ['2018', '2019', '2020', '2021', '2022', '2023', '2024']
        for year in years:
            button = tk.Button(self.master, text=f"Select {year} File", command=lambda y=year: self.select_file(y))
            button.pack()
        
        # Output directory selection
        self.output_button = tk.Button(self.master, text="Select Output Directory", command=self.select_output_dir)
        self.output_button.pack()
        
        # Process button
        self.process_button = tk.Button(self.master, text="Process Data", command=self.run_processing)
        self.process_button.pack()
    
    def select_file(self, year):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            self.input_files[year] = file_path
            messagebox.showinfo("File Selected", f"{year} file selected: {file_path}")
    
    def select_output_dir(self):
        self.output_dir = filedialog.askdirectory()
        if self.output_dir:
            messagebox.showinfo("Directory Selected", f"Output directory selected: {self.output_dir}")
    
    def run_processing(self):
        if not self.input_files:
            messagebox.showerror("Error", "Please select at least one input file.")
            return
        if not self.output_dir:
            messagebox.showerror("Error", "Please select an output directory.")
            return
        
        process_data(self.input_files, self.output_dir)

if __name__ == "__main__":
    root = tk.Tk()
    app = DataProcessorGUI(root)
    root.mainloop()