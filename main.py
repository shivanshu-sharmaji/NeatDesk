import os
import shutil
import threading
import hashlib
import logging
import customtkinter as ctk
from tkinter import filedialog, messagebox

# -----------------------
# Configuration & Globals
# -----------------------

# Modern UI Appearance Settings
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# File categories by extension (add more as needed)
FILE_CATEGORIES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff"],
    "Documents": [".pdf", ".doc", ".docx", ".txt", ".xls", ".xlsx", ".ppt", ".pptx"],
    "Videos": [".mp4", ".mov", ".avi", ".mkv", ".flv", ".wmv"],
    "Music": [".mp3", ".wav", ".aac", ".flac"],
    "Archives": [".zip", ".rar", ".tar", ".gz", ".7z"],
    "Scripts": [".py", ".js", ".sh", ".bat", ".pl"],
    "Executables": [".exe", ".msi", ".bin", ".apk"],
    "Others": []
}

# Logging setup
logging.basicConfig(
    filename='file_organizer.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# -----------------------
# Utility Functions
# -----------------------

def get_file_hash(filepath, block_size=65536):
    """Calculate SHA256 hash of a file for duplicate detection."""
    sha = hashlib.sha256()
    try:
        with open(filepath, 'rb') as f:
            while True:
                data = f.read(block_size)
                if not data:
                    break
                sha.update(data)
    except Exception as e:
        logging.warning(f"Cannot read file for hashing: {filepath}, {e}")
        return None
    return sha.hexdigest()

def get_category(filename):
    """Get the category folder for a given filename based on extension."""
    ext = os.path.splitext(filename)[1].lower()
    for category, extensions in FILE_CATEGORIES.items():
        if ext in extensions:
            return category
    return "Others"

def safe_move_file(src, dest_folder):
    """Move a file to destination folder, handling duplicate names by renaming."""
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)
    filename = os.path.basename(src)
    dest_path = os.path.join(dest_folder, filename)

    # If file exists, rename
    base, ext = os.path.splitext(filename)
    counter = 1
    while os.path.exists(dest_path):
        dest_path = os.path.join(dest_folder, f"{base}({counter}){ext}")
        counter += 1
    shutil.move(src, dest_path)
    return dest_path

def remove_empty_folders(folder):
    """Recursively remove empty folders."""
    removed_count = 0
    for root, dirs, files in os.walk(folder, topdown=False):
        for d in dirs:
            full_path = os.path.join(root, d)
            try:
                if not os.listdir(full_path):
                    os.rmdir(full_path)
                    removed_count += 1
            except Exception as e:
                logging.warning(f"Failed to remove folder {full_path}: {e}")
    return removed_count

# -----------------------
# Core Organizer Class
# -----------------------

class FileOrganizerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("NeatDesk - Smart File Organizer")
        self.geometry("950x600")

        self.selected_folder = ctk.StringVar(value="No folder selected")
        self.status_text = ctk.StringVar(value="Ready")
        self.file_list = []
        self.preview_moves = []

        # Configure Layout Grid
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.setup_ui()

    def setup_ui(self):
        # Sidebar Navigation
        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(6, weight=1)

        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="📁 NeatDesk", font=ctk.CTkFont(size=24, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 30))

        self.browse_btn = ctk.CTkButton(self.sidebar_frame, text="Browse Folder", command=self.browse_folder)
        self.browse_btn.grid(row=1, column=0, padx=20, pady=10)

        self.scan_btn = ctk.CTkButton(self.sidebar_frame, text="Scan Folder", command=self.scan_folder)
        self.scan_btn.grid(row=2, column=0, padx=20, pady=10)

        self.preview_btn = ctk.CTkButton(self.sidebar_frame, text="Show Preview", state='disabled', command=self.show_preview)
        self.preview_btn.grid(row=3, column=0, padx=20, pady=10)

        self.organize_btn = ctk.CTkButton(self.sidebar_frame, text="Organize Files", state='disabled', command=self.organize_files)
        self.organize_btn.grid(row=4, column=0, padx=20, pady=10)

        self.clean_btn = ctk.CTkButton(self.sidebar_frame, text="Clean Folders", state='disabled', command=self.clean_empty_folders)
        self.clean_btn.grid(row=5, column=0, padx=20, pady=10)

        self.appearance_label = ctk.CTkLabel(self.sidebar_frame, text="Theme:", anchor="w")
        self.appearance_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.appearance_menu = ctk.CTkOptionMenu(self.sidebar_frame, values=["Dark", "Light", "System"], command=self.change_appearance_mode)
        self.appearance_menu.grid(row=8, column=0, padx=20, pady=(5, 20))

        # Main Content Area
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(2, weight=1)

        # Visual Card for Path Information
        self.path_card = ctk.CTkFrame(self.main_frame, height=50)
        self.path_card.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        self.folder_label = ctk.CTkLabel(self.path_card, textvariable=self.selected_folder, font=ctk.CTkFont(size=12, slant="italic"))
        self.folder_label.pack(pady=10, padx=20)

        # Status & Progress Area
        self.status_label = ctk.CTkLabel(self.main_frame, textvariable=self.status_text, text_color="#1f6aa5")
        self.status_label.grid(row=1, column=0, pady=(10, 0))
        
        self.progress = ctk.CTkProgressBar(self.main_frame, width=600)
        self.progress.grid(row=2, column=0, pady=10)
        self.progress.set(0)

        # Preview Text Area (Replaces Listbox)
        self.preview_textbox = ctk.CTkTextbox(self.main_frame, font=ctk.CTkFont(family="Consolas", size=12))
        self.preview_textbox.grid(row=3, column=0, sticky="nsew", padx=5, pady=15)

    def change_appearance_mode(self, mode):
        ctk.set_appearance_mode(mode)

    def browse_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.selected_folder.set(folder)
            self.status_text.set(f"Selected folder: {folder}")
            self.file_list = []
            self.preview_moves = []
            self.preview_textbox.delete("0.0", "end")
            self.preview_btn.configure(state='disabled')
            self.organize_btn.configure(state='disabled')
            self.clean_btn.configure(state='disabled')
            self.progress.set(0)

    def scan_folder(self):
        folder = self.selected_folder.get()
        if not folder or folder == "No folder selected" or not os.path.exists(folder):
            messagebox.showerror("Error", "Please select a valid folder!")
            return

        self.status_text.set("Scanning folder, please wait...")
        self.preview_textbox.delete("0.0", "end")
        self.file_list = []

        def scan():
            for root, dirs, files in os.walk(folder):
                for file in files:
                    filepath = os.path.join(root, file)
                    self.file_list.append(filepath)

            self.status_text.set(f"Scan complete: {len(self.file_list)} files found.")
            self.preview_btn.configure(state='normal')
            self.organize_btn.configure(state='disabled')
            self.clean_btn.configure(state='disabled')

        threading.Thread(target=scan, daemon=True).start()

    def show_preview(self):
        if not self.file_list:
            messagebox.showinfo("No files", "No files to preview. Please scan first.")
            return

        self.preview_textbox.delete("0.0", "end")
        self.preview_moves = []

        folder = self.selected_folder.get()
        total = len(self.file_list)
        self.status_text.set("Generating preview...")

        for idx, filepath in enumerate(self.file_list):
            filename = os.path.basename(filepath)
            category = get_category(filename)
            dest_folder = os.path.join(folder, category)
            dest_path = os.path.join(dest_folder, filename)

            # Handle duplicate names in preview (simulate renaming)
            base, ext = os.path.splitext(filename)
            counter = 1
            while any(move[1] == dest_path for move in self.preview_moves):
                dest_path = os.path.join(dest_folder, f"{base}({counter}){ext}")
                counter += 1

            self.preview_moves.append((filepath, dest_path))
            display_text = f"MOVE: {filename} -> {category}/\n"
            self.preview_textbox.insert("end", display_text)
            self.progress.set((idx + 1) / total)
            self.update_idletasks()

        self.status_text.set(f"Preview ready: {total} files will be moved.")
        self.organize_btn.configure(state='normal')
        self.clean_btn.configure(state='disabled')

    def organize_files(self):
        if not self.preview_moves:
            messagebox.showinfo("No preview", "Please generate preview before organizing.")
            return

        folder = self.selected_folder.get()
        total = len(self.preview_moves)
        self.status_text.set("Organizing files, please wait...")

        def organize():
            success_count = 0
            for idx, (src, dest) in enumerate(self.preview_moves):
                try:
                    dest_folder = os.path.dirname(dest)
                    if not os.path.exists(dest_folder):
                        os.makedirs(dest_folder)

                    final_dest = dest
                    base, ext = os.path.splitext(os.path.basename(dest))
                    counter = 1
                    while os.path.exists(final_dest):
                        final_dest = os.path.join(dest_folder, f"{base}({counter}){ext}")
                        counter += 1

                    shutil.move(src, final_dest)
                    success_count += 1
                    logging.info(f"Moved: {src} -> {final_dest}")
                except Exception as e:
                    logging.error(f"Failed to move {src} -> {dest}: {e}")

                self.progress.set((idx + 1) / total)
                self.update_idletasks()

            self.status_text.set(f"Organizing complete. {success_count}/{total} files moved.")
            self.clean_btn.configure(state='normal')
            self.organize_btn.configure(state='disabled')
            self.preview_btn.configure(state='disabled')

        threading.Thread(target=organize, daemon=True).start()

    def clean_empty_folders(self):
        folder = self.selected_folder.get()
        if not folder or folder == "No folder selected" or not os.path.exists(folder):
            messagebox.showerror("Error", "Please select a valid folder!")
            return

        self.status_text.set("Cleaning empty folders...")

        def clean():
            removed = remove_empty_folders(folder)
            self.status_text.set(f"Cleaned {removed} empty folders.")
            self.clean_btn.configure(state='disabled')

        threading.Thread(target=clean, daemon=True).start()

