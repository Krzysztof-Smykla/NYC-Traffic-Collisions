import tkinter as tk
from tkinter import filedialog, messagebox
from tkcalendar import Calendar

import folium
from folium import Map


class Menu:
    def __init__(self):
        # Initialize root tkinter window
        self.root = tk.Tk()
        self.root.title("Car crash Menu")
        self.root.geometry("500x400")

        # Fields for user inputs

        # Select date range in calendar gui
        self.date_range_label = tk.Label(self.root, text="Date Range:")
        self.date_range_label.pack()
        self.date_range_entry = tk.Entry(self.root)
        self.date_range_entry.pack()

        # Slider
        self.severity_label = tk.Label(self.root, text="Severity:")
        self.severity_label.pack()
        self.severity_entry = tk.Entry(self.root)
        self.severity_entry.pack()

        # Dropdown of boroughs of NYC
        # Use geopandas to define the borough area on map
        self.location_label = tk.Label(self.root, text="Location:")
        self.location_label.pack()
        self.location_entry = tk.Entry(self.root)
        self.location_entry.pack()

        # Buttons
        self.fetch_button = tk.Button(self.root, text="Fetch Data", command=self.FetchData)
        self.fetch_button.pack()

        """self.display_map_button = tk.Button(self.root, text="Display Map", command=self.DisplayMap)
        self.display_map_button.pack()"""

        self.download_button = tk.Button(self.root, text="Download Data", command=self.DownloadData)
        self.download_button.pack()

        # Progress indicator
        self.progress_label = tk.Label(self.root, text="")
        self.progress_label.pack()

    def DisplayMenu(self):
        # Error handling and display menu
        try:
            self.root.mainloop()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def FetchData(self):
        # Placeholder function for data fetching
        # Update progress label as a simple indicator
        self.progress_label.config(text="Fetching data... Please wait.")
        self.root.update()

        # Simulate data fetch
        # Replace this with actual data fetching logic as needed
        import time
        time.sleep(2)  # simulate delay

        self.progress_label.config(text="Data fetched successfully!")

    def DownloadData(self):
        # Open a dialog for user to select file type and location
        filetypes = [('CSV Files', '*.csv'), ('JSON Files', '*.json')]
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=filetypes)

        if file_path:
            try:
                # Simulate data download - replace with actual data export logic
                with open(file_path, 'w') as f:
                    f.write("Sample data")  # Placeholder content
                messagebox.showinfo("Success", f"Data saved to {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Could not save file: {e}")

    
# Initialize and run the menu
menu = Menu()
menu.DisplayMenu()
