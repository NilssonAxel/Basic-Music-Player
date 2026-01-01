import sys
import tkinter as tk
import os
from PIL import ImageTk, Image
import pygame



pygame.init()


#pygame.mixer.music.load(r"D:\[Python Codes & HW\Music Player\assets\mp3_folder\TonyZ _ Road So Far _Inspired By Alan Walker_ _NCN Release_.mp3")
#pygame.mixer.music.play()
#pygame.mixer.music.play(-1)   # -1 = loop forever
#pygame.mixer.pause()
#pygame.mixer.unpause()


# Asset locator
def locate_assets(relative_path):
    if getattr(sys, "frozen", False):
        base_path1 = os.path.dirname(sys.executable)
    else:
        base_path1 = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path1, relative_path)

# Update Label with the current song
#def update_label(event):

# tkinter string variables

# Play song when double clicking listbox
def play_stop_song(*args):
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.stop()
        play_stop_button.configure(text="▶")
    else:
        play_stop_button.configure(text="⏸")
        index_lb = playlist.curselection()[0]
        song = playlist.get(index_lb)
        pygame.mixer.music.load(locate_assets("assets\\mp3_folder\\") + song)
        pygame.mixer.music.play()
        song_text.configure(text=song[0:25])

def stop_song(*args):
    pygame.mixer.music.stop()

# Change color scheme.
background_color = "grey"
button_style = {"font": ("Segoe UI", 16), "bg": "#3c3f41", "fg": "white", "bd": 0, "width": 4}

# Main window Gui
main_window = tk.Tk()
main_window.geometry("300x600")
main_window.title("Music Player by Richard Gunnarsson")
main_window.grid_columnconfigure(0, weight=1)
main_window.grid_rowconfigure(2, weight=1)
main_window.grid_propagate(False)

# Get logo
try:
    if hasattr(sys, "_MEIPASS"):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    icon_path = os.path.join(base_path, "assets", "logo.png")
    logo = Image.open(icon_path)
    logo = ImageTk.PhotoImage(logo)
    main_window.iconphoto(True, logo)
except:
    pass

# TOP Control frame
control_frame = tk.Frame(main_window, bg=background_color, width=300, height=160)
control_frame.grid(row=0, column=0, sticky="nsew")
#control_frame.grid_propagate(False)
control_frame.grid_columnconfigure([0,1,2,3], weight=1)

# TOP Control Buttons
play_button = tk.Button(control_frame, text="⏮️", **button_style)
play_stop_button = tk.Button(control_frame, text="▶", command = play_stop_song, **button_style)
random_button = tk.Button(control_frame, text="⏭️", **button_style)
#🔀⏸
play_button.grid(row=0, column=0, padx=5, pady=10, sticky="nsew")
play_stop_button.grid(row=0, column=1, padx=5, pady=10, sticky="nsew")
random_button.grid(row=0, column=2, padx=5, pady=10, sticky="nsew")

# TOP Control Search Entry
search_entry = tk.Entry(control_frame, bg=background_color, font=("Segoe UI", 16))
search_entry.grid(row=1, column=0, columnspan=3, sticky="nsew")
search_entry.grid_rowconfigure(1, weight=0)
search_entry.grid_columnconfigure(0, weight=0)

# TOP Control Song Text Window
song_text = tk.Label(control_frame, text="let's play some music.", **button_style)
song_text.grid(row=2, column=0, columnspan=3, sticky="nsew")
song_text.grid_rowconfigure(2, weight=0)
song_text.grid_columnconfigure(0, weight=1)

# LOWER Playlist
playlist = tk.Listbox(main_window, bg=background_color, selectmode = tk.SINGLE, highlightthickness=0)
playlist.grid(row=2, column=0, sticky="nsew")
mp3_list = [file for file in os.listdir(locate_assets("assets/mp3_folder")) if file.endswith(".mp3")]
for index, song in enumerate(mp3_list, start=1):
    playlist.insert(tk.END, song)


# Binds
playlist.bind("<Double-Button-1>", play_stop_song)


if __name__ == "__main__":
    main_window.mainloop()
