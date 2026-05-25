import tkinter as tk
from tkinter import messagebox
import datetime
import time
import threading
import winsound
import json
import os


class PersistentAlarm:
    def __init__(self, root):
        self.root = root
        self.root.title("Умный будильник")
        self.root.geometry("450x400")

        self.alarm_time = None
        self.alarm_active = False
        self.snooze_minutes = 5

        self.setup_ui()
        self.load_settings()
        self.update_clock()
        self.start_alarm_checker()

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def setup_ui(self):
        # Основной фрейм
        main_frame = tk.Frame(self.root, bg='#1a1a2e')
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Заголовок
        title = tk.Label(main_frame, text="⏰ УМНЫЙ БУДИЛЬНИК ⏰",
                         font=("Arial", 20, "bold"), bg='#1a1a2e', fg='#e74c3c')
        title.pack(pady=20)

        # Текущее время
        self.time_label = tk.Label(main_frame, text="", font=("Arial", 40, "bold"),
                                   bg='#1a1a2e', fg='white')
        self.time_label.pack(pady=10)

        # Дата
        self.date_label = tk.Label(main_frame, text="", font=("Arial", 12),
                                   bg='#1a1a2e', fg='gray')
        self.date_label.pack(pady=5)

        # Рамка ввода
        input_frame = tk.Frame(main_frame, bg='#16213e',
                               relief=tk.RAISED, bd=2)
        input_frame.pack(pady=20, padx=20, fill=tk.X)

        tk.Label(input_frame, text="Установить время:", font=("Arial", 12),
                 bg='#16213e', fg='white').pack(pady=10)

        time_frame = tk.Frame(input_frame, bg='#16213e')
        time_frame.pack(pady=10)

        self.hour_spin = tk.Spinbox(time_frame, from_=0, to=23, width=5,
                                    font=("Arial", 16), format="%02.0f")
        self.hour_spin.pack(side=tk.LEFT, padx=5)
        self.hour_spin.delete(0, tk.END)
        self.hour_spin.insert(0, "07")

        tk.Label(time_frame, text=":", font=("Arial", 20),
                 bg='#16213e', fg='white').pack(side=tk.LEFT)

        self.minute_spin = tk.Spinbox(time_frame, from_=0, to=59, width=5,
                                      font=("Arial", 16), format="%02.0f")
        self.minute_spin.pack(side=tk.LEFT, padx=5)
        self.minute_spin.delete(0, tk.END)
        self.minute_spin.insert(0, "00")

        # Кнопки
        btn_frame = tk.Frame(main_frame, bg='#1a1a2e')
        btn_frame.pack(pady=10)

        self.set_btn = tk.Button(btn_frame, text="✅ Установить", command=self.set_alarm,
                                 bg='#2ecc71', fg='white', font=("Arial", 11), padx=15, pady=5)
        self.set_btn.pack(side=tk.LEFT, padx=5)

        self.cancel_btn = tk.Button(btn_frame, text="❌ Отменить", command=self.cancel_alarm,
                                    bg='#e74c3c', fg='white', font=("Arial", 11), padx=15, pady=5,
                                    state=tk.DISABLED)
        self.cancel_btn.pack(side=tk.LEFT, padx=5)

        # Кнопка "Отложить"
        self.snooze_btn = tk.Button(btn_frame, text="⏰ Отложить (5 мин)", command=self.snooze,
                                    bg='#f39c12', fg='white', font=("Arial", 11), padx=15, pady=5,
                                    state=tk.DISABLED)
        self.snooze_btn.pack(side=tk.LEFT, padx=5)

        # Информация
        self.info_label = tk.Label(main_frame, text="Будильник не установлен",
                                   font=("Arial", 10), bg='#1a1a2e', fg='gray')
        self.info_label.pack(pady=10)

    def update_clock(self):
        now = datetime.datetime.now()
        self.time_label.config(text=now.strftime("%H:%M:%S"))
        self.date_label.config(text=now.strftime("%d.%m.%Y"))
        self.root.after(1000, self.update_clock)

    def set_alarm(self):
        try:
            hour = int(self.hour_spin.get())
            minute = int(self.minute_spin.get())

            now = datetime.datetime.now()
            alarm_datetime = datetime.datetime(
                now.year, now.month, now.day, hour, minute)

            # Если время уже прошло сегодня, устанавливаем на завтра
            if alarm_datetime <= now:
                alarm_datetime += datetime.timedelta(days=1)

            self.alarm_time = alarm_datetime
            self.alarm_active = True

            self.set_btn.config(state=tk.DISABLED)
            self.cancel_btn.config(state=tk.NORMAL)
            self.snooze_btn.config(state=tk.NORMAL)

            self.info_label.config(
                text=f"Будильник установлен на {alarm_datetime.strftime('%H:%M %d.%m')}", fg="green")

            messagebox.showinfo(
                "Успех", f"Будильник установлен на {alarm_datetime.strftime('%H:%M %d.%m')}")

        except ValueError:
            messagebox.showerror("Ошибка", "Введите корректное время!")

    def cancel_alarm(self):
        self.alarm_active = False
        self.alarm_time = None
        self.set_btn.config(state=tk.NORMAL)
        self.cancel_btn.config(state=tk.DISABLED)
        self.snooze_btn.config(state=tk.DISABLED)
        self.info_label.config(text="Будильник отменён", fg="gray")

    def snooze(self):
        if self.alarm_time:
            self.alarm_time += datetime.timedelta(minutes=self.snooze_minutes)
            self.info_label.config(
                text=f"Будильник отложен на {self.snooze_minutes} мин. Новое время: {self.alarm_time.strftime('%H:%M')}", fg="orange")
            messagebox.showinfo(
                "Отложено", f"Будильник отложен на {self.snooze_minutes} минут")

    def check_alarm(self):
        while True:
            if self.alarm_active and self.alarm_time:
                now = datetime.datetime.now()
                if now >= self.alarm_time:
                    self.show_alarm()
                    self.alarm_active = False
                    self.root.after(0, self._update_ui_after_alarm)
                    break
            time.sleep(1)

    def _update_ui_after_alarm(self):
        self.set_btn.config(state=tk.NORMAL)
        self.cancel_btn.config(state=tk.DISABLED)
        self.snooze_btn.config(state=tk.DISABLED)
        self.info_label.config(text="Будильник сработал!", fg="red")

    def show_alarm(self):
        alarm_win = tk.Toplevel(self.root)
        alarm_win.title("ПОДЪЁМ!")
        alarm_win.geometry("500x400")
        alarm_win.attributes('-topmost', True)
        alarm_win.configure(bg='#2c3e50')

        # Центрирование
        alarm_win.update_idletasks()
        x = (alarm_win.winfo_screenwidth() // 2) - 250
        y = (alarm_win.winfo_screenheight() // 2) - 200
        alarm_win.geometry(f"+{x}+{y}")

        # Анимация
        frame = tk.Frame(alarm_win, bg='#2c3e50')
        frame.pack(expand=True)

        # Эмодзи
        emoji = tk.Label(frame, text="🔔🔔🔔", font=("Arial", 60), bg='#2c3e50')
        emoji.pack(pady=20)

        title = tk.Label(frame, text="ВРЕМЯ ПРОСЫПАТЬСЯ!",
                         font=("Arial", 24, "bold"), bg='#2c3e50', fg='#e74c3c')
        title.pack(pady=10)

        time_label = tk.Label(frame, text=datetime.datetime.now().strftime("%H:%M:%S"),
                              font=("Arial", 48), bg='#2c3e50', fg='white')
        time_label.pack(pady=20)

        message = tk.Label(frame, text="☀️ Доброе утро, программист! Пора писать код! ☀️",
                           font=("Arial", 14), bg='#2c3e50', fg='white')
        message.pack(pady=10)

        # Звук
        def play_alarm_sound():
            for _ in range(5):
                for freq in [1000, 1200, 1400, 1600]:
                    winsound.Beep(freq, 300)
                    time.sleep(0.1)

        sound_thread = threading.Thread(target=play_alarm_sound)
        sound_thread.daemon = True
        sound_thread.start()

        def close_and_snooze():
            alarm_win.destroy()
            self.snooze()

        btn_frame = tk.Frame(frame, bg='#2c3e50')
        btn_frame.pack(pady=20)

        tk.Button(btn_frame, text="ВСТАТЬ!", command=alarm_win.destroy,
                  bg='#2ecc71', fg='white', font=("Arial", 14), padx=20, pady=10).pack(side=tk.LEFT, padx=10)

        tk.Button(btn_frame, text="ОТЛОЖИТЬ (5 мин)", command=close_and_snooze,
                  bg='#f39c12', fg='white', font=("Arial", 14), padx=20, pady=10).pack(side=tk.LEFT, padx=10)

        # Мигание
        def blink():
            colors = ['#2c3e50', '#c0392b']
            for i in range(10):
                alarm_win.configure(bg=colors[i % 2])
                alarm_win.update()
                time.sleep(0.3)

        blink_thread = threading.Thread(target=blink, daemon=True)
        blink_thread.start()

    def start_alarm_checker(self):
        thread = threading.Thread(target=self.check_alarm, daemon=True)
        thread.start()

    def load_settings(self):
        pass  # Можно добавить загрузку сохранённых настроек

    def on_closing(self):
        self.alarm_active = False
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = PersistentAlarm(root)
    root.mainloop()
