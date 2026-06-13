import tkinter as tk
import sliders
import interfaces
import settings
import song
import keyboard


def on_key(event):
    if event.keycode == 32:
        player.pause()
    elif event.keycode == 39:
        player.skip_sec()
    elif event.keycode == 37:
        player.return_sec()
    elif event.keycode == 38:
        player.volume_up()
    elif event.keycode == 40:
        player.volume_down()
    elif event.keycode == 83:
        interface.toggle_setting()
    # print(event)


root = tk.Tk()
root.geometry('500x600')
root.title("MySpotty!")
root.resizable(False, False)

canvas = tk.Canvas(root, width=500, height=600, bg='#F3F4ED')
canvas.pack(side='left')

player = song.Song(canvas, root)
slider = sliders.Slider(canvas, 40, 440, 20, player,
                        bounds=(40, 440, 460, 460))
interface = interfaces.Interface(canvas, player, root, slider)
setting = settings.Setting(root, player, interface)
player.slider, player.interface, player.setting, interface.setting = slider, interface, setting, setting
interface.song = player

keyboard.hook(lambda e: player.pause() if e.name ==
              "play/pause media" else None)  # -179
# keyboard.hook(lambda e: player.skip_sec() if e == keyboard.KeyboardEvent(
#    name='right', event_type='down', scan_code=77) else None)  # 77
# keyboard.hook(lambda e: player.return_sec() if e == keyboard.KeyboardEvent(name='left',
#              event_type='down', scan_code=75) else None)
# keyboard.hook(lambda e: player.pause() if e ==
#              keyboard.KeyboardEvent(name='space', event_type='down', scan_code=57) else None)

root.bind("<KeyPress>", on_key)


root.mainloop()