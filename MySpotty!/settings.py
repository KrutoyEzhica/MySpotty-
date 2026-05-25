class Slider:
    def __init__(self, canvas, x, y, width, song, bounds=None):
        self.canvas = canvas
        self.width = width
        self.bounds = bounds  # (min_x, min_y, max_x, max_y)
        self.line = canvas.create_line(
            # width=10
            bounds[0] + width // 2, bounds[1] + width // 2, bounds[2] - width // 2, bounds[3] - width // 2, width=5, fill="#536162", tags="slider")
        canvas.tag_bind("slider", "<Button-1>", lambda event: self.song.rewind(
            int(self.song.duration * ((event.x - self.bounds[0]) / 400))))
        
        self.line1 = canvas.create_line(
            # width=10
            bounds[0] + width // 2, bounds[1] + width // 2, bounds[0] + width // 2, bounds[3] - width // 2, width=10, fill="#C06014", tags="slider")
        canvas.tag_bind("slider", "<Button-1>", lambda event: self.song.rewind(
            int(self.song.duration * ((event.x - self.bounds[0]) / 400))))
        
        self.obj = canvas.create_oval(
            x, y, x + width, y + width, fill="#424642", width=0)

        canvas.tag_bind(self.obj, "<ButtonPress-1>", self.start_drag)
        canvas.tag_bind(self.obj, "<B1-Motion>",
                        self.drag)
        canvas.tag_bind(self.obj, "<ButtonRelease-1>", self.release)
        self.isdrag = False
        self.song = song
        self.drag_data = {"x": 0, "y": 0}

    def start_drag(self, event):
        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y
        self.isdrag = True

    def drag(self, event):
        dx = event.x - self.drag_data["x"]
        dy = event.y - self.drag_data["y"]

        # Получаем текущие координаты
        coords = self.canvas.coords(self.obj)
        new_x = coords[0] + dx
        new_y = coords[1] + dy

        # Применяем ограничения
        if self.bounds:
            new_x = max(self.bounds[0], min(
                new_x, self.bounds[2] - self.width))
            new_y = max(self.bounds[1], min(
                new_y, self.bounds[3] - self.width))

        self.canvas.coords(
            self.obj, new_x, new_y, new_x + self.width, new_y + self.width
        )
        self.canvas.coords(
            self.line1, self.bounds[0] + self.width // 2, self.bounds[1] +
            self.width // 2, new_x +
            self.width, self.bounds[3] - self.width // 2
        )
        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y
        # print(new_x)
        # print(int((-40 + new_x) / 4))

    def release(self, event):
        self.isdrag = False
        self.song.rewind(
            int(self.song.duration * ((self.drag_data["x"] - self.bounds[0]) / 400)))

    def song_move(self, song_prec):
        if not self.isdrag:
            new_x = int(song_prec * 4 + 40)
            self.canvas.coords(self.obj, new_x, 440, new_x + self.width, 460)
        self.canvas.coords(
            self.line1, self.bounds[0] + self.width // 2, self.bounds[1] +
            self.width // 2, new_x +
            self.width, self.bounds[3] - self.width // 2
        )
    
    def recolor(self, colors):
        self.canvas.itemconfig(self.line, fill=colors[1])
        self.canvas.itemconfig(self.obj, fill=colors[2])
        self.canvas.itemconfig(self.obj, fill=colors[3])
