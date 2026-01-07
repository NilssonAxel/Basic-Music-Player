import sys
import tkinter as tk
import os
import random
from PIL import ImageTk, Image
import pygame
import threading
import time

pygame.init()
# Main window Gui
main_window = tk.Tk()
main_window.geometry("300x600")
main_window.title("Music Player by Richard Gunnarsson")
main_window.grid_columnconfigure(0, weight=1)
main_window.grid_rowconfigure(2, weight=1)
main_window.grid_propagate(False)
# Change color scheme.
background_color = "grey"
button_style = {"font": ("Segoe UI", 16), "bg": "#3c3f41", "fg": "white", "bd": 0}
# Asset locator
def locate_assets(relative_path):
    if getattr(sys, "frozen", False):
        base_path1 = os.path.dirname(sys.executable)
    else:
        base_path1 = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path1, relative_path)
to_pm3_folder = locate_assets("assets\\mp3_folder\\")
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
            with open(locate_assets("cfg.txt"), "wb") as f:
                f.write(b"01")
            reset_randomized_playlist()
        else:
            self.shuffle_button.configure(fg="white")
            with open(locate_assets("cfg.txt"), "wb") as f:
                f.write(b"00")
# Class mp3Rename and error window
class Mp3Renamer:
    def __init__(self, main_window):
        self.main_window = main_window
        self.error_window = None
        self.error_label = None
        self.change_button = None
        self.ignore_button = None

    def check_mp3_names(self, control):
        weird_names = self.find_weird_names()

        if control:
            self.rename_files(weird_names)
            self.update_existing_window(weird_names)
        else:
            if len(weird_names) > 0:
                self.show_error_window(weird_names)

    def find_weird_names(self):
        weird = []
        for old_name in os.listdir(locate_assets("assets\\mp3_folder\\")):
            if any(ord(ch) > 127 for ch in old_name):
                weird.append(old_name)
        return weird

    def rename_files(self, weird_names):
        for old_name in weird_names:
            new_name = ''.join(ch if ord(ch) < 128 else 'a' for ch in old_name)
            os.rename(
                os.path.join(locate_assets("assets/mp3_folder"), old_name),
                os.path.join(locate_assets("assets/mp3_folder"), new_name)
            )

    def show_error_window(self, weird_names):
        self.error_window = tk.Toplevel(self.main_window, bg=background_color)
        self.error_window.geometry(get_display_resolution("error"))
        self.error_window.title("ERROR - Rename mp3 files")

        text = "\n".join(weird_names)
        self.error_label = tk.Label(
            self.error_window,
            text=f"These mp3 need to be renamed:\n{text}",
            bg=background_color,
            fg="purple"
        )
        self.error_label.pack(fill="x", padx=20, pady=10)

        self.change_button = tk.Button(
            self.error_window,
            text="Change mp3 names and close",
            command=lambda: self.check_mp3_names(True),
            **button_style
        )
        self.change_button.pack(side="bottom")

        self.ignore_button = tk.Button(
            self.error_window,
            text="Ignore, close",
            command=self.error_window.destroy,
            **button_style
        )
        self.ignore_button.pack(side="bottom")

    def update_existing_window(self, weird_names):
        text = "\n".join(weird_names)
        self.error_label.configure(text=f"These were changed:\n{text}")
        self.change_button.destroy()
        self.ignore_button.configure(bg="green", text="Close")

# Get display resolution
def get_display_resolution(window):
    sw = main_window.winfo_screenwidth()
    sh = main_window.winfo_screenheight()
    if window == "main":
        mww = 300
        mwh = 600
        x = sw // 3
        y = sh // 3
        return f"{mww}x{mwh}+{x}+{y}"
    else:
        eww = 300
        ewh = 600
        x = sw // 3 + 300
        y = sh // 3
        return f"{eww}x{ewh}+{x}+{y}"

