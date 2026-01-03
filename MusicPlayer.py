import sys
import tkinter as tk
import os
import random
from PIL import ImageTk, Image
import pygame

pygame.init()

# Class for shuffle button
class toggle_shuffle_button:
    def __init__(self, master_window):
        self.shuffle_on = False

        self.shuffle_button = tk.Button(control_frame, text="🔀", command = self.toggle_shuffle, **button_style)
        self.shuffle_button.grid(row=0, column=3, padx=5, pady=5, sticky="nsew")

    def toggle_shuffle(self):
        self.shuffle_on = not self.shuffle_on
        self.update_shuffle_button()

    def update_shuffle_button(self):
        if self.shuffle_on:
            self.shuffle_button.configure(fg="green")
            randomize_playlist()
        else:
            self.shuffle_button.configure(fg="white")

# Open configuration or create one # TODO INSERT TRY
def open_cfg_file():
    if os.path.exists("cfg.txt"):
        with open("cfg.txt", "rb") as f:
            config = f.read()
        if int(config) == 0x00:
            with open("data.txt", "w") as c:
                c.write("")
        elif int(config) == 0x01:
            print("config01")
        else:
            reset_cfg()
    else:
        reset_cfg()
# Reset cfg if corrupted
def reset_cfg():
    with open("cfg.txt", "wb") as f:
        f.write(b"00")
    open_cfg_file()

# Asset locator
def locate_assets(relative_path):
    if getattr(sys, "frozen", False):
        base_path1 = os.path.dirname(sys.executable)
    else:
        base_path1 = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path1, relative_path)
# w/r from txt file
def open_write(song):
    with open("data.txt", "a") as f:
        f.writelines(song + ",")
    return
def open_read():
    with open(locate_assets("data.txt"), "r") as f:
        current_song = f.readline()
    return current_song
# Randomize playlist
def randomize_playlist():
    all_songs = [file for file in os.listdir(locate_assets("assets\\mp3_folder"))]
    random.shuffle(all_songs)
    #pygame.mixer.init()
    with open("random.txt", "w") as f:
        for song in all_songs:
            f.writeline(song + ", ")
# Play from the randomized playlist
def play_randomized_playlist():
    with open("random.txt", "r") as f:
        all_songs = [line.strip() for line in f]
    next_random_song = all_songs.pop()
    #with open("random.txt", "w") as f:
    pygame.mixer.music.load(next_random_song)
    pygame.mixer.music.play()
# Just randomize the next song
def randomize_next_song():
    all_songs = [file for file in os.listdir(locate_assets("assets\\mp3_folder"))]
    random.shuffle(all_songs)
    next_song = all_songs.pop()
    pygame.mixer.music.load(locate_assets("assets\\mp3_folder\\") + next_song)
    pygame.mixer.music.play()
    open_write(next_song)
    song_text.configure(text=next_song[0:25])
# Search function
def search_song(event=None):
    query = search_entry.get().lower()
    mp3_list = [file for file in os.listdir(locate_assets("assets\\mp3_folder\\")) if file.endswith(".mp3")]
    if query == "":
        update_playlist("every_song")
    else:
        filtered_list = [song for song in mp3_list if query in song.lower()]
        update_playlist(filtered_list)
# Playlist update
def update_playlist(filtered_list):
    mp3_list = [file for file in os.listdir(locate_assets("assets\\mp3_folder\\")) if file.endswith(".mp3")]
    playlist.delete(0, tk.END)
    if filtered_list == "every_song":
        for index, song in enumerate(mp3_list, start=1):
            line = f"{index}. {song}"
            playlist.insert(tk.END, line)
    else:
        for index, song in enumerate(filtered_list, start=1):
            line = f"{index}. {song}"
            playlist.insert(tk.END, line)


# Play song when double clicking listbox
def play_stop_song(origin):
    index_lb = playlist.curselection()[0]
    chosen_song = playlist.get(index_lb)
    chosen_song = chosen_song.split(". ", 1)[1]
    current_song = open_read()
    if pygame.mixer.music.get_busy() and origin == "Button":
        pygame.mixer.music.pause()
        play_stop_button.configure(text="▶")
    elif origin == "DoubleClick":
        pygame.mixer.music.load(locate_assets("assets\\mp3_folder\\") + chosen_song)
        pygame.mixer.music.play()
        play_stop_button.configure(text="⏸")
        open_write(chosen_song)
        song_text.configure(text=chosen_song[0:25])
    elif pygame.mixer.music.get_pos() >= 0 and current_song == chosen_song:
        pygame.mixer.music.unpause()
        play_stop_button.configure(text="⏸")
    else:
        play_stop_button.configure(text="⏸")
        if tsb.shuffle_on:
            randomize_playlist()
        else:
            randomize_next_song()

def next_song():
    if tsb.shuffle_on:
        randomize_playlist()
    else:
        randomize_next_song()
# Just reset the current song
def previous_song():
    pygame.mixer.music.play()

def shuffle_songs():
    shuffle_button.configure(fg="green")

# Change color scheme.
background_color = "grey"
button_style = {"font": ("Segoe UI", 16), "bg": "#3c3f41", "fg": "white", "bd": 0}

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
control_frame.grid_columnconfigure([0,1,2], weight=1)
control_frame.grid_rowconfigure([0,1,2], weight=1)
# TOP Control Buttons
previous_button = tk.Button(control_frame, text="⏮️", command= previous_song, **button_style)
play_stop_button = tk.Button(control_frame, text="▶", command = lambda event = None: play_stop_song("Button"), **button_style)
next_button = tk.Button(control_frame, text="⏭️", command = next_song, **button_style)
#shuffle_button = tk.Button(control_frame, text="🔀", command = self.toggle_shuffle, **button_style)
#⏸
previous_button.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
play_stop_button.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
next_button.grid(row=0, column=2, padx=5, pady=5, sticky="nsew")
#shuffle_button.grid(row=0, column=3, padx=5, pady=5, sticky="nsew")
# TOP Control Search Entry
search_entry = tk.Entry(control_frame, bg="#3c3f41", fg="white", insertbackground="white", font=("Segoe UI", 10))
search_entry.grid(row=1, column=0, columnspan=4, padx=5, sticky="nsew")
# TOP Control Song Text Window
song_text = tk.Label(control_frame, height=1, text="let's play some music.", **button_style)
song_text.grid(row=2, column=0, columnspan=4, padx=5, pady=5, sticky="nsew")
# LOWER Playlist
playlist = tk.Listbox(main_window, bg=background_color, selectmode = tk.SINGLE, highlightthickness=0)
playlist.grid(row=2, column=0, columnspan=4, sticky="nsew")

# Binds
playlist.bind("<Double-Button-1>", lambda event = None: play_stop_song("DoubleClick"))
search_entry.bind("<KeyRelease>", search_song)

if __name__ == "__main__":
    open_cfg_file()
    tsb = toggle_shuffle_button(main_window)
    update_playlist("every_song")
    main_window.mainloop()
