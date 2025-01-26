# File Type Checker
A Python script that adds a **"Check File Types"** option to the Windows right-click context menu. Count file types and open random folders with ease!
![File Type Checker](https://github.com/user-attachments/assets/802e592a-4a91-4a9e-9685-ddfed024ea3e)

---

## Features

- **Right-Click Integration:** Adds "Check File Types" to folder context menus.
- **File Type Counts:** Displays file type counts (sorted by most to least).
- **Random Folder Navigation:** Opens a random folder containing the selected file type.
- **Custom Icon:** Uses `finder.ico` for the context menu and GUI.

---

## Installation

1. **Save the Script:**
   - Save the script as `CheckFileTypes.pyw` in a directory (e.g., `C:\CheckFileTypes.pyw`).

2. **Add the Icon:**
   - Place `finder.ico` in the same directory as the script.

3. **Run the Script:**
   - Open Command Prompt as administrator, navigate to the script directory, and run:
     ```bash
     pythonw file_type_checker.pyw
     ```

4. **Verify:**
   - Right-click any folder → "Check File Types".

---

## Usage

1. **Check File Types:**
   - Right-click a folder → "Check File Types".
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

## contribute
Modify this program so that it can also run as an executable file.
