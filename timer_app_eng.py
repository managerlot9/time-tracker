import tkinter as tk
from tkinter import ttk
import json
import os
from datetime import datetime, timedelta
import threading
import time

class TimerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Time Tracker")
        
        # Setting window size
        self.root.geometry("300x400")
        
        # Creating main frame
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Dictionary for storing timers
        self.timers = {}
        
        # Loading saved timers
        self.load_timers()
        
        # Creating and configuring UI elements
        self.create_widgets()
        
        # Variable for tracking if timer is running
        self.is_running = False
        
        # Thread for timer
        self.timer_thread = None

    def create_widgets(self):
        # Input field for new timer name
        self.timer_name_var = tk.StringVar()
        self.timer_entry = ttk.Entry(self.main_frame, textvariable=self.timer_name_var)
        self.timer_entry.grid(row=0, column=0, padx=5, pady=5)
        
        # Button to add new timer
        self.add_button = ttk.Button(self.main_frame, text="Add Timer", command=self.add_timer)
        self.add_button.grid(row=0, column=1, padx=5, pady=5)
        
        # Frame for timer list
        self.timers_frame = ttk.Frame(self.main_frame)
        self.timers_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E))

        # Displaying existing timers
        self.update_timer_display()

    def add_timer(self):
        # Getting timer name from input field
        name = self.timer_name_var.get().strip()
        if name and name not in self.timers:
            # Adding new timer with zero time
            self.timers[name] = {"time": "00:00:00", "running": False}
            self.save_timers()
            self.update_timer_display()
            self.timer_name_var.set("")  # Clearing input field

    def update_timer_display(self):
        # Clearing current timer display
        for widget in self.timers_frame.winfo_children():
            widget.destroy()
        
        # Displaying each timer
        for row, (name, data) in enumerate(self.timers.items()):
            # Timer name
            name_label = ttk.Label(self.timers_frame, text=name)
            name_label.grid(row=row, column=0, padx=5, pady=2)
            
            # Timer time
            time_var = tk.StringVar(value=data["time"])
            time_label = ttk.Label(self.timers_frame, textvariable=time_var)
            time_label.grid(row=row, column=1, padx=5, pady=2)
            
            # Start/Stop button
            button_text = "Stop" if data["running"] else "Start"
            start_stop_button = ttk.Button(
                self.timers_frame,
                text=button_text,
                command=lambda n=name, tv=time_var: self.toggle_timer(n, tv)
            )
            start_stop_button.grid(row=row, column=2, padx=5, pady=2)
            
            # Delete button
            delete_button = ttk.Button(
                self.timers_frame,
                text="Delete",
                command=lambda n=name: self.delete_timer(n)
            )
            delete_button.grid(row=row, column=3, padx=5, pady=2)

    def toggle_timer(self, name, time_var):
        self.timers[name]["running"] = not self.timers[name]["running"]
        self.save_timers()
        self.update_timer_display()
        
        if self.timers[name]["running"]:
            # Starting timer in a separate thread
            thread = threading.Thread(target=self.run_timer, args=(name, time_var))
            thread.daemon = True
            thread.start()

    def run_timer(self, name, time_var):
        while self.timers[name]["running"]:
            # Converting current time to seconds
            h, m, s = map(int, self.timers[name]["time"].split(':'))
            total_seconds = h * 3600 + m * 60 + s
            
            # Adding one second
            total_seconds += 1
            
            # Converting back to HH:MM:SS format
            new_time = str(timedelta(seconds=total_seconds))
            if '.' in new_time:
                new_time = new_time.split('.')[0]
            
            # Updating timer
            self.timers[name]["time"] = new_time
            time_var.set(new_time)
            self.save_timers()
            
            time.sleep(1)

    def delete_timer(self, name):
        # Stopping timer if it's running
        if self.timers[name]["running"]:
            self.timers[name]["running"] = False
        
        # Removing timer
        del self.timers[name]
        self.save_timers()
        self.update_timer_display()

    def save_timers(self):
        # Saving timers to JSON file
        with open('timers.json', 'w') as f:
            json.dump(self.timers, f)

    def load_timers(self):
        # Loading timers from JSON file if it exists
        if os.path.exists('timers.json'):
            with open('timers.json', 'r') as f:
                self.timers = json.load(f)

if __name__ == "__main__":
    root = tk.Tk()
    app = TimerApp(root)
    root.mainloop()
