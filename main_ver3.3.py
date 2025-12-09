import os
import platform
import tkinter as tk
from tkinter import ttk
import threading
from tkinter import filedialog, messagebox
import soundfile as sf
import numpy as np
import re
import webbrowser
import shutil

def get_operating_system():
    """
    Detect the current operating system.
    
    Returns:
        str: 'Windows', 'Darwin' (macOS), 'Linux', or 'Unknown'
    """
    system = platform.system()
    return system


class FileOrdererApp:
    def __init__(self, folder):
        self.folder = folder
        self.elements = []
        self.categories = ["01- DRUMS", "02- PERCUSSION", "03- BASS", "04- GUITARS", "05- KEYS, SYNTHS, FX, ETC", "06- VOCALS"]
        self.category_colors = {'01- DRUMS': ('white', 'blue'),
                                '02- PERCUSSION': ('white', 'green'),
                                '03- BASS': ('white', 'red'),
                                '04- GUITARS': ('white', 'orange'),
                                '05- KEYS, SYNTHS, FX, ETC': ('white', 'purple'),
                                '06- VOCALS': ('white', 'gray')}
        self.populate_files()
        self.create_widgets()

    def populate_files(self):
        self.files = [os.path.join(self.folder, f) for f in os.listdir(self.folder) if os.path.isfile(os.path.join(self.folder, f)) and not f.startswith(".")]
        self.elements.extend(self.files)
        self.elements.extend(self.categories)

    def create_widgets(self):
        self.root = tk.Tk()

        self.listbox_frame = tk.Frame(self.root)
        self.listbox_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.listbox = tk.Listbox(self.listbox_frame, selectmode=tk.SINGLE, bg='white', font=('Arial', 10))
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar = tk.Scrollbar(self.listbox_frame, orient=tk.VERTICAL, command=self.listbox.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.listbox.config(yscrollcommand=self.scrollbar.set)

        for item in self.elements:
            if item in self.categories:
                fg_color, bg_color = self.category_colors[item]
                self.listbox.insert(tk.END, item)
                self.listbox.itemconfig(tk.END, {'fg': fg_color, 'bg': bg_color})
            else:
                self.listbox.insert(tk.END, os.path.basename(item) if os.path.isfile(item) else item)

        self.rename_button = tk.Button(self.root, text="OK", command=self.rename_files)
        self.rename_button.pack(pady=5)

        self.drag_data = {"x": 0, "y": 0, "index": None}

        self.listbox.bind("<Button-1>", self.on_select)
        self.listbox.bind("<B1-Motion>", self.on_motion)
        self.listbox.bind("<ButtonRelease-1>", self.on_release)

    def on_select(self, event):
        widget = event.widget
        self.drag_data["index"] = widget.nearest(event.y)

    def on_motion(self, event):
        dragged_index = self.drag_data["index"]
        
        if dragged_index is None:
            return

        if self.elements[dragged_index] in self.categories:
            return

        widget = event.widget
        current_index = widget.nearest(event.y)

        if current_index != dragged_index:
            self.elements.insert(current_index, self.elements.pop(dragged_index))
            self.update_listbox()
            self.drag_data["index"] = current_index


    def on_release(self, event):
        self.drag_data["index"] = None

    def update_listbox(self):
        self.listbox.delete(0, tk.END)
        for item in self.elements:
            if item in self.categories:
                fg_color, bg_color = self.category_colors[item]
                self.listbox.insert(tk.END, item)
                self.listbox.itemconfig(tk.END, {'fg': fg_color, 'bg': bg_color})
            else:
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
        self.root.title("Reorder Your Tracks. NOTE: You can also leave files out of the categories.")
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        window_width = int(screen_width * 0.3)
        window_height = int(screen_height * 0.8)
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.root.mainloop()

def select_folder(root):
    folder = filedialog.askdirectory(parent=root, title="Select Folder")
    return folder

def show_donation_dialog(root):
    donation_message = "Created by Doc Shadrach.\n\nThis is free, but if this program is helpful to you, saves your time (and money), and you appreciate all my work, you might consider making a donation."
    response = messagebox.askyesno("Donate to Support", donation_message, 
                                 detail="Do you want to make a donation?", 
                                 icon="info", parent=root)
    if response:
        webbrowser.open("https://ko-fi.com/docshadrach")

def main():
    # Create single root window and hide it
    root = tk.Tk()
    root.withdraw()
    
    current_directory = os.getcwd()
    folder = select_folder(root)
    if folder:
        if any(file.startswith(".") for file in os.listdir(folder)):
            confirm_delete_hidden_files(folder)
        
        # Get identified dualmono files
        dualmono_files = confirm_identify_audio_type(folder)
        print(f"Dualmono files found: {dualmono_files}")  # Debug log
        
        # If there are dualmono files, show selection dialog
        if dualmono_files:
            print("Showing dualmono selection dialog...")  # Debug log
            confirm_convert_dualmono_to_mono(dualmono_files)
        
        # Continue with next steps
        confirm_convert_LR_to_stereo(folder)
        confirm_reorder_files(folder)
        print("Process completed.")
        show_donation_dialog(root)
    else:
        print("No folder selected.")
    
    # Clean up
    root.destroy()

def show_dualmono_files(dualmono_files):
    root = tk.Tk()
    root.title("Dualmono Files Found")
    
    # Main frame
    main_frame = tk.Frame(root)
    main_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
    
    # Label
    label = tk.Label(main_frame, text="Select files to convert from dualmono to mono:", font=('Arial', 10))
    label.pack(pady=5)
    
    # Listbox with checkboxes
    list_frame = tk.Frame(main_frame)
    list_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    scrollbar = tk.Scrollbar(list_frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    listbox = tk.Listbox(list_frame, selectmode=tk.MULTIPLE, 
                        yscrollcommand=scrollbar.set,
                        height=min(10, len(dualmono_files)),
                        width=70,
                        font=('Arial', 10))
    scrollbar.config(command=listbox.yview)
    
    for file_path in dualmono_files:
        listbox.insert(tk.END, os.path.basename(file_path).replace('(dualmono).wav', ''))
    
    # Select all items by default
    listbox.selection_set(0, tk.END)
    
    listbox.pack(fill=tk.BOTH, expand=True)
    
    # Selection buttons frame
    btn_frame = tk.Frame(main_frame)
    btn_frame.pack(pady=5)
    
    # Select All button
    select_all_btn = tk.Button(btn_frame, text="Select All", 
                             command=lambda: listbox.selection_set(0, tk.END))
    select_all_btn.pack(side=tk.LEFT, padx=5)
    
    # Deselect All button
    deselect_all_btn = tk.Button(btn_frame, text="Deselect All", 
                               command=lambda: listbox.selection_clear(0, tk.END))
    deselect_all_btn.pack(side=tk.LEFT, padx=5)
    
    # Store selected files
    selected_files = []
    
    # OK button
    def on_ok():
        nonlocal selected_files
        selected_indices = listbox.curselection()
        selected_files = [dualmono_files[i] for i in selected_indices]
        print(f"Selected files: {selected_files}")  # Debug log
        root.quit()  # Only closes mainloop, doesn't destroy window
    
    ok_btn = tk.Button(main_frame, text="OK", command=on_ok)
    ok_btn.pack(pady=5)
    

    # Set window size and center
    root.geometry("400x300")
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'400x300+{x}+{y}')
    
    root.mainloop()
    root.destroy()  # Destroys window after exiting mainloop
    print(f"Returning files: {selected_files}")  # Debug log
    return selected_files

def show_LR_pairs(matching_files):
    lr_pairs = []
    for normalized_name, files in matching_files.items():
        # More flexible detection for left/right files including common misspellings
        left_files = []
        right_files = []
        for file in files:
            # Check for left indicators (L, left, _L, _left) - case insensitive
            if re.search(r'(\bL\b|_L\b|\bleft\b|_left\b)', file, re.IGNORECASE):
                left_files.append(file)
            # Check for right indicators including misspellings (R, right, _R, _right, rigth, rigt, righ) - case insensitive
            elif re.search(r'(\bR\b|_R\b|\bright\b|_right\b|\brigth\b|\brigt\b|\brigh\b)', file, re.IGNORECASE):
                right_files.append(file)
        
        if len(left_files) == 1 and len(right_files) == 1:
            lr_pairs.append((left_files[0], right_files[0]))

    if not lr_pairs:
        print("No matching L/R pairs found.")
        return []

    root = tk.Tk()
    root.title("L/R Pairs Found")
    root.geometry("400x300")  # Slightly larger to accommodate buttons
    
    main_frame = tk.Frame(root)
    main_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
    
    label = tk.Label(main_frame, text="Select files to join L/R pair to stereo:", font=('Arial', 10))
    label.pack(pady=5)
    
    # Listbox frame
    list_frame = tk.Frame(main_frame)
    list_frame.pack(fill=tk.BOTH, expand=True)
    
    scrollbar = tk.Scrollbar(list_frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    listbox = tk.Listbox(list_frame, 
                        selectmode=tk.MULTIPLE,
                        yscrollcommand=scrollbar.set,
                        height=min(10, len(lr_pairs)),
                        width=70,
                        font=('Arial', 10))
    scrollbar.config(command=listbox.yview)
    
    for left, right in lr_pairs:
        left_name = os.path.basename(left)
        right_name = os.path.basename(right)
        display_text = f"{left_name[:30]}... | {right_name[:30]}..."
        listbox.insert(tk.END, display_text)
    
    # Select all by default
    listbox.selection_set(0, tk.END)
    
    listbox.pack(fill=tk.BOTH, expand=True)
    
    # Selection buttons frame (moved below listbox like in dualmono dialog)
    btn_frame = tk.Frame(main_frame)
    btn_frame.pack(pady=5)
    
    select_all_btn = tk.Button(btn_frame, text="Select All", 
                             command=lambda: listbox.selection_set(0, tk.END))
    select_all_btn.pack(side=tk.LEFT, padx=5)
    
    deselect_all_btn = tk.Button(btn_frame, text="Deselect All", 
                               command=lambda: listbox.selection_clear(0, tk.END))
    deselect_all_btn.pack(side=tk.LEFT, padx=5)
    
    selected_pairs = []
    
    def on_ok():
        nonlocal selected_pairs
        selected_indices = listbox.curselection()
        selected_pairs = [lr_pairs[i] for i in selected_indices]
        root.quit()
    
    ok_btn = tk.Button(main_frame, text="OK", command=on_ok)
    ok_btn.pack(pady=10)
    
    # Center window
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'+{x}+{y}')
    
    root.mainloop()
    root.destroy()
    return selected_pairs  # Only return selected pairs

def convert_dualmono_to_mono(dualmono_files, convert):
    if convert:
        progress_window = ProgressWindow("Converting dualmono to mono")
        total_files = len(dualmono_files)
        
        for i, file_path in enumerate(dualmono_files):
            progress_window.update(f"Processing: {os.path.basename(file_path)}", i, total_files)
            
            try:
                # Read original file preserving exact format
                file_info = sf.info(file_path)
                original_data, original_sample_rate = sf.read(file_path, always_2d=True)
                subtype = file_info.subtype

                # Check channels and select the appropriate one
                if original_data.shape[1] == 2:  # Check if file is stereo
                    left_channel = original_data[:, 0]
                    right_channel = original_data[:, 1]
                    
                    # Check if a channel is silent
                    left_silent = np.all(np.abs(left_channel) < 1e-10)
                    right_silent = np.all(np.abs(right_channel) < 1e-10)
                    
                    if left_silent or right_silent:
                        # Show informative message
                        silent_side = "left" if left_silent else "right"
                        print(f"File {os.path.basename(file_path)} has silent {silent_side} channel. Converting to mono using active channel.")
                        
                        if left_silent and not right_silent:
                            mono_data = right_channel  # Use right channel if left is silent
                        elif right_silent and not left_silent:
                            mono_data = left_channel  # Use left channel if right is silent
                        else:
                            mono_data = left_channel  # Default to left channel
                    else:
                        mono_data = left_channel  # Original behavior if both channels have audio
                else:
                    mono_data = original_data[:, 0] if original_data.ndim == 2 else original_data  # If mono, no change needed

                # Save mono file preserving original bit depth
                output_file_path = file_path.replace('(dualmono).wav', '(mono).wav')
                sf.write(output_file_path, mono_data, original_sample_rate, subtype=subtype)

                print(f"Mono file generated: {output_file_path}")

                # Move original (dualmono) file to OBSOLETE FILES folder
                obsolete_folder_path = os.path.join(os.path.dirname(file_path), "-- OBSOLETE FILES")
                os.makedirs(obsolete_folder_path, exist_ok=True)
                shutil.move(file_path, os.path.join(obsolete_folder_path, os.path.basename(file_path)))
                print(f"Dualmono file moved to OBSOLETE FILES folder: {file_path}")

            except Exception as e:
                print("Error converting file:", e)
                
        progress_window.root.destroy()

def confirm_convert_dualmono_to_mono(dualmono_files):
    if not dualmono_files:
        print("No dualmono files received for processing.")
        return True  # Continue with the flow

    selected_files = show_dualmono_files(dualmono_files)
    print(f"Selected files: {selected_files}")  # Debug log
    
    if not selected_files:  # If no files were selected
        print("Continuing with L/R files detection...")
        return True  # Continue with the flow
    
    # If there are selected files, convert them directly
    convert_dualmono_to_mono(selected_files, True)
    
    # Always continue with the flow after processing dualmono
    return True

def confirm_delete_hidden_files(folder):
    """
    Ask user if they want to delete hidden files (starting with '.').
    Only shows the dialog on Windows. On macOS, hidden files are system files
    and should not be deleted.
    """
    # Check operating system
    os_name = get_operating_system()
    
    if os_name == "Windows":
        # On Windows, hidden files starting with '.' are often temporary files
        delete = messagebox.askyesno("Confirm", 
            "Do you want to delete temporary files (files starting with '.')?\n\n"
            "These are often temporary files created by some applications.\n"
            "Note: This will permanently delete these files.")
        if delete:
            delete_hidden_files(folder)
    elif os_name == "Darwin":  # macOS
        # On macOS, files starting with '.' are system hidden files (like .DS_Store)
        # We should not delete them automatically
        print("macOS detected: Skipping hidden files deletion (system files)")
        return
    else:  # Linux or other
        # For other systems, ask with a generic message
        delete = messagebox.askyesno("Confirm",
            "Do you want to delete hidden files (files starting with '.')?\n\n"
            "These are typically hidden system or configuration files.\n"
            "Note: This will permanently delete these files.")
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
        identify = messagebox.askyesno("Confirm", "Do you want to identify the audio type (mono/stereo) of the files?\n\nThis will only label files, not convert them.")
        if identify:
            return identify_audio_type(folder)  # Returns found dualmono files
    return []

def contains_labeled_files(folder):
    for root_dir, _, files in os.walk(folder):
        for file in files:
            if "(mono)" in file or "(stereo)" in file:
                return True
    return False

class ProgressWindow:
    def __init__(self, title="Progress"):
        self.root = tk.Toplevel()
        self.root.withdraw()  # Hide window initially
        self.root.title(title)
        
        # Main frame
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Center window on screen
        self.root.update_idletasks()
        width = 600
        height = 400
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        self.root.deiconify()  # Show window after positioning
        
        # Progress section
        progress_frame = tk.Frame(main_frame)
        progress_frame.pack(fill=tk.X, pady=5)
        
        self.status_label = tk.Label(progress_frame, text="Preparing...", font=('Arial', 10, 'bold'))
        self.status_label.pack()
        
        self.progress = ttk.Progressbar(progress_frame, orient="horizontal", length=500, mode="determinate")
        self.progress.pack(pady=5)
        
        self.percent_label = tk.Label(progress_frame, text="0%", font=('Arial', 10))
        self.percent_label.pack()
        
        # Log section
        log_frame = tk.Frame(main_frame)
        log_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.log_label = tk.Label(log_frame, text="Activity log:", font=('Arial', 10))
        self.log_label.pack(anchor=tk.W)
        
        self.log_text = tk.Text(log_frame, height=12, wrap=tk.WORD, font=('Arial', 9))
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = tk.Scrollbar(log_frame, command=self.log_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.log_text.config(yscrollcommand=scrollbar.set)
        
    # Button section (initially hidden)
        self.button_frame = tk.Frame(main_frame)
        self.yes_button = tk.Button(self.button_frame, text="Yes", command=self.set_response_yes)
        self.no_button = tk.Button(self.button_frame, text="No", command=self.set_response_no)
        self.user_response = None
        
    def update(self, status, value, max_value):
        self.status_label.config(text=status)
        self.progress["maximum"] = max_value
        self.progress["value"] = value
        percent = int((value / max_value) * 100) if max_value > 0 else 0
        self.percent_label.config(text=f"{percent}%")
        
        self.log_text.insert(tk.END, f"{status} ({percent}%)\n")
        self.log_text.see(tk.END)
        self.root.update()
        
    def add_log(self, message):
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
        self.root.update()
        
    def ask_question(self, question):
        self.log_text.insert(tk.END, f"\n{question}\n")
        self.button_frame.pack(pady=10)
        self.yes_button.pack(side=tk.LEFT, padx=10)
        self.no_button.pack(side=tk.LEFT)
        self.root.wait_variable(self.user_response)
        self.button_frame.pack_forget()
        return self.user_response.get()
        
    def set_response_yes(self):
        self.user_response.set(True)
        
    def set_response_no(self):
        self.user_response.set(False)
        
    def show_files_list(self, files, title="Files found"):
        self.log_text.insert(tk.END, f"\n{title}:\n")
        for file in files:
            self.log_text.insert(tk.END, f"- {os.path.basename(file)}\n")
        self.log_text.see(tk.END)
        self.root.update()

def identify_audio_type(folder):
    progress_window = ProgressWindow("Analyzing audio files")
    dualmono_files = []
    total_files = sum([len(files) for _, _, files in os.walk(folder) if any(f.endswith('.wav') for f in files)])
    processed_files = 0
    
    # Walk through all directories
    for root_dir, _, files in os.walk(folder):
        wav_files = [file for file in files if file.endswith(".wav")]
        
        # Process each WAV file
        for file in wav_files:
            # Skip already labeled files
            if "(mono)" in file or "(stereo)" in file:
                continue
                
            original_path = os.path.join(root_dir, file)
            audio_type = get_audio_type(original_path)
            
            if not audio_type:
                continue
                
            try:
                # Handle silent channel conversion
                if audio_type == "silent_channel":
                    file_info = sf.info(original_path)
                    new_name = f"{os.path.splitext(file)[0]} (mono).wav"
                    data, sample_rate = sf.read(original_path)
                    
                    # Select active channel
                    left_channel = data[:, 0]
                    right_channel = data[:, 1]
                    mono_data = right_channel if np.all(np.abs(left_channel) < 1e-10) else left_channel
                    
                    # Save preserving original bit depth
                    sf.write(os.path.join(root_dir, new_name), mono_data, sample_rate, subtype=file_info.subtype)
                    print(f"File with silent channel converted to mono (preserving {file_info.subtype}): {original_path} -> {new_name}")
                    
                    # Move original to obsolete folder
                    obsolete_path = os.path.join(root_dir, "-- OBSOLETE FILES")
                    os.makedirs(obsolete_path, exist_ok=True)
                    shutil.move(original_path, os.path.join(obsolete_path, file))
                
                # Rename other audio types
                else:
                    new_name = f"{os.path.splitext(file)[0]} ({audio_type}).wav"
                    os.rename(original_path, os.path.join(root_dir, new_name))
                    if audio_type == "dualmono":
                        dualmono_files.append(os.path.join(root_dir, new_name))
            
            except Exception as e:
                print(f"Error processing file {file}: {e}")
            
            # Update progress
            processed_files += 1
            progress_window.update(f"Processing: {file}", processed_files, total_files)
    
    progress_window.root.destroy()
    
    # Return dualmono files found (let main flow handle conversion)
    return dualmono_files

def get_audio_type(file):
    try:
        # Read file preserving original format
        file_info = sf.info(file)
        data, sample_rate = sf.read(file)
        subtype = file_info.subtype

        if len(data.shape) == 1 or data.shape[1] == 1:
            return "mono"
        elif data.shape[1] == 2:
            left_channel = data[:, 0]
            right_channel = data[:, 1]
            
            # Improved silent channel detection
            left_silent = np.all(np.abs(left_channel) < 1e-10)
            right_silent = np.all(np.abs(right_channel) < 1e-10)
            
            if left_silent or right_silent:
                silent_side = "left" if left_silent else "right"
                root = tk.Tk()
                root.withdraw()
                root.after(100, lambda: root.focus_force())
                messagebox.showinfo("Silent Channel Detected", 
                    f"File {os.path.basename(file)} has silent {silent_side} channel.\n"
                    "It will be automatically converted to mono.")
                root.destroy()
                return "silent_channel"  # New type for files with silent channels
            
            channel_type = detect_audio_type(data)
            if channel_type == "False stereo":
                return "dualmono"
            else:
                return "stereo"
        else:
            return "unknown"
    except Exception as e:
        print("Error obtaining file information:", e)
        return None

def detect_audio_type(data):
    try:
        if data.shape[1] == 2:
            left_channel = data[:, 0]
            right_channel = data[:, 1]

            # Check if a channel is empty (silent)
            left_empty = np.all(np.abs(left_channel) < 1e-10)
            right_empty = np.all(np.abs(right_channel) < 1e-10)

            if left_empty or right_empty:
                return "False stereo"
            
            # Check if both channels are equal
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

def is_mono(file_path):
    """
    Check if an audio file is mono (single channel).
    
    Args:
        file_path: Path to the audio file
        
    Returns:
        bool: True if the file is mono, False otherwise
    """
    try:
        data, sample_rate = sf.read(file_path, always_2d=True)
        return data.shape[1] == 1  # True if it's mono (1 channel)
    except Exception as e:
        print(f"Error checking if file is mono {file_path}: {str(e)}")
        return False  # By default assume is not mono if there is error

def confirm_convert_LR_to_stereo(folder):
    matching_files = find_matching_files(folder)
    if matching_files:
        selected_pairs = show_LR_pairs(matching_files)  # Show selection dialog
        
        if selected_pairs:
            progress_window = ProgressWindow("Converting L/R to stereo")
            total_pairs = len(selected_pairs)
            processed_pairs = 0
            
            for left_file, right_file in selected_pairs:
                progress_window.update(f"Processing: {os.path.basename(left_file)} + {os.path.basename(right_file)}", 
                                     processed_pairs, total_pairs)
                
                if not is_mono(left_file):
                    left_file = convert_to_mono(left_file)
                if not is_mono(right_file):
                    right_file = convert_to_mono(right_file)
                convert_to_stereo(left_file, right_file, progress_window)
                
                processed_pairs += 1
                progress_window.add_log(f"Files converted to stereo: {left_file} + {right_file}")
            
            progress_window.root.destroy()
    else:
        print("No matching L/R pairs found in the folder.")

def confirm_reorder_files(folder):
    wav_files = [file for file in os.listdir(folder) if file.endswith(".wav")]
    if wav_files:
        reorder = messagebox.askyesno("Confirm", "Do you want to reorder the files (and maybe categorize them)?")
        if reorder:
            reorder_files(folder)
    else:
        print("No .wav files found in the folder. Exiting the program.")

def reorder_files(folder):
    app = FileOrdererApp(folder)
    app.run()

def find_matching_files(folder_path):
    """
    Find matching L/R files in the folder, handling case-sensitivity properly.
    Uses os.path.normcase() for cross-platform case normalization.
    """
    matching_files = {}
    for root_folder, _, files in os.walk(folder_path):
        if os.path.basename(root_folder) == "-- OBSOLETE FILES":  # Ignore the "-- OBSOLETE FILES" folder
            continue
        for file in files:
            if file.startswith('.'):
                continue
            
            # Improved regex to handle common misspellings and variations
            # Pattern: base_name + optional separator + optional left/right indicator + optional (tags) + extension
            match = re.match(r'(.+?)(?:_|\s)*(?:left|right|l|r|rigth|rigt|righ)?(?:\s*\(.*?\))?\.(.+)', file, re.IGNORECASE)
            if match:
                base_name = match.group(1)
                # Remove trailing spaces or underscores that might be left after suffix removal
                base_name = base_name.rstrip(' _')
                # Use normcase for cross-platform case handling
                # On Windows: converts to lowercase, on macOS/Linux: preserves case but helps with normalization
                normalized_name = os.path.normcase(base_name)
                if normalized_name in matching_files:
                    matching_files[normalized_name].append(os.path.join(root_folder, file))
                else:
                    matching_files[normalized_name] = [os.path.join(root_folder, file)]
    return matching_files

def convert_to_mono(file_path):
    try:
        # Use soundfile to read the file
        data, sample_rate = sf.read(file_path, always_2d=True)
        
        # If the file already has tag "(mono)", it does not need conversion
        if "(mono)" not in file_path.lower():
            # If you have tag "(dualmono)", turn it to mono
            if "(dualmono)" in file_path.lower():
                # Take only the left channel
                if data.shape[1] == 2:  # Verify if it's stereo
                    mono_data = data[:, 0]  # Take only the first channel (left)
                else:
                    mono_data = data  # If it is mono, there are no necessary changes
                
                # Update file name
                file_name, file_ext = os.path.splitext(file_path)
                new_file_path = f"{file_name} (mono){file_ext}"
                
                # Save mono file preserving the original format
                file_info = sf.info(file_path)
                sf.write(new_file_path, mono_data, sample_rate, subtype=file_info.subtype)
                print(f"File converted to mono: {file_path} -> {new_file_path}")
                
                # Move original file to an OBSOLETE folder
                obsolete_folder_path = os.path.join(os.path.dirname(file_path), "-- OBSOLETE FILES")
                os.makedirs(obsolete_folder_path, exist_ok=True)
                shutil.move(file_path, os.path.join(obsolete_folder_path, os.path.basename(file_path)))
                print(f"Dualmono file moved to OBSOLETE FILES: {file_path}")
                
                return new_file_path
        return file_path
    except Exception as e:
        print(f"Error converting to mono {file_path}: {str(e)}")
        return file_path  # In case of error, return the original file

def convert_to_stereo(left_file_path, right_file_path, progress_window=None):
    # Show progress if a window is provided
    if progress_window:
        progress_window.add_log(f"Processing L/R pair: {os.path.basename(left_file_path)} and {os.path.basename(right_file_path)}")
    
    # Verify files exist
    if not os.path.exists(left_file_path):
        print(f"Error: Left file not found: {left_file_path}")
        return None
    if not os.path.exists(right_file_path):
        print(f"Error: Right file not found: {right_file_path}")
        return None
    
    # Get file info to preserve original format
    try:
        left_info = sf.info(left_file_path)
        right_info = sf.info(right_file_path)
        
        # Compare sample rates
        if left_info.samplerate != right_info.samplerate:
            print(f"Warning: Different sample rates - L: {left_info.samplerate} vs R: {right_info.samplerate}")
        
        subtype = left_info.subtype  # Use left file's subtype as reference
        
        # Read files preserving original format
        left_data, left_sample_rate = sf.read(left_file_path, always_2d=True)
        right_data, right_sample_rate = sf.read(right_file_path, always_2d=True)
        
        if progress_window:
            progress_window.add_log(f"Read files - L: {len(left_data)} samples, R: {len(right_data)} samples")
        
        # Adjust data length to the minimum of both channels
        min_len = min(len(left_data), len(right_data))
        left_data = left_data[:min_len]
        right_data = right_data[:min_len]
        
        if progress_window:
            progress_window.add_log(f"Combining {min_len} samples (trimmed to shortest file)")
        
        # Combine left and right channels to create stereo
        stereo_data = np.column_stack((left_data[:,0], right_data[:,0]))
        
    except Exception as e:
        error_msg = f"Error processing files: {str(e)}"
        print(error_msg)
        if progress_window:
            progress_window.add_log(error_msg)
        return None
    
    # Get base name for stereo file
    base_name_left = os.path.splitext(os.path.basename(left_file_path))[0]
    base_name_right = os.path.splitext(os.path.basename(right_file_path))[0] if right_file_path else None
    
    if progress_window:
        progress_window.add_log("Generating name for stereo file...")
    
    if base_name_right:
        base_name_stereo = ''
        for c1, c2 in zip(base_name_left, base_name_right):
            # Use normcase for cross-platform case-insensitive comparison
            if os.path.normcase(c1) == os.path.normcase(c2):
                base_name_stereo += c1
            else:
                break
    else:
        base_name_stereo = base_name_left
            
    # Save stereo file preserving original bit depth
    output_file = os.path.join(os.path.dirname(left_file_path), f"{base_name_stereo}(stereo).wav")
    
    if progress_window:
        progress_window.add_log(f"Saving stereo file (preserving {subtype}): {os.path.basename(output_file)}")
    
    sf.write(output_file, stereo_data, left_sample_rate, subtype=subtype)
    
    if progress_window:
        progress_window.add_log("Stereo file saved successfully")
        progress_window.add_log("Moving original files to OBSOLETE folder...")
    
    # Move original files to OBSOLETE folder
    obsolete_folder_path = os.path.join(os.path.dirname(left_file_path), "-- OBSOLETE FILES")
    os.makedirs(obsolete_folder_path, exist_ok=True)
    shutil.move(left_file_path, os.path.join(obsolete_folder_path, os.path.basename(left_file_path)))
    if right_file_path:
        shutil.move(right_file_path, os.path.join(obsolete_folder_path, os.path.basename(right_file_path)))
    
    if progress_window:
        progress_window.add_log("Process completed")
    
    return output_file

if __name__ == "__main__":
    main()
