import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox
from collections import defaultdict
import winreg
import random
import subprocess

def count_file_types(folder_path):
    file_types = defaultdict(int)
    folder_files = defaultdict(list)  # Stores folders and their files

    # Recursively count files and folders
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            _, ext = os.path.splitext(file)
            ext = ext.lower()  # Normalize to lowercase
            if not ext:
                ext = "No Extension"
            file_types[ext] += 1
            folder_files[ext].append(root)  # Store the folder path for this file type

    # Sort file types by count (most to least)
    sorted_file_types = sorted(file_types.items(), key=lambda x: x[1], reverse=True)

    return sorted_file_types, folder_files

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

def display_results(folder_path, file_types, folder_files):
    root = tk.Tk()
    root.title("Count The File Extensions")

    # Set the icon for the GUI window
    script_dir = os.path.dirname(os.path.abspath(__file__))
    ico_path = os.path.join(script_dir, "finder.ico")
    if os.path.exists(ico_path):
        root.iconbitmap(ico_path)  # Set the window icon
    else:
        print(f"ICO file not found: {ico_path}")

    # Prepare the result message
    result = f"Folder: {folder_path}\n\n"
    result += "File Types and Counts:\n"

    # Create a frame for the list and scrollbar
    frame = tk.Frame(root)
    frame.pack(padx=10, pady=10)

    # Create a Text widget for displaying results
    text_widget = tk.Text(frame, width=50, height=15)
    text_widget.pack(side=tk.LEFT)

    # Add a scrollbar
    scrollbar = tk.Scrollbar(frame, command=text_widget.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    text_widget.config(yscrollcommand=scrollbar.set)

    # Function to update the display based on sorting
    def update_display(sort_by):
        text_widget.delete(1.0, tk.END)  # Clear the current text
        if sort_by == "Count":
            sorted_file_types = sorted(file_types, key=lambda x: x[1], reverse=True)
        else:  # Sort alphabetically
            sorted_file_types = sorted(file_types, key=lambda x: x[0])

        for ext, count in sorted_file_types:
            text_widget.insert(tk.END, f"{ext}: {count}\n")

    # Initial display
    update_display("Count")

    # Dropdown to select sorting method
    sort_options = ["Count", "Alphabetical"]
    selected_sort = tk.StringVar()
    selected_sort.set(sort_options[0])  # Default to sorting by count

    sort_label = tk.Label(root, text="Sort by:")
    sort_label.pack(padx=10, pady=5)

    sort_dropdown = ttk.Combobox(root, textvariable=selected_sort, values=sort_options, state="readonly")
    sort_dropdown.pack(padx=10, pady=5)

    # Update display when sorting option changes
    def on_sort_change(event):
        update_display(selected_sort.get())

    sort_dropdown.bind("<<ComboboxSelected>>", on_sort_change)

    # Dropdown to select an extension (always sorted alphabetically)
    extensions = sorted([ext for ext, _ in file_types])  # Sort extensions alphabetically
    selected_extension = tk.StringVar()
    selected_extension.set(extensions[0])  # Default to the first extension

    extension_label = tk.Label(root, text="Select an extension:")
    extension_label.pack(padx=10, pady=5)

    extension_dropdown = ttk.Combobox(root, textvariable=selected_extension, values=extensions, state="readonly")
    extension_dropdown.pack(padx=10, pady=5)

    # Button to open a random folder
    def on_open_random_folder():
        ext = selected_extension.get()
        open_random_folder(ext, folder_files)

    open_button = tk.Button(root, text="Open Random Folder", command=on_open_random_folder)
    open_button.pack(padx=10, pady=10)

    root.mainloop()


def add_context_menu_option():
    try:
        # Path to the current Python script
        script_path = os.path.abspath(__file__)
        script_dir = os.path.dirname(script_path)

        # Path to the ICO file
        ico_path = os.path.join(script_dir, "finder.ico")

        # Check if the ICO file exists
        if not os.path.exists(ico_path):
            print(f"ICO file not found: {ico_path}")
            return

        # Create the registry key for the context menu
        key_path = r"Directory\\shell\\FileExtensionCounter"
        key = winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, key_path)
        winreg.SetValue(key, "", winreg.REG_SZ, "Count The File Extensions")

        # Set the icon for the context menu
        winreg.SetValueEx(key, "Icon", 0, winreg.REG_SZ, ico_path)

        # Create the command key
        command_key = winreg.CreateKey(key, "command")
        pythonw_path = os.path.join(os.path.dirname(sys.executable), "pythonw.exe")
        winreg.SetValue(command_key, "", winreg.REG_SZ, f'"{pythonw_path}" "{script_path}" "%1"')

        print("Context menu option added successfully!")
    except Exception as e:
        print(f"Failed to add context menu option: {e}")

def main(folder_path):
    # Count file types and folders
    file_types, folder_files = count_file_types(folder_path)
    # Display the results
    display_results(folder_path, file_types, folder_files)

if __name__ == "__main__":
    if len(sys.argv) == 1:
        # If no arguments are passed, add the context menu option
        add_context_menu_option()
    elif len(sys.argv) > 1:
        # If a folder path is passed, run the File Extension Counter
        main(sys.argv[1])
