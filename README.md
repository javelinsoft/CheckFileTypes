# File Extension Counter
A Python script that adds a **"Count The File Extensions"** option to the Windows right-click context menu. Count file types and open random folders with ease! 
  ![File Extension Counter](https://github.com/user-attachments/assets/7d801e30-4623-4569-a681-495b645f31ff)



---

## Features

- **Right-Click Integration:** Adds "Count The File Extensions" to folder context menus.
- **File Type Counts:** Displays file type counts (sorted by most to least).
- **Random Folder Navigation:** Opens a random folder containing the selected file type.
- **Custom Icon:** Uses `finder.ico` for the context menu and GUI.

---

## Installation

1. **Save the Script:**
   - Save the script as `FileExtensionCounter.pyw` in a directory (e.g., `C:\FileExtensionCounter.pyw`).

2. **Add the Icon:**
   - Place `finder.ico` in the same directory as the script.

3. **Run the Script:**
   - Open Command Prompt as administrator, navigate to the script directory, and run:
     ```bash
     pythonw FileExtensionCounter.pyw
     ```

4. **Verify:**
   - Right-click any folder → "Count The File Extensions".

---

## Usage

1. **Check File Types:**
   - Right-click a folder → "Count The File Extensions".
   - A GUI shows file type counts and lets you open random folders.

2. **Open Random Folder:**
   - Select a file type → Click "Open Random Folder".

---

## Troubleshooting

- **Console Window Appears:** Ensure the script is saved as `.pyw` and uses `pythonw.exe`.
- **Icon Not Showing:** Ensure `finder.ico` is in the same directory and valid.
- **Admin Privileges:** Run Command Prompt as admin if registry changes fail.

---

## License

CC0 License.

---

## Contribute
Modify this program so that it can also run as an executable file.
