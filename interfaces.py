import json


class Interface:
    def __init__(self, canvas, song, root, slider):
        self.set = False
        self.root = root
        self.canvas = canvas
        self.setting = None
        self.song = None
        with open("themes.json", "r", encoding="utf-8") as f:
            main = json.load(f)
            main = main[main[0]["main"]]
        self.slider = slider
        self.canvas.config(main["bg"])
        self.setting_btn = canvas.create_rectangle(
            440, 25, 480, 65, width=3, **main["setting_btn"], tags='setting')
        # canvas.create_arc(60, 500, 100, 540, width=3, outline='#424642', start=270, extent=270, style="arc")
        # Фото-карточка сонга
        self.photo = canvas.create_rectangle(
            75, 25, 425, 375, width=3, **main["photo"])
        # Название сонга
        self.name = canvas.create_text(
            250, 395, text="\u2014", font=("Arial", 25, "bold"), **main["song"]
        )
        # Имя исполнителя
        self.art_name = canvas.create_text(
            250, 425, text="\u2014", font=("Arial", 15), **main["art_name"]
        )

        # Длительность сонга
        self.time_s = canvas.create_text(
            431, 470, text=": --", font=("Arial", 15, "bold"), **main["seconds"]
        )
        self.time_m = canvas.create_text(
            406, 470, text="--", font=("Arial", 15, "bold"), **main["minutes"]
        )
        # Текущее время
        self.cur_time_s = canvas.create_text(
            91, 470, text=":00", font=("Arial", 15, "bold"), **main["seconds"]
        )
        self.cur_time_m = canvas.create_text(
            66, 470, text="00", font=("Arial", 15, "bold"), **main["minutes"]
        )
        # Кнопка паузы
        self.pause_btn = canvas.create_oval(
            224, 494, 276, 546, width=3, **main["pause_btn"], tags="pause"
        )
        self.p = canvas.create_polygon(
            240, 507, 266, 520, 240, 533, **main["p"], width=3, tags="pause"
        )
        self.p1 = canvas.create_rectangle(
            239, 507, 247, 533, width=3, **main["p"], tags="pause"
        )

        self.p2 = canvas.create_rectangle(
            253, 507, 261, 533, width=3, **main["p"], tags="pause"
        )
        canvas.itemconfig(self.p1, state="hidden")
        canvas.itemconfig(self.p2, state="hidden")
        canvas.tag_bind("pause", "<Button-1>", lambda e: song.pause())
        canvas.tag_bind("setting", "<Button-1>",
                        lambda e: self.toggle_setting())
        # Кнопка для предыдущего сонга
        self.previous_hitbox = canvas.create_rectangle(
            125, 490, 175, 550, **main["hitbox"], width=0, tags="previous")
        self.previous1 = canvas.create_polygon(
            166, 507, 140, 520, 166, 533, **main["rewind"], width=3, tags="previous")
        self.previous2 = canvas.create_line(
            137, 507, 137, 533, width=5, **main["lines"], tags="previous")
        # Кнопка для следующего сонга
        self.next_hitbox = canvas.create_rectangle(
            330, 490, 380, 550, **main["hitbox"], width=0, tags="next")
        self.next1 = canvas.create_polygon(
            340, 507, 366, 520, 340, 533, width=3, **main["rewind"], tags="next")
        self.next2 = canvas.create_line(
            369, 507, 369, 533, width=5, **main["lines"], tags="next")
        canvas.tag_bind("next", "<Button-1>",
                        lambda e: self.song.next_song())
        canvas.tag_bind("previous", "<Button-1>",
                        lambda e: self.song.previous_song())

    def redraw(self):
        theme = self.setting.tlist.get()
        with open("themes.json", "r", encoding="utf-8") as f:
            for i in json.load(f)[1::]:
                if theme == i["name"]:
                    colors = i
                    break
        self.canvas.config(colors["bg"])
        self.canvas.itemconfig(self.setting_btn, colors["setting_btn"])
        self.canvas.itemconfig(self.photo, colors["photo"])
        self.canvas.itemconfig(self.name, colors["song"])
        self.canvas.itemconfig(self.art_name, colors["art_name"])
        self.canvas.itemconfig(self.time_s, colors["seconds"])
        self.canvas.itemconfig(self.time_m, colors["minutes"])
        self.canvas.itemconfig(self.cur_time_s, colors["seconds"])
        self.canvas.itemconfig(self.cur_time_m, colors["minutes"])
        self.canvas.itemconfig(self.pause_btn, colors["pause_btn"])
        self.canvas.itemconfig(self.p, colors["p"])
        self.canvas.itemconfig(self.p1, colors["p"])
        self.canvas.itemconfig(self.p2, colors["p"])
        self.canvas.itemconfig(self.previous_hitbox, colors["hitbox"])
        self.canvas.itemconfig(self.next_hitbox, colors["hitbox"])
        self.canvas.itemconfig(self.previous1, colors["rewind"])
        self.canvas.itemconfig(self.previous2, colors["lines"])
        self.canvas.itemconfig(self.next1, colors["rewind"])
        self.canvas.itemconfig(self.next2, colors["lines"])
        self.slider.recolor(colors["slider"])
        self.setting.recolor(colors["setting"], colors["playlist"])

    def choose_song_intf(self, song, artist, size, dtime):
        self.canvas.itemconfig(self.p1, state="normal")
        self.canvas.itemconfig(self.p2, state="normal")
        self.canvas.itemconfig(self.p, state="hidden")
        self.isplay = True
        self.canvas.itemconfig(
            self.name, text=song if song else "\u2014", font=("Arial", size, "bold")
        )  # len=28
        self.canvas.itemconfig(
            self.art_name, text=artist if artist else "\u2014")
        self.canvas.itemconfig(
            self.time_m,
            text=f"{int(dtime//60):02d}"
        )
        self.canvas.itemconfig(
            self.time_s,
            text=f":{int(dtime-dtime//60*60):02d}"
        )
        self.canvas.itemconfig(self.cur_time_s, text=":00")
        self.canvas.itemconfig(self.cur_time_m, text="00")

    def update_cur_time(self, cur_time):
        self.canvas.itemconfig(
            self.cur_time_m, text=f"{int(cur_time//60):02d}"
        )
        self.canvas.itemconfig(
            self.cur_time_s, text=f":{int(cur_time-cur_time//60*60):02d}"
        )

    def pause(self, ispause):
        if ispause:
            self.canvas.itemconfig(self.p1, state="hidden")
            self.canvas.itemconfig(self.p2, state="hidden")
            self.canvas.itemconfig(self.p, state="normal")
        else:
            self.canvas.itemconfig(self.p1, state="normal")
            self.canvas.itemconfig(self.p2, state="normal")
            self.canvas.itemconfig(self.p, state="hidden")

    def animate_window_size(self, target_width, step=50, delay=10):
        current_width = self.root.winfo_width()
        if step > 0 and current_width < target_width:
            new_width = min(current_width + step, target_width)
            self.root.geometry(f'{new_width}x600')
            self.root.after(delay, lambda: self.animate_window_size(
                target_width, step, delay))
        elif step < 0 and current_width > target_width:
            new_width = max(current_width + step, target_width)
            self.root.geometry(f'{new_width}x600')
            self.root.after(delay, lambda: self.animate_window_size(
                target_width, step, delay))
        else:
            self.set = not self.set

    def toggle_setting(self):
        if self.set:
            self.animate_window_size(500, -50, 10)
        else:
            self.animate_window_size(1000, 50, 10)
