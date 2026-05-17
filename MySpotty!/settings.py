import tkinter as tk
import json


class Setting:
    def __init__(self, root, song, interface):
        self.song = song
        self.root = root
        self.interface = interface
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)  # .place(x=501, y=0)
        self.canvas = tk.Canvas(
            self.main_frame, bg='#F3F4ED', highlightthickness=0)
        self.canvas.pack(side='left', fill='both', expand=True)
        scrollbar = tk.Scrollbar(
            self.main_frame, orient='vertical', command=self.canvas.yview)
        scrollbar.pack(side='right', fill='y')

        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.inner_frame = tk.Frame(self.canvas, bg='#F3F4ED')
        self.canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")

        self.inner_frame.bind("<Configure>", self._update_scrollregion)

        self.canvas.bind("<MouseWheel>", self._on_mousewheel)
        self.draw_setting()

    def draw_setting(self):
        self.canvas.delete('all')

        # self.choose_btn = self.canvas.create_window(250, 100, window=tk.Button(
        #    self.root, text="Выбрать", width=12, height=2, command=self.song.choose))
        # self.choose_btn.pack()

        # self.mlist = tk.StringVar(value="Выберите песню")
        # self.song_option_menu = None
        # self.update_playlist()

        # self.open_button = self.canvas.create_window(250, 150, window=tk.Button(
        #    self.root, text="Добавить в плейлист", width=20, height=2, command=self.song.add))

        self.change_theme_btn = self.canvas.create_window(250, 100, window=tk.Button(
            self.root, text="Поменять тему", width=20, height=2, command=self.interface.redraw))

        self.tlist = tk.StringVar(value="Choose theme")
        self.theme_option_menu = None
        self.update_themelist()

        self.change_mode = self.canvas.create_window(250, 200, window=tk.Button(
            self.root, text="Show playlist", width=20, height=2, command=self.draw_playlist))
        # self.open_button.pack(pady=5)

        # self.addnewgr = tk.Button(self.label, text="Добавить из Newgrounds", command=song.add_song_from_newgr)
        # self.addnewgr.pack(pady=5)

        # self.song_id = tk.Entry(self.label)
        # self.song_id.pack(pady=5)
        # self.song_id.insert(0, "Введите ID")
    def draw_playlist(self):
        self.canvas.delete('all')
        self.change_mode = self.canvas.create_window(250, 100, window=tk.Button(
            self.root, text="Show setting", width=20, height=2, command=self.draw_setting))
        with open("playlist.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            data = sorted(data, key=lambda data: data["name"])
        for i in data:
            y = data.index(i) * 100
            self.canvas.create_rectangle(
                20, y + 10, 450, y + 100, width=3, fill="#536162", outline='#424642', tags=f"song{data.index(i)}"
            )
            size = int(25 * min(1, (25 / len(i["name"]))))
            self.canvas.create_text(
                440, y + 30, text=i["name"], fill="#F3F4ED", anchor="e", font=("Arial", size, "bold"), tags=f"song{data.index(i)}")
            self.canvas.create_text(
                440, y + 60, text=i["artist"] if i["artist"] else "\u2014", fill="#F3F4ED", anchor="e", font=("Arial", 15), tags=f"song{data.index(i)}")
            dtime = int(i["duration"])
            self.canvas.create_text(
                440, y + 85, text=f"{int(dtime//60):02d}:{int(dtime-dtime//60*60):02d}", fill="#F3F4ED", anchor="e", font=("Arial", 15), tags=f"song{data.index(i)}")
            self.canvas.tag_bind(
                f"song{data.index(i)}", "<Button-1>", lambda e, i=i: self.song.choose(i))

    def _update_scrollregion(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def update_playlist(self):
        if self.song_option_menu:
            self.song_option_menu.destroy()

        try:
            with open("playlist.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                song_names = [i["name"]
                              for i in data]
                song_names = sorted(song_names)
        except Exception:
            song_names = ["Нет песен"]

        self.song_option_menu = self.canvas.create_window(
            250, 200, window=tk.OptionMenu(self.root, self.mlist, *song_names))
        # self.option_menu.pack(pady=5)
        self.mlist.set(song_names[0] if song_names else "Выберите песню")

    def update_themelist(self):
        if self.theme_option_menu:
            self.theme_option_menu.destroy()

        try:
            with open("themes.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                theme_names = [i["name"]
                               for i in data]
                theme_names = sorted(theme_names)
        except Exception:
            theme_names = ["There no themes"]

        self.theme_option_menu = self.canvas.create_window(
            250, 150, window=tk.OptionMenu(self.root, self.tlist, *theme_names))
        # self.option_menu.pack(pady=5)
        self.tlist.set(theme_names[0] if theme_names else "Choose theme")
