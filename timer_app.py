import tkinter as tk
from datetime import datetime, timedelta

def calculate_time_difference():
    # Задаем целевую дату и время
    target_date = datetime(2024, 2, 2, 12, 0, 0)

    # Получаем текущую дату и время
    current_date = datetime.now()

    # Вычисляем разницу
    time_difference = current_date - target_date

    # Получаем количество дней, часов и минут
    days = time_difference.days
    hours, remainder = divmod(time_difference.seconds, 3600)
    minutes, _ = divmod(remainder, 60)

    return days, hours, minutes

def update_display():
    # Обновляем отображение каждую секунду
    days, hours, minutes = calculate_time_difference()
    label.config(text=f"{days} дней, {hours} часов, {minutes} минут")
    root.after(1000, update_display)

# Создаем основное окно
root = tk.Tk()
root.title("прошло с 12:00 02.02.2024")

# Создаем метку для отображения времени
label = tk.Label(root, font=('Helvetica', 24))
label.pack(padx=20, pady=20)

# Запускаем обновление отображения
update_display()

# Запускаем основной цикл обработки событий
root.mainloop()
