import os
import tkinter as tk
from tkinter import filedialog, messagebox
import ffmpeg
from tqdm import tqdm

def confirm_delete_hidden_files(folder):
    delete = messagebox.askyesno("Confirm", "Do you want to delete files starting with a dot?")
    if delete:
        delete_hidden_files(folder)

def delete_hidden_files(folder):
    for root_dir, dirs, files in os.walk(folder):
        for file in files:
            if file.startswith("."):
                file_path = os.path.join(root_dir, file)
                os.remove(file_path)
                print(f"File deleted: {file_path}")

def confirm_identify_audio_type(folder):
    if not contains_labeled_files(folder):
        identify = messagebox.askyesno("Confirm", "Do you want to identify the audio type (mono/stereo) of the files?")
        if identify:
            identify_audio_type(folder)

def contains_labeled_files(folder):
    for root_dir, _, files in os.walk(folder):
        for file in files:
            if "(mono)" in file or "(stereo)" in file:
                return True
    return False

def identify_audio_type(folder):
    for root_dir, _, files in os.walk(folder):
        wav_files = [file for file in files if file.endswith(".wav")]
        with tqdm(total=len(wav_files), desc=f"Processing files in {root_dir}") as pbar:
            for file in wav_files:
                if "(mono)" in file or "(stereo)" in file:
                    continue  # Skip files already labeled
                original_path = os.path.join(root_dir, file)
                audio_type = get_audio_type(original_path)
                if audio_type:
                    new_name = f"{os.path.splitext(file)[0]} ({audio_type}).wav"
                    try:
                        os.rename(original_path, os.path.join(root_dir, new_name))
                    except Exception as e:
                        print("Error renaming file:", e)
                pbar.update(1)

def get_audio_type(file):
    try:
        info = ffmpeg.probe(file, cmd='C:/ffmpeg/bin/ffprobe.exe')
        num_channels = info['streams'][0]['channels']
        if num_channels == 1:
            return "mono"
        elif num_channels == 2:
            channel_type = detect_audio_type(file)
            if channel_type == "False stereo":
                return "mono"
            else:
                return "stereo"
        else:
            return "unknown"
    except Exception as e:
        print("Error obtaining file information:", e)
        return None

def detect_audio_type(file):
    try:
        import soundfile as sf
        import numpy as np

        data, _ = sf.read(file)

        if len(data.shape) == 1 or data.shape[1] == 1:
            return "Mono"

        if data.shape[1] == 2:
            left_channel = data[:, 0]
            right_channel = data[:, 1]
            correlation = np.corrcoef(left_channel, right_channel)[0, 1]

            if correlation > 0.95:
                return "False stereo"

            return "True stereo"

        return "Unknown"
    except Exception as e:
        print("Error detecting audio type:", e)
        return "Unknown"

def confirm_reorder_files(folder):
    wav_files = [file for file in os.listdir(folder) if file.endswith(".wav")]
    if wav_files:
        reorder = messagebox.askyesno("Confirm", "Do you want to reorder the files into folders?")
        if reorder:
            reorder_files(folder)
    else:
        print("No .wav files found in the folder. Exiting the program.")

def reorder_files(folder):
    app = FileOrdererApp(folder)
    app.run()

class FileOrdererApp:
    def __init__(self, folder):
        self.folder = folder
        self.elements = []
        self.categories = ["01- DRUMS", "02- PERCUSSION", "03- BASS", "04- GUITARS", "05- KEYS, SYNTHS, FX, ETC", "06- VOCALS"]
        self.populate_files()
        self.create_widgets()

    def populate_files(self):
        self.files = [os.path.join(self.folder, f) for f in os.listdir(self.folder) if os.path.isfile(os.path.join(self.folder, f)) and not f.startswith(".")]
        self.elements.extend(self.files)
        self.elements.extend(self.categories)

    def create_widgets(self):
        self.root = tk.Tk()
        self.listbox = tk.Listbox(self.root, selectmode=tk.SINGLE)
        for item in self.elements:
            self.listbox.insert(tk.END, os.path.basename(item) if os.path.isfile(item) else item)
        self.listbox.pack(expand=True, fill=tk.BOTH)

        self.listbox.bind("<Button-1>", self.on_select)
        self.listbox.bind("<B1-Motion>", self.on_motion)
        self.listbox.bind("<ButtonRelease-1>", self.on_release)

        self.rename_button = tk.Button(self.root, text="OK", command=self.rename_files)
        self.rename_button.pack(pady=5)

        self.drag_data = {"x": 0, "y": 0, "index": None}

    def on_select(self, event):
        widget = event.widget
        self.drag_data["index"] = widget.nearest(event.y)

    def on_motion(self, event):
        widget = event.widget
        current_index = widget.nearest(event.y)
        if self.drag_data["index"] is not None and current_index != self.drag_data["index"]:
            if 0 <= self.drag_data["index"] < len(self.elements) and 0 <= current_index < len(self.elements):
                self.elements.insert(current_index, self.elements.pop(self.drag_data["index"]))
                self.update_listbox()
                self.drag_data["index"] = current_index

    def on_release(self, event):
        self.drag_data["index"] = None

    def update_listbox(self):
        self.listbox.delete(0, tk.END)
        for item in self.elements:
            self.listbox.insert(tk.END, os.path.basename(item) if os.path.isfile(item) else item)

    def rename_files(self):
        uncategorized_files = []
        for i, item in enumerate(self.elements):
            if os.path.isfile(item):
                folder_name = None
                for category in self.categories:
                    category_index = self.elements.index(category)
                    if category_index < i:
                        folder_name = category
                if folder_name:
                    folder_path = os.path.join(self.folder, folder_name)
                    os.makedirs(folder_path, exist_ok=True)
                    new_name = os.path.join(folder_path, f"{len(os.listdir(folder_path)) + 1:02d} - {os.path.basename(item)}")
                    try:
                        os.rename(item, new_name)
                    except Exception as e:
                        print("Error renaming file:", e)
                else:
                    uncategorized_files.append(item)
        for i, item in enumerate(uncategorized_files):
            new_name = os.path.join(self.folder, f"{i + 1:02d} - {os.path.basename(item)}")
            try:
                os.rename(item, new_name)
            except Exception as e:
                print("Error renaming file:", e)
        self.root.quit()

    def run(self):
        self.root.title("Reorder Your Tracks. IMPORTANT: DON'T CHANGE THE ORDER OF THE CATEGORIES")
        # Obtener las dimensiones de la pantalla
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Definir el tamaño y la posición de la ventana
        window_width = int(screen_width * 0.4)  # Ancho de la ventana
        window_height = int(screen_height * 0.4)  # Alto de la ventana
        x = (screen_width - window_width) // 2  # Posición x de la ventana
        y = (screen_height - window_height) // 2  # Posición y de la ventana

        # Configurar la geometría de la ventana
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.root.mainloop()

def select_folder():
    root = tk.Tk()
    root.withdraw()
    folder = filedialog.askdirectory(title="Select Folder")
    return folder

def main():
    folder = select_folder()
    if folder:
        if any(file.startswith(".") for file in os.listdir(folder)):
            confirm_delete_hidden_files(folder)
        confirm_identify_audio_type(folder)
        confirm_reorder_files(folder)
        print("Process completed.")
    else:
        print("No folder selected.")

if __name__ == "__main__":
    main()
