import pygame
import json
import os
import newgroundsdl
import glob
import time
import tkinter as tk
from tinytag import TinyTag
from tkinter import filedialog


class Song:
    def __init__(self, canvas, root):
        self.duration = 0
        self.canvas = canvas
        self.slider = ''
        self.setting = ''
        self.interface = ''
        self.root = root
        self.isplay = False
        self.cur_time = 0
        self.music_start_time = 0
        self.music_paused_time = 0
        self.volume = 1.0
        pygame.init()
        pygame.mixer.init()

    def pause(self):
        if self.isplay:
            self.music_paused_time = self.get_current_position()
            pygame.mixer.music.pause()

        else:
            pygame.mixer.music.unpause()
            self.music_start_time = time.time() - self.music_paused_time
        self.interface.pause(self.isplay)
        self.isplay = not self.isplay
        self.update()

    def get_current_position(self):
        if self.isplay:
            return time.time() - self.music_start_time
        else:
            return self.music_paused_time

    def update(self):
        if self.isplay and pygame.mixer.music.get_busy():
            self.cur_time = self.get_current_position()
            self.interface.update_cur_time(self.cur_time)
            self.slider.song_move(int(self.cur_time / self.duration * 100))
            self.root.after(50, lambda: self.update())
        else:
            self.interface.pause(1)

    def choose(self, songs_arguments):
        path = songs_arguments["path"]
        song = songs_arguments["name"]
        art = songs_arguments["artist"]
        self.duration = int(songs_arguments["duration"])
        pygame.mixer.music.load(path)
        pygame.mixer.music.play()
        pygame.mixer.music.set_volume(1.0)
        size = int(25 * min(1, (25 / len(song))))
        self.interface.choose_song_intf(song, art, size, self.duration)
        self.music_start_time = time.time()
        self.music_paused_time = 0
        self.isplay = True
        self.update()

    def add(self):
        songpath = filedialog.askopenfilename(
            title="Выбрать файл", filetypes=[("Аудиофайлы", "*.mp3")]
        )
        if songpath != "":
            tag = TinyTag.get(songpath)
            song = {
                "path": songpath,
                "name": tag.title if tag.title else os.path.basename(songpath),
                "artist": tag.artist,
                "duration": tag.duration,
            }
            try:
                with open("playlist.json", "r", encoding="utf-8") as f:
                    play = json.load(f)
            except Exception:
                play = []
            if not any(s.get("path") == songpath for s in play):
                play.append(play, key=lambda play: play["name"])
                with open("playlist.json", "w", encoding="utf-8") as f:
                    json.dump(play, f)
                    self.setting.mlist = tk.StringVar(value="Выберите сонг")
                    self.setting.update_playlist()

    def skip_sec(self):
        if self.isplay:
            new_time = min(self.get_current_position() + 10, self.duration)
            pygame.mixer.music.play(start=new_time)
            self.music_start_time = time.time() - new_time
            self.update()

    def rewind(self, new_time):
        pygame.mixer.music.play(start=new_time)
        self.music_start_time = time.time() - new_time
        self.update()

    def return_sec(self):
        if self.isplay:
            new_time = max(self.get_current_position() - 10, 0)
            pygame.mixer.music.play(start=new_time)
            self.music_start_time = time.time() - new_time
            self.update()

    def volume_up(self):
        if self.isplay:
            self.volume = min(1.0, self.volume + 0.1)
            pygame.mixer.music.set_volume(self.volume)

    def volume_down(self):
        if self.isplay:
            self.volume = max(0.0, self.volume - 0.1)
            pygame.mixer.music.set_volume(self.volume)
