import os
import tkinter as tk
from tkinter import filedialog, messagebox
import ffmpeg
from tqdm import tqdm
import scipy.io.wavfile as wav
import soundfile as sf
import numpy as np
import re
import webbrowser

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
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        window_width = int(screen_width * 0.4)
        window_height = int(screen_height * 0.4)
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.root.mainloop()

def select_folder():
    root = tk.Tk()
    root.withdraw()
    folder = filedialog.askdirectory(title="Select Folder")
    return folder

def show_donation_dialog():
    root = tk.Tk()
    root.withdraw()
    donation_message = "Created by Doc Shadrach.\n\nThis is free, but if this program is helpful to you, saves your time (and money), and you appreciate all my work, you might consider making a donation."
    response = messagebox.askyesno("Donate to Support", donation_message, detail="Do you want to make a donation?", icon="info")
    if response:
        webbrowser.open("https://ko-fi.com/docshadrach")
    root.destroy()

def main():
    current_directory = os.getcwd().replace("\\", "/") + "/ffprobe.exe"  # Convertir \ a / y agregar /ffprobe.exe al final
    print("Current directory:", current_directory)
    folder = select_folder()
    if folder:
        if any(file.startswith(".") for file in os.listdir(folder)):
            confirm_delete_hidden_files(folder)
        confirm_identify_audio_type(folder, current_directory)  # Pasar la ubicación del ffprobe como parámetro
        confirm_convert_dualmono_to_mono(folder)
        confirm_convert_LR_to_stereo(folder)
        confirm_reorder_files(folder)  # Confirmar la reordenación después de todas las conversiones
        print("Process completed.")
        show_donation_dialog()
    else:
        print("No folder selected.")

def show_dualmono_files(dualmono_files):
    filenames = [os.path.basename(file_path).replace('(dualmono).wav', '') for file_path in dualmono_files]
    messagebox.showinfo("Dualmono Files Found", "\n".join(filenames))

def show_LR_files(matching_files):
    lr_pairs = []
    for base_name_lower, files in matching_files.items():
        left_files = [file for file in files if re.search(r'\bL\b|\bleft\b', file, re.IGNORECASE)]
        right_files = [file for file in files if re.search(r'\bR\b|\bright\b', file, re.IGNORECASE)]
        if len(left_files) == 1 and len(right_files) == 1:
            lr_pairs.append((left_files[0], right_files[0]))

    if lr_pairs:
        messagebox.showinfo("LR Files Found", "\n".join([f"Left: {os.path.basename(left)} - Right: {os.path.basename(right)}" for left, right in lr_pairs]))
        return True
    else:
        print("No matching L/R pairs found.")
        return False

def convert_dualmono_to_mono(dualmono_files):
    show_dualmono_files(dualmono_files)  # Mostrar los nombres de los archivos dualmono
    convert = messagebox.askyesno("Confirm", "Do you want to convert dualmono files to mono?")
    if convert:
        for file_path in dualmono_files:
            try:
                # Leer el archivo de audio
                original_sample_rate, original_data = wav.read(file_path)

                # Tomar solo el canal izquierdo
                if original_data.ndim == 2:  # Verificar si el archivo es estéreo
                    mono_data = original_data[:, 0]  # Tomar solo el primer canal (izquierdo)
                else:
                    mono_data = original_data  # Si es mono, no hay necesidad de cambiar nada

                # Guardar el archivo mono
                output_file_path = file_path.replace('(dualmono).wav', '(mono).wav')
                wav.write(output_file_path, original_sample_rate, mono_data)

                print(f"Archivo mono generado: {output_file_path}")

                # Eliminar el archivo original (dualmono)
                os.remove(file_path)
                print(f"Archivo dualmono eliminado: {file_path}")

            except Exception as e:
                print("Error converting file:", e)

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

def confirm_identify_audio_type(folder, ffprobe_path):
    if not contains_labeled_files(folder):
        identify = messagebox.askyesno("Confirm", "Do you want to identify the audio type (mono/stereo) of the files?")
        if identify:
            identify_audio_type(folder, ffprobe_path)  # Pasar la ubicación del ffprobe como parámetro

def contains_labeled_files(folder):
    for root_dir, _, files in os.walk(folder):
        for file in files:
            if "(mono)" in file or "(stereo)" in file:
                return True
    return False

def identify_audio_type(folder, ffprobe_path):
    dualmono_files = []
    for root_dir, _, files in os.walk(folder):
        wav_files = [file for file in files if file.endswith(".wav")]
        with tqdm(total=len(wav_files), desc=f"Processing files in {root_dir}") as pbar:
            for file in wav_files:
                if "(mono)" in file or "(stereo)" in file:
                    continue  # Skip files already labeled
                original_path = os.path.join(root_dir, file)
                audio_type = get_audio_type(original_path, ffprobe_path)  # Pasar la ubicación del ffprobe como parámetro
                if audio_type:
                    new_name = f"{os.path.splitext(file)[0]} ({audio_type}).wav"
                    try:
                        os.rename(original_path, os.path.join(root_dir, new_name))
                    except Exception as e:
                        print("Error renaming file:", e)
                pbar.update(1)
                if audio_type == "dualmono":
                    dualmono_files.append(os.path.join(root_dir, new_name))  # Usar el nombre modificado
    if dualmono_files:
        convert_dualmono_to_mono(dualmono_files)