# -----------------------
# Main Execution
# -----------------------

def main():
    app = FileOrganizerApp()
    app.mainloop()

if __name__ == "__main__":
    main()

# [Retained comments from your original script]
# This script is a simple file organizer GUI application using Tkinter.
# It allows users to select a folder, scan for files, preview the organization,
# and move files into categorized folders based on their extensions.
# It also cleans up empty folders after the organization process.
# The application uses threading to keep the UI responsive during long operations.
# Logging is implemented to track file movements and errors.
# The script is designed to be user-friendly and provides feedback through status messages.
# The file categories and extensions can be easily modified in the FILE_CATEGORIES dictionary.
# The application is structured with a main class (FileOrganizerApp) that handles the UI and logic.
# The utility functions are defined separately for better organization and readability.
# The script is intended for educational purposes and can be further enhanced with additional features.
# For example, adding more file categories, improving error handling,
# or implementing a more sophisticated duplicate file detection mechanism.
# The GUI is designed to be simple and intuitive, making it accessible for users with varying levels of technical expertise.
# The application can be run directly, and it will open a window for user interaction.
# The script is self-contained and does not require any external dependencies beyond the standard library.
# The use of threading ensures that the application remains responsive,
# even when performing potentially time-consuming operations like scanning and moving files.
# The progress bar provides visual feedback on the status of file operations,
# enhancing the user experience.
# The application can be further improved by adding features such as:
# - Customizable file categories and extensions
# - A settings menu for user preferences
# - A help section with usage instructions
# - Support for undoing the last operation
# - Integration with cloud storage services for file organization
# - A more advanced duplicate file detection and merging system
# - A search function to quickly find files within the selected folder
# - The ability to filter files by size, date, or other criteria
# - A dark mode or theme customization option
# - Support for multiple languages
# - A command-line interface for advanced users
# - A logging system that allows users to view past operations and errors 
# - A backup feature to save original files before moving them
# - A batch processing feature to organize multiple folders at once
# - A file preview feature to view images or documents before moving
# - A context menu integration for right-clicking files in the file explorer
# - A built-in file viewer for quick access to files without opening external applications
# - A file compression feature to zip files before moving them
# - A file encryption feature for sensitive files
# - A user authentication system for added security
# - A built-in file renamer for batch renaming files
# - A built-in file converter for changing file formats
# - A built-in file splitter for large files
# - A built-in file merger for combining multiple files into one
# - A built-in file compressor for reducing file size
# - A built-in file extractor for decompressing files
# - A built-in file shredder for securely deleting files