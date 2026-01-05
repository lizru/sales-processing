
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from tkinter import messagebox, filedialog
import pandas as pd
import export_upload




def select_sales_file_path():
    """Returns a pandas DataFrame of the selected sales data CSV file."""
    print("Opening file dialog...")
    root= Tk()
    root.title("Select Sales Data CSV File")
    root.lift()
    root.attributes("-topmost", True)
    root.after(1000, lambda: root.attributes("-topmost", False))
    root.withdraw()
    file_path = askopenfilename(parent=root, filetypes=[("CSV files", "*.csv")])
    root.destroy()
    if not file_path:
        raise FileNotFoundError("No file selected.")
    return pd.read_csv(file_path)




def export_choice_dialog(df):
    """tkinter dialogue asking whether to export to Excel or Google Sheets."""
    root = Tk()
    root.withdraw()
    
    result = messagebox.askquestion(
        "Export Option", 
        "Do you want to export to Google Sheets? (No will export to Excel)"
    )
    
    if result == 'yes':
        export_upload.upload_to_google_sheet(df)
    else:
        file_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx")],
            title="Save anonymized data as Excel"
        )
        if not file_path:
            raise FileNotFoundError("No file selected for Excel export.")
        df.to_excel(file_path, index=False)
        print(f"Excel export completed: {file_path}")

