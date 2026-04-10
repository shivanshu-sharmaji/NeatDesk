# 📁 NeatDesk — Smart File Organizer

> **NeatDesk** is a sleek, modern desktop application that automatically organizes your messy folders into clean, categorized structures — with just a few clicks!

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)
![CustomTkinter](https://img.shields.io/badge/UI-CustomTkinter-blueviolet)
![License](https://img.shields.io/badge/License-MIT-green)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey)

---

## ✨ Features

- 🗂️ **Auto-categorization** — Sorts files into folders like Images, Documents, Videos, Music, Archives, Scripts, and Executables
- 👁️ **Preview before action** — See exactly what will move before anything changes
- 🔄 **Safe file moving** — Handles duplicate filenames automatically by renaming conflicts
- 🧹 **Empty folder cleanup** — Removes leftover empty directories after organizing
- 📊 **Progress tracking** — Real-time progress bar and status updates
- 🌗 **Theme switcher** — Dark, Light, and System themes supported
- 📝 **Activity logging** — Every move and error is recorded to `file_organizer.log`
- ⚡ **Non-blocking UI** — All heavy operations run on background threads to keep the app responsive

---

## 🖥️ Screenshots

> _Launch the app, select your messy folder, scan it, preview the plan, and organize — all in four clicks!_

---

## 📦 File Categories

| 📂 Category     | 🔖 Extensions                                      |
|----------------|----------------------------------------------------|
| 🖼️ Images       | `.jpg`, `.jpeg`, `.png`, `.gif`, `.bmp`, `.tiff`  |
| 📄 Documents    | `.pdf`, `.doc`, `.docx`, `.txt`, `.xls`, `.xlsx`, `.ppt`, `.pptx` |
| 🎬 Videos       | `.mp4`, `.mov`, `.avi`, `.mkv`, `.flv`, `.wmv`    |
| 🎵 Music        | `.mp3`, `.wav`, `.aac`, `.flac`                   |
| 🗜️ Archives     | `.zip`, `.rar`, `.tar`, `.gz`, `.7z`              |
| 🐍 Scripts      | `.py`, `.js`, `.sh`, `.bat`, `.pl`                |
| ⚙️ Executables  | `.exe`, `.msi`, `.bin`, `.apk`                    |
| 📦 Others       | Everything else                                   |

---

## 🚀 Getting Started

### ✅ Prerequisites

- Python **3.8** or higher
- `pip` package manager

### 📥 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/neatdesk.git
   cd neatdesk
   ```

2. **Install dependencies**
   ```bash
   pip install customtkinter
   ```

3. **Run the app**
   ```bash
   python main.py
   ```

---

## 🎮 How to Use

1. 📂 Click **Browse Folder** → select the folder you want to organize
2. 🔍 Click **Scan Folder** → NeatDesk scans all files recursively
3. 👁️ Click **Show Preview** → review the planned moves in the text area
4. ✅ Click **Organize Files** → files are moved into categorized subfolders
5. 🧹 Click **Clean Folders** → removes any leftover empty directories

---

## 🗂️ Project Structure

```
neatdesk/
│
├── main.py               # 🚀 Main application entry point
├── file_organizer.log    # 📝 Auto-generated activity log
└── README.md             # 📖 This file
```

---

## ⚙️ Configuration

You can easily customize file categories by editing the `FILE_CATEGORIES` dictionary at the top of `main.py`:

```python
FILE_CATEGORIES = {
    "Images": [".jpg", ".jpeg", ".png", ...],
    "Documents": [".pdf", ".docx", ...],
    # ➕ Add your own categories here!
    "MyCategory": [".ext1", ".ext2"],
}
```

---

## 📋 Logging

All file operations are automatically logged to **`file_organizer.log`** in the same directory:

```
2025-01-15 10:23:01 - INFO - Moved: /Downloads/photo.jpg -> /Downloads/Images/photo.jpg
2025-01-15 10:23:02 - WARNING - Cannot read file for hashing: /Downloads/locked.pdf
```

---

## 🛣️ Roadmap

- [ ] 🔁 Undo last organization
- [ ] ☁️ Cloud storage integration
- [ ] 🔍 Duplicate file detection (SHA256-based)
- [ ] 🖼️ In-app file preview
- [ ] 🌍 Multi-language support
- [ ] 💻 Command-line interface (CLI) mode
- [ ] 🔐 File encryption for sensitive files
- [ ] 🗃️ Batch folder processing

---

## 🤝 Contributing

Contributions are welcome! 🎉

1. Fork the repo
2. Create your feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request 🚀

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgements

- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) — for the beautiful modern UI components
- Python's `shutil`, `os`, `hashlib`, and `threading` standard libraries

---

<p align="center">Made with ❤️ and Shivanshu Sharma</p>
