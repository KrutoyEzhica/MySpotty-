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
        self.mode = 'setting'
        self.colors = ["#F3F4ED", "#536162",
                       "#424642", "#C06014", "#424642", "#F3F4ED"]

        # === ФИКСИРОВАННЫЙ ВЕРХНИЙ ФРЕЙМ (опционально) ===
        self.top_frame = tk.Frame(root, bg=self.colors[2], height=50)
        self.top_frame.pack(fill=tk.X, side=tk.TOP)
        self.top_frame.pack_propagate(False)

        self.title = tk.Label(self.top_frame, text="НАСТРОЙКИ",
                              font=("Arial", 16, "bold"), fg="white", bg=self.colors[2])
        self.title.pack(expand=True)

        # === ПРОКРУЧИВАЕМАЯ ОБЛАСТЬ ===
        self.main_frame = tk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(
            self.main_frame, bg=self.colors[0], highlightthickness=0)
        self.canvas.pack(side='left', fill='both', expand=True)

        scrollbar = tk.Scrollbar(
            self.main_frame, orient='vertical', command=self.canvas.yview)
        scrollbar.pack(side='right', fill='y')

        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.inner_frame = tk.Frame(self.canvas, bg=self.colors[0])
        self.canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")

        self.inner_frame.bind("<Configure>", self._update_scrollregion)
        self.canvas.bind("<MouseWheel>", self._on_mousewheel)

        # === ФИКСИРОВАННЫЙ НИЖНИЙ ФРЕЙМ ===
        self.bottom_frame = tk.Frame(root, bg=self.colors[2], height=80)
        self.bottom_frame.pack(fill=tk.X, side=tk.BOTTOM)
        self.bottom_frame.pack_propagate(False)

        self.change_mode_btn = tk.Button(
            self.bottom_frame, text="Show playlist",
            bg=self.colors[3], fg="white", font=("Arial", 12),
            command=self.change_mode
        )
        self.change_mode_btn.pack()

        self.add_btn = tk.Button(
            self.bottom_frame, text="Add song",
            bg=self.colors[3], fg="white", font=("Arial", 12),
            command=self.song.add
        )
        self.add_btn.pack(padx=20)

        self.del_btn = tk.Button(
            self.bottom_frame, text="Delete song",
            bg=self.colors[3], fg="white", font=("Arial", 12),
            command=self.change_state
        )
        self.del_btn.pack(padx=20)

        self.draw_setting()

    def draw_setting(self):
        for widget in self.inner_frame.winfo_children():
            widget.destroy()

        # Кнопка смены темы
        self.change_theme_btn = tk.Button(
            self.inner_frame, text="Поменять тему", width=20, height=2,
            command=self.interface.redraw
        )
        self.change_theme_btn.pack(padx=180, pady=10)

        self.tlist = tk.StringVar(value="Choose theme")
        self.theme_option_menu = None
        self.update_themelist()

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
            song_frame = tk.Frame(self.inner_frame, bg=self.colors[0])
            song_frame.pack(fill=tk.X, pady=5, padx=10)

            # Прямоугольник (фон)
            canvas_item = tk.Canvas(song_frame, width=450, height=90,
                                    bg=self.colors[1], highlightthickness=0)
            canvas_item.pack()
            canvas_item.create_rectangle(
                0, 0, 450, 90, fill=self.colors[1], outline=self.colors[2], width=3)

            # Название песни
            size = int(25 * min(1, (25 / len(i["name"]))))
            canvas_item.create_text(440, 25, text=i["name"], fill=self.colors[0],
                                    anchor="e", font=("Arial", size, "bold"))

            # Исполнитель
            artist_text = i["artist"] if i["artist"] else "\u2014"
            canvas_item.create_text(440, 55, text=artist_text, fill=self.colors[0],
                                    anchor="e", font=("Arial", 15))

            # Длительность
            dtime = int(i["duration"])
            time_text = f"{int(dtime//60):02d}:{int(dtime - dtime//60 * 60):02d}"
            canvas_item.create_text(440, 80, text=time_text, fill=self.colors[0],
                                    anchor="e", font=("Arial", 15))

            song_frame.bind("<Button-1>", lambda e,
                            i=i: self.song.choose_del(i))
            canvas_item.bind("<Button-1>", lambda e,
                             i=i: self.song.choose_del(i))

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
                theme_names = [i["name"] for i in data]
                theme_names = sorted(theme_names)
        except Exception:
            theme_names = ["There no themes"]

        self.theme_option_menu = tk.OptionMenu(
            self.inner_frame, self.tlist, *theme_names)
        self.theme_option_menu.pack(padx=180, pady=10)
        self.tlist.set(theme_names[0] if theme_names else "Choose theme")

    def change_state(self):
        self.state = self.states[abs(self.states.index(self.state) - 1)]
        if self.state == 'del':
            self.del_btn.config(text="Choose and play song")
        elif self.state == 'play':
            self.del_btn.config(text="Delete song")
        # print(self.state)

    def change_mode(self):
        self.mode = self.modes[abs(self.modes.index(self.mode) - 1)]
        if self.mode == 'playlist':
            self.draw_playlist()
            self.change_mode_btn.config(text="Show settings")
        elif self.mode == 'setting':
            self.draw_setting()
            self.change_mode_btn.config(text="Show playlist")
        # print(self.state)

    def recolor(self, colors):
        self.canvas.config(bg=colors[0])
        self.inner_frame.configure(bg=colors[0])
        self.top_frame.configure(bg=colors[2])
        self.title.configure(bg=colors[2], fg=colors[5])
        self.bottom_frame.configure(bg=colors[2])
        self.del_btn.configure(bg=colors[3], fg=colors[0])
        self.change_mode_btn.configure(bg=colors[3], fg=colors[0])
        self.add_btn.configure(bg=colors[3], fg=colors[0])
        self.colors = colors
