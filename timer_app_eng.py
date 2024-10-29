import tkinter as tk
from datetime import datetime, timedelta

def calculate_time_difference():
    # Set target date and time
    target_date = datetime(2024, 2, 2, 12, 0, 0)

    # Get current date and time
    current_date = datetime.now()

    # Calculate the difference
    time_difference = current_date - target_date

    # Get days, hours and minutes
    days = time_difference.days
    hours, remainder = divmod(time_difference.seconds, 3600)
    minutes, _ = divmod(remainder, 60)

    return days, hours, minutes

def update_display():
    # Update display every second
    days, hours, minutes = calculate_time_difference()
    label.config(text=f"{days} days, {hours} hours, {minutes} minutes")
    root.after(1000, update_display)

# Create main window
root = tk.Tk()
root.title("Time passed since 12:00 02.02.2024")

# Create label to display time
label = tk.Label(root, font=('Helvetica', 24))
label.pack(padx=20, pady=20)

# Start display update
update_display()

# Start main event loop
root.mainloop()
