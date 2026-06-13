import tkinter as tk
import json


class Setting:
    def __init__(self, root, song, interface):
        self.song = song
        self.root = root
        self.interface = interface
        self.states = ['play', 'del']
        self.state = 'play'
        self.modes = ['setting', 'playlist']
        self.mode = 'playlist'
        with open("themes.json", "r", encoding="utf-8") as f:
            main = json.load(f)
            self.main = main[main[0]["main"]]["setting"]
            self.playlist = main[main[0]["main"]]["playlist"]

        # Фиксированная верхняя область
        self.top_frame = tk.Frame(root, bg=self.main["top_frame"], height=50)
        self.top_frame.pack(fill=tk.X, side=tk.TOP)
        self.top_frame.pack_propagate(False)

        self.title = tk.Label(self.top_frame, text="Плейлист",
                              font=("Arial", 16, "bold"), **self.main["title"])
        self.title.pack(expand=True)

        # Прокручиваемая область
        self.main_frame = tk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(
            self.main_frame, bg=self.main["canvas"], highlightthickness=0)
        self.canvas.pack(side='left', fill='both', expand=True)

        scrollbar = tk.Scrollbar(
            self.main_frame, orient='vertical', command=self.canvas.yview)
        scrollbar.pack(side='right', fill='y')

        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.inner_frame = tk.Frame(self.canvas, bg=self.main["inner_frame"])
        self.canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")

        self.inner_frame.bind("<Configure>", self._update_scrollregion)
        self.canvas.bind("<MouseWheel>", self._on_mousewheel)

        # Фиксированная нижняя область
        self.bottom_frame = tk.Frame(
            root, bg=self.main["bottom_frame"], height=80)
        self.bottom_frame.pack(fill=tk.X, side=tk.BOTTOM)
        self.bottom_frame.pack_propagate(False)

        self.change_mode_btn = tk.Button(
            self.bottom_frame, text="Show settings",
            bg=self.main["btn"], fg="white", font=("Arial", 12), relief="flat",
            command=self.change_mode
        )
        self.change_mode_btn.pack(side='left', padx=50)

        self.add_btn = tk.Button(
            self.bottom_frame, text="Add song",
            bg=self.main["btn"], fg="white", font=("Arial", 12), relief="flat",
            command=self.song.add
        )
        self.add_btn.pack(side='left')

        self.del_btn = tk.Button(
            self.bottom_frame, text="Delete song",
            bg=self.main["btn"], fg="white", font=("Arial", 12), relief="flat",
            command=self.change_state
        )
        self.del_btn.pack(side='left', padx=50)

        self.draw_playlist()

    def draw_setting(self):
        for widget in self.inner_frame.winfo_children():
            widget.destroy()

        # Кнопка смены темы
        self.change_theme_btn = tk.Button(
            self.inner_frame, text="Поменять тему", width=20, height=2, relief="flat",
            command=self.interface.redraw
        )
        self.change_theme_btn.pack(padx=180, pady=5)

        self.tlist = tk.StringVar(value="Выбирите тему")
        self.theme_option_menu = None
        self.update_themelist()

        self.own_theme_btn = tk.Button(
            self.inner_frame, text="Сделать свою тему", width=20, height=2, relief="flat",
            command=self.interface.redraw
        )
        self.own_theme_btn.pack(padx=180, pady=5)

    def draw_playlist(self):
        # Очищаем inner_frame
        for widget in self.inner_frame.winfo_children():
            widget.destroy()

        with open("playlist.json", "r", encoding="utf-8") as f:
            data = json.load(f)

        for i in data:
            idx = data.index(i)
            y = idx * 100
            i["idx"] = idx
            # Фрейм для каждой песни (внутри inner_frame)
            song_frame = tk.Frame(self.inner_frame, bg=self.playlist["song_frame"
                                                                     ])
            song_frame.pack(fill=tk.X, pady=5, padx=10)

            # Прямоугольник (фон)
            canvas_item = tk.Canvas(song_frame, width=450, height=100,
                                    bg=self.playlist["canvas"], highlightthickness=0)
            canvas_item.pack()
            canvas_item.create_rectangle(
                0, 0, 450, 100, fill=self.playlist["canvas"], outline=self.playlist["song_frame"], width=5)

            # Название песни
            size = int(25 * min(1, (25 / len(i["name"]))))
            canvas_item.create_text(440, 25, text=i["name"], fill=self.playlist["text"],
                                    anchor="e", font=("Arial", size, "bold"))

            # Исполнитель
            artist_text = i["artist"] if i["artist"] else "\u2014"
            canvas_item.create_text(440, 55, text=artist_text, fill=self.playlist["text"],
                                    anchor="e", font=("Arial", 15))

            # Длительность
            dtime = int(i["duration"])
            time_text = f"{int(dtime//60):02d}:{int(dtime - dtime//60 * 60):02d}"
            canvas_item.create_text(440, 80, text=time_text, fill=self.playlist["text"],
                                    anchor="e", font=("Arial", 15))

            song_frame.bind("<Button-1>", lambda e,
                            i=i: self.song.choose_del(i))
            canvas_item.bind("<Button-1>", lambda e,
                             i=i: self.song.choose_del(i))
            song_frame.bind("<Button-3>", lambda e,
                            i=i: self.change_val(i))
            canvas_item.bind("<Button-3>", lambda e,
                             i=i: self.change_val(i))

    def _update_scrollregion(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def update_themelist(self):
        if self.theme_option_menu:
            self.theme_option_menu.destroy()

        try:
            with open("themes.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                theme_names = [i["name"] for i in data[1::]]
                theme_names = sorted(theme_names)
        except Exception:
            theme_names = ["There are no themes"]

        self.theme_option_menu = tk.OptionMenu(
            self.inner_frame, self.tlist, *theme_names)
        self.theme_option_menu.pack(padx=180, pady=10)
        self.tlist.set(theme_names[0] if theme_names else "Choose theme")

    def change_state(self):
        self.state = self.states[abs(self.states.index(self.state) - 1)]
        if self.state == 'del':
            self.del_btn.config(text="Choose and \n play song", height=2)
        elif self.state == 'play':
            self.del_btn.config(text="Delete song", height=1)
        # print(self.state)

    def change_mode(self):
        self.mode = self.modes[abs(self.modes.index(self.mode) - 1)]
        if self.mode == 'playlist':
            self.draw_playlist()
            self.title.config(text="Плейлист")
            self.change_mode_btn.config(text="Show settings")
        elif self.mode == 'setting':
            self.draw_setting()
            self.title.config(text="Настройки")
            self.change_mode_btn.config(text="Show playlist")
        # print(self.state)

    def recolor(self, main, playlist):
        self.canvas.config(bg=main["canvas"])
        self.inner_frame.configure(bg=main["inner_frame"])
        self.top_frame.configure(bg=main["top_frame"])
        self.title.configure(**main["title"])
        self.bottom_frame.configure(bg=main["bottom_frame"])
        self.del_btn.configure(bg=main["btn"])
        self.change_mode_btn.configure(bg=main["btn"])
        self.add_btn.configure(bg=main["btn"])
        self.main = main
        self.playlist = playlist

    def change_val(self, song_arguments):
        dialog = tk.Toplevel(self.root)
        dialog.title("Параметры песни")
        dialog.geometry("300x280")
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()
        name_entry = tk.Entry(
            dialog, width=40, font=('Arial', 20), fg="#7f7f7f", justify="center")
        name_entry.pack(pady=50)
        name_entry.insert(0, song_arguments["name"])
        artist_entry = tk.Entry(dialog, width=40, font=(
            'Arial', 14), fg="#7f7f7f", justify="center")
        artist_entry.pack(pady=20)
        artist_entry.insert(0, str(song_arguments["artist"]))
        cancel_btn = tk.Button(
            dialog, text='Отмена', command=lambda: dialog.destroy()).pack(side='left', padx=60)
        save_btn = tk.Button(dialog, text='Сохранить', command=lambda: self.save_val(
            name_entry.get(), artist_entry.get(), song_arguments["idx"], dialog)).pack(side='left')

    def save_val(self, name, artist, idx, dialog):
        with open("playlist.json", "r", encoding="utf-8") as f:
            song = json.load(f)
        song[idx]["name"] = name
        song[idx]["artist"] = artist if artist != 'None' else None
        with open("playlist.json", "w", encoding="utf-8") as f:
            json.dump(sorted(song, key=lambda song: song["name"].lower()), f)
        dialog.destroy()
        self.draw_playlist()
