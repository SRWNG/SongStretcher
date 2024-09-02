import tkinter as tk
from tkinter import filedialog, ttk
import pydub
from pydub import AudioSegment
import os
import shutil

class Mp3SpeedChanger:
    def __init__(self, root):
        self.root = root
        self.root.title("MP3 SONG STRETCHER")
        self.root.geometry("400x250")  # Set the window size
        self.root.resizable(False, False)  # Make the window non-resizable

        # Set up FFmpeg environment variables
        os.environ["PATH"] += os.pathsep + r"C:\Program Files\ffmpeg\bin"
        AudioSegment.converter = r"C:\Program Files\ffmpeg\bin\ffmpeg.exe"
        AudioSegment.ffprobe = r"C:\Program Files\ffmpeg\bin\ffprobe.exe"

        # Create a label and button to select an MP3 file
        self.label = tk.Label(root, text="Select an MP3 file:", font=("Arial", 12))
        self.label.pack(pady=10)

        self.button = tk.Button(root, text="Browse", command=self.select_file, font=("Arial", 12), width=10)
        self.button.pack(pady=10)

        # Create a label and button to download the sped-up and slowed-down MP3 files
        self.download_label = tk.Label(root, text="Download sped-up and slowed-down MP3 files:", font=("Arial", 12))
        self.download_label.pack(pady=10)

        self.download_button = tk.Button(root, text="Download", command=self.download_files, state=tk.DISABLED, font=("Arial", 12), width=10)
        self.download_button.pack(pady=10)

        # Create a progress bar
        self.progress_bar = ttk.Progressbar(root, orient="horizontal", length=200, mode="determinate")
        self.progress_bar.pack(pady=10)

        # Initialize the file path and sped-up and slowed-down audio
        self.file_path = None
        self.sped_up_audio = None
        self.slowed_down_audio = None

    def select_file(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("MP3 files", "*.mp3")])
        if self.file_path:
            self.button.config(text="File selected!")
            self.speed_up_mp3()
            self.slow_down_mp3()
            self.download_button.config(state=tk.NORMAL)

    def speed_up_mp3(self):
        audio = pydub.AudioSegment.from_mp3(self.file_path)
        self.sped_up_audio = audio._spawn(audio.raw_data, overrides={"frame_rate": int(audio.frame_rate * 1.15)})

    def slow_down_mp3(self):
        audio = pydub.AudioSegment.from_mp3(self.file_path)
        self.slowed_down_audio = audio._spawn(audio.raw_data, overrides={"frame_rate": int(audio.frame_rate * 0.85)})

    def download_files(self):
        file_path, file_name = self.file_path.rsplit("/", 1)
        folder_name = f"Modified {file_name.rsplit('.', 1)[0]}"
        folder_path = f"{file_path}/{folder_name}"
        os.makedirs(folder_path, exist_ok=True)

        self.progress_bar.config(mode="indeterminate")
        self.progress_bar.start()

        new_file_name_spd = f"sped_up_{file_name}"
        new_file_name_slow = f"slowed_down_{file_name}"
        new_file_path_spd = f"{folder_path}/{new_file_name_spd}"
        new_file_path_slow = f"{folder_path}/{new_file_name_slow}"

        self.sped_up_audio.export(new_file_path_spd, format="mp3")
        self.slowed_down_audio.export(new_file_path_slow, format="mp3")

        self.progress_bar.stop()
        self.progress_bar.config(mode="determinate")
        self.progress_bar.config(value=100)

        print(f"Files saved in folder {folder_path}")
        tk.messagebox.showinfo("Download Complete", "Downloaded!")

root = tk.Tk()
app = Mp3SpeedChanger(root)
root.mainloop()