import tkinter as tk
from datetime import datetime
import json
from tkinter import messagebox

class TimeTracker:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Time Tracker")
        self.target_date = self.load_settings()
        
        self.setup_ui()
        self.create_menu()
        self.update_display()
        
    def setup_ui(self):
        self.label = tk.Label(self.root, font=('Helvetica', 24))
        self.label.pack(padx=20, pady=20)
        
        tk.Button(self.root, text="+", command=lambda: self.change_font_size(2)).pack(side=tk.RIGHT)
        tk.Button(self.root, text="-", command=lambda: self.change_font_size(-2)).pack(side=tk.RIGHT)
        
    def create_menu(self):
        menu = tk.Menu(self.root)
        self.root.config(menu=menu)
        
        file_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Set Target Date", command=self.set_target_date)
        file_menu.add_command(label="Toggle Theme", command=self.toggle_theme)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
    def update_display(self):
        days, hours, minutes = self.safe_calculate_time_difference()
        formatted_time = self.format_time(days, hours, minutes)
        self.label.config(text=formatted_time)
        self.root.after(1000, self.update_display)
        
    def safe_calculate_time_difference(self):
        try:
            current_date = datetime.now()
            time_difference = current_date - self.target_date
            days = time_difference.days
            hours, remainder = divmod(time_difference.seconds, 3600)
            minutes, _ = divmod(remainder, 60)
            return days, hours, minutes
        except Exception as e:
            print(f"Error: {e}")
            return 0, 0, 0
        
    def format_time(self, days, hours, minutes):
        if days == 0:
            if hours == 0:
                return f"{minutes} minutes"
            return f"{hours} hours, {minutes} minutes"
        return f"{days} days, {hours} hours, {minutes} minutes"
    
    def set_target_date(self):
        def save_date():
            date_str = entry.get()
            try:
                self.target_date = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
                self.save_settings()
                top.destroy()
            except ValueError:
                messagebox.showerror("Error", "Invalid date format. Use YYYY-MM-DD HH:MM:SS")

        top = tk.Toplevel(self.root)
        tk.Label(top, text="Enter target date (YYYY-MM-DD HH:MM:SS):").pack()
        entry = tk.Entry(top)
        entry.pack()
        tk.Button(top, text="Save", command=save_date).pack()
        
    def toggle_theme(self):
        if self.root.cget('bg') == 'white':
            self.root.configure(bg='black')
            self.label.configure(bg='black', fg='white')
        else:
            self.root.configure(bg='white')
            self.label.configure(bg='white', fg='black')
        
    def change_font_size(self, delta):
        current_size = int(self.label['font'].split()[-1])
        new_size = max(8, min(72, current_size + delta))
        self.label.configure(font=('Helvetica', new_size))
        
    def save_settings(self):
        settings = {
            'target_date': self.target_date.strftime("%Y-%m-%d %H:%M:%S")
        }
        with open('settings.json', 'w') as f:
            json.dump(settings, f)
            
    def load_settings(self):
        try:
            with open('settings.json', 'r') as f:
                settings = json.load(f)
                return datetime.strptime(settings['target_date'], "%Y-%m-%d %H:%M:%S")
        except:
            return datetime(2024, 2, 2, 12, 0, 0)
        
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = TimeTracker()
    app.run()