def get_audio_type(file, ffprobe_path):
    try:
        info = ffmpeg.probe(file, cmd=ffprobe_path)
        num_channels = info['streams'][0]['channels']
        if num_channels == 1:
            return "mono"
        elif num_channels == 2:
            channel_type = detect_audio_type(file)
            if channel_type == "False stereo":
                return "dualmono"
            else:
                return "stereo"
        else:
            return "unknown"
    except Exception as e:
        print("Error obtaining file information:", e)
        return None

def detect_audio_type(file):
    try:
        data, _ = sf.read(file)

        if len(data.shape) == 1 or data.shape[1] == 1:
            return "Mono"

        if data.shape[1] == 2:
            left_channel = data[:, 0]
            right_channel = data[:, 1]

            absolute_difference = np.abs(left_channel - right_channel)
            tolerance = 1e-10

            if np.all(absolute_difference < tolerance):
                return "False stereo"
            else:
                return "True stereo"

        return "Unknown"
    except Exception as e:
        print("Error detecting audio type:", e)
        return "Unknown"

def confirm_convert_dualmono_to_mono(folder):
    dualmono_files = [file for file in os.listdir(folder) if file.lower().endswith("(dualmono).wav")]
    if dualmono_files:
        convert = messagebox.askyesno("Confirm", "Do you want to convert dualmono files to mono?")
        if convert:
            dualmono_paths = [os.path.join(folder, file) for file in dualmono_files]
            convert_dualmono_to_mono(dualmono_paths)

def confirm_convert_LR_to_stereo(folder):
    matching_files = find_matching_files(folder)
    if matching_files:
        lr_files_found = show_LR_files(matching_files)  # Mostrar los archivos L y R encontrados
        if lr_files_found:
            convert = messagebox.askyesno("Confirm", "Do you want to convert L/R files to stereo?")
            if convert:
                for base_name_lower, files in matching_files.items():
                    if len(files) > 1:
                        left_files = [file for file in files if re.search(r'\bL\b|\bleft\b', file, re.IGNORECASE)]
                        right_files = [file for file in files if re.search(r'\bR\b|\bright\b', file, re.IGNORECASE)]
                        if len(left_files) == 1 and len(right_files) == 1:
                            convert_to_stereo(left_files[0], right_files[0])
    else:
        print("No matching L/R pairs found in the folder.")

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

def find_matching_files(folder_path):
    matching_files = {}
    for root_folder, _, files in os.walk(folder_path):
        for file in files:
            if file.startswith('.'):
                continue
            
            match = re.match(r'(.+?)\s*(?:left|right|l|r)?(?:\s*\(.*?\))?\.(.+)', file, re.IGNORECASE)
            if match:
                base_name = match.group(1)
                base_name_lower = base_name.lower()
                if base_name_lower in matching_files:
                    matching_files[base_name_lower].append(os.path.join(root_folder, file))
                else:
                    matching_files[base_name_lower] = [os.path.join(root_folder, file)]
    return matching_files

def convert_to_mono(file_path):
    sample_rate, data = wav.read(file_path)
    
    # Si el archivo ya tiene la marca "(mono)", no es necesario convertirlo
    if "(mono)" not in file_path.lower():
        # Si el archivo tiene la marca "(dualmono)", convertirlo a mono
        if "(dualmono)" in file_path.lower():
            data = np.mean(data, axis=1, dtype=np.int16)  # Promediar los dos canales para convertir a mono
        
        # Actualizar el nombre del archivo agregando "(mono)"
        file_name, file_ext = os.path.splitext(file_path)
        new_file_path = f"{file_name} (mono){file_ext}"
        
        # Guardar el archivo convertido a mono
        wav.write(new_file_path, sample_rate, data)
        print(f"Archivo convertido a mono: {file_path} -> {new_file_path}")
        
        return new_file_path
    else:
        return file_path

def convert_to_stereo(left_file_path, right_file_path):
    left_sample_rate, left_data = wav.read(left_file_path)
    right_sample_rate, right_data = wav.read(right_file_path)
    
    # Ajustar la longitud de los datos al mínimo de ambos canales
    min_len = min(len(left_data), len(right_data))
    left_data = left_data[:min_len]
    right_data = right_data[:min_len]
    
    # Combinar los canales izquierdo y derecho para formar el estéreo
    stereo_data = np.column_stack((left_data, right_data))
    
    # Obtener el nombre base del archivo estéreo
    base_name_left = os.path.splitext(os.path.basename(left_file_path))[0]
    base_name_right = os.path.splitext(os.path.basename(right_file_path))[0] if right_file_path else None
    
    if base_name_right:
        base_name_stereo = ''
        for c1, c2 in zip(base_name_left, base_name_right):
            if c1.lower() == c2.lower():
                base_name_stereo += c1
            else:
                break
    else:
        base_name_stereo = base_name_left
            
    # Guardar el archivo estéreo
    output_file = os.path.join(os.path.dirname(left_file_path), f"{base_name_stereo}(stereo).wav")
    wav.write(output_file, left_sample_rate, stereo_data)
    print(f"Archivos mono convertidos a estéreo: {left_file_path} y {right_file_path} -> {output_file}")
    
    # Eliminar los archivos originales
    os.remove(left_file_path)
    if right_file_path:
        os.remove(right_file_path)

if __name__ == "__main__":
    main()