# Open configuration or create one
def open_cfg_file():
    if os.path.exists("cfg.txt"):
        with open(locate_assets("cfg.txt"), "rb") as f:
            config = f.read()
        if int(config) == 0x00: # Normal
            with open(locate_assets("random.txt"), "w") as c:
                c.write("")
        elif int(config) == 0x01: # Shuffle button ON
            tsb.toggle_shuffle()
        else:
            reset_cfg()
    else:
        reset_cfg()
# Reset cfg if corrupted
def reset_cfg():
    with open(locate_assets("cfg.txt"), "wb") as f:
        f.write(b"00")
    open_cfg_file()

# w/r from txt file - Use to check played song and perhaps previous played songs
def open_write(song):
    with open(locate_assets("data.txt"), "a") as f:
        f.write(song + ",")
    return
def open_read():
    with open(locate_assets("data.txt"), "r") as f:
        current_song = f.readline()
    return current_song
# Get a random playlist back
def get_randomized_playlist():
    all_songs = [file for file in os.listdir(locate_assets("assets\\mp3_folder"))]
    random.shuffle(all_songs)
    return all_songs
# Get a random song
def get_random_song():
    all_songs = [file for file in os.listdir(locate_assets("assets\\mp3_folder"))]
    random.shuffle(all_songs)
    next_random_song = all_songs.pop(random.randrange(len(all_songs)))
    return next_random_song
# Reset playlist when pressing shuffle-button, so songs can be added and ignored
def reset_randomized_playlist():
    with open(locate_assets("random.txt"), "w") as f:
        f.write("")
# Play from the randomized playlist
def get_randomized_playlist_song():
    played_songs = open(locate_assets("random.txt"), "r").readlines()
    all_songs = [file for file in os.listdir(locate_assets("assets\\mp3_folder"))]
    random_song = list(set(all_songs) - set(played_songs))
    next_random_song = random_song.pop(random.randrange(len(all_songs)))
    with open("random.txt", "a") as f:
        f.write(next_random_song)
    open_write(next_random_song)
    song_text.configure(text=next_random_song[0:25])
    pygame.mixer.music.load(locate_assets("assets\\mp3_folder\\") + next_random_song)
    pygame.mixer.music.play()
# Just randomize the next song
def randomize_next_song():
    all_songs = [file for file in os.listdir(locate_assets("assets\\mp3_folder"))]
    next_song = all_songs.pop(random.randrange(len(all_songs)))
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
    try:
        index_lb = playlist.curselection()[0]
        chosen_song = playlist.get(index_lb)
        chosen_song = chosen_song.split(". ", 1)[1]
        current_song = open_read()
    except:
        chosen_song = True
        current_song = False
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
            get_randomized_playlist_song()
        else:
            randomize_next_song()
# When pressing the forward button
def next_song():
    if tsb.shuffle_on:
        play_stop_button.configure(text="⏸")
        get_randomized_playlist_song()
    else:
        play_stop_button.configure(text="⏸")
        randomize_next_song()
# Just reset the current song
def previous_song():
    pygame.mixer.music.play()
# while true loop when playing
pygame.mixer.init()
next_song_event = pygame.USEREVENT + 1
pygame.mixer.music.set_endevent(next_song_event)

def check_for_song_end():
    for event in pygame.event.get():
        if event.type == next_song_event:
            play_stop_song("pygame_event")

    main_window.after(1000, check_for_song_end)  # schedule next check


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
previous_button.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
play_stop_button.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
next_button.grid(row=0, column=2, padx=5, pady=5, sticky="nsew")
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
# Threading?
standby_music = threading.Thread(target=check_for_song_end)
standby_music.start()
main_window.geometry(get_display_resolution("main"))

if __name__ == "__main__":
    tsb = toggle_shuffle_button(main_window)
    open_cfg_file()
    update_playlist("every_song")
    main_window.after(1000, Mp3Renamer(main_window).check_mp3_names, False)
    main_window.mainloop()
