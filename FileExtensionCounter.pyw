import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from collections import defaultdict
import winreg
import random
import subprocess

def count_file_types(folder_path):
    file_types = defaultdict(int)
    folder_files = defaultdict(list)
    total_files = 0
    total_folders = 0

    for root, dirs, files in os.walk(folder_path):
        total_folders += len(dirs)
        total_files += len(files)
        for file in files:
            _, ext = os.path.splitext(file)
            ext = ext.lower()
            if not ext:
                ext = "No Extension"
            file_types[ext] += 1
            folder_files[ext].append(root)

    sorted_file_types = sorted(file_types.items(), key=lambda x: x[1], reverse=True)

    return sorted_file_types, folder_files, total_files, total_folders

def open_random_folder(extension, folder_files):
    if extension in folder_files:
        folders = folder_files[extension]
        if folders:
            random_folder = random.choice(folders)
            subprocess.Popen(f'explorer "{random_folder}"')
        else:
            messagebox.showinfo("Error", f"No folders found for extension: {extension}")
    else:
        messagebox.showinfo("Error", f"Extension not found: {extension}")

def display_results(folder_path, file_types, folder_files, total_files, total_folders):
    root = tk.Tk()
    root.title("File Extension Counter")

    script_dir = os.path.dirname(os.path.abspath(__file__))
    ico_path = os.path.join(script_dir, "finder.ico")
    if os.path.exists(ico_path):
        root.iconbitmap(ico_path)
    else:
        print(f"ICO file not found: {ico_path}")

    # Create a menu bar
    menu_bar = tk.Menu(root)
    root.config(menu=menu_bar)

    # Create a File menu
    file_menu = tk.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="File", menu=file_menu)

    # Add commands to the File menu
    file_menu.add_command(label="Open Folder", command=open_folder)
    file_menu.add_command(label="Exit", command=root.quit)
    file_menu.add_command(label="About", command=show_about)

    # Construct the result string
    result = f"Folder: {folder_path}\n\n"
    result += f"Total Files: {total_files}\n"
    result += f"Total Folders: {total_folders}\n\n"
    result += "File Types and Counts:\n"

    frame = tk.Frame(root)
    frame.pack(padx=10, pady=10)

    text_widget = tk.Text(frame, width=50, height=15)
    text_widget.pack(side=tk.LEFT)

    scrollbar = tk.Scrollbar(frame, command=text_widget.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    text_widget.config(yscrollcommand=scrollbar.set)

    # Insert the result string into the text widget
    text_widget.insert(tk.END, result)

    # Function to update the display of file types
    def update_display(sort_by):
        if sort_by == "Count":
            sorted_file_types = sorted(file_types, key=lambda x: x[1], reverse=True)
        else:
            sorted_file_types = sorted(file_types, key=lambda x: x[0])

        for ext, count in sorted_file_types:
            text_widget.insert(tk.END, f"{ext}: {count}\n")

    # Initial display of file types
    update_display("Count")

    sort_options = ["Count", "Alphabetical"]
    selected_sort = tk.StringVar()
    selected_sort.set(sort_options[0])

    sort_label = tk.Label(root, text="Sort by:")
    sort_label.pack(padx=10, pady=5)

    sort_dropdown = ttk.Combobox(root, textvariable=selected_sort, values=sort_options, state="readonly")
    sort_dropdown.pack(padx=10, pady=5)

    def on_sort_change(event):
        text_widget.delete(1.0, tk.END)  # Clear the text widget
        text_widget.insert(tk.END, result)  # Reinsert the result string
        update_display(selected_sort.get())  # Update the file types display

    sort_dropdown.bind("<<ComboboxSelected>>", on_sort_change)

    extensions = sorted([ext for ext, _ in file_types])
    selected_extension = tk.StringVar()
    selected_extension.set(extensions[0])

    extension_label = tk.Label(root, text="Select an extension:")
    extension_label.pack(padx=10, pady=5)

    extension_dropdown = ttk.Combobox(root, textvariable=selected_extension, values=extensions, state="readonly")
    extension_dropdown.pack(padx=10, pady=5)

    def on_open_random_folder():
        ext = selected_extension.get()
        open_random_folder(ext, folder_files)

    open_button = tk.Button(root, text="Open Random Folder", command=on_open_random_folder)
    open_button.pack(padx=10, pady=10)

    root.mainloop()


def open_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        file_types, folder_files, total_files, total_folders = count_file_types(folder_path)
        display_results(folder_path, file_types, folder_files, total_files, total_folders)

def show_about():
    messagebox.showinfo("About", "File Extension Counter\n\n"
                                  "This program counts the number of files and folders in a selected directory.\n"
                                  "It categorizes files by their extensions and allows you to open a random folder\n"
                                  "that contains files of a selected extension.\n\n"
                                  "https://github.com/javelinsoft/file-extension-counter")

def add_context_menu_option():
    try:
        script_path = os.path.abspath(__file__)
        script_dir = os.path.dirname(script_path)
        ico_path = os.path.join(script_dir, "finder.ico")

        if not os.path.exists(ico_path):
            print(f"ICO file not found: {ico_path}")
            return

        key_path = r"Directory\shell\FileExtensionCounter"
        key = winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, key_path)
        winreg.SetValue(key, "", winreg.REG_SZ, "Count The File Extensions")
        winreg.SetValueEx(key, "Icon", 0, winreg.REG_SZ, ico_path)

        command_key = winreg.CreateKey(key, "command")
        pythonw_path = os.path.join(os.path.dirname(sys.executable), "pythonw.exe")
        winreg.SetValue(command_key, "", winreg.REG_SZ, f'"{pythonw_path}" "{script_path}" "%1"')

        print("Context menu option added successfully!")
    except Exception as e:
        print(f"Failed to add context menu option: {e}")

def main(folder_path):
    file_types, folder_files, total_files, total_folders = count_file_types(folder_path)
    display_results(folder_path, file_types, folder_files, total_files, total_folders)

if __name__ == "__main__":
    if len(sys.argv) == 1:
        add_context_menu_option()
    elif len(sys.argv) > 1:
        main(sys.argv[1])

