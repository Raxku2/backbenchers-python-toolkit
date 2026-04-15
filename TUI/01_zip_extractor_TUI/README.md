
# 🔐 Zip Extractor — AES Encrypted ZIP File Extractor (Terminal UI)

A modern **terminal-based Zip extractor** built with [Textual](https://github.com/Textualize/textual) and [Rich](https://github.com/Textualize/rich).  
Easily extract **password-protected (AES encrypted)** `.zip` files using a **beautiful Textual UI** — right from your terminal.  

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Textual](https://img.shields.io/badge/Textual-Modern%20TUI-orange)
![Rich](https://img.shields.io/badge/Rich-Formatting%20and%20Traceback-purple)

---

## 🧰 Features

✅ Extract **AES-encrypted** ZIP archives  
✅ Simple **Textual UI** with input boxes and buttons  
✅ **Password input** support  
✅ Error handling with beautiful **Rich tracebacks**  
✅ **Auto directory creation** if output folder doesn’t exist  
✅ Lightweight and **cross-platform (Windows/Linux/Mac)**  

---

## 🖼️ Preview

> ⚙️ Terminal-based Textual UI Example  
```

+-------------------------------------------------------+

| Zip Extractor🔐                            11:23:54 🕒    |
| --------------------------------------------------------- |
| Enter zip path:          [__________________________]     |
| Enter output folder:     [__________________________]     |
| Enter Password:          [__________________________]     |
|                                                           |
| [ Extract Zip.. ]                                         |
|                                                           |
| Status: [green]Extracted[/green]                          |
| -------------------------------------------------------   |
| Press Q to exit                                           |
| +-------------------------------------------------------+ |

````

---

## 🧑‍💻 Installation

Clone the repository and install dependencies:

```bash
git clone https://github.com/yourusername/zip-extractor.git
cd zip-extractor
pip install -r requirements.txt
````

### 🧩 Requirements

Make sure you have these packages installed:

```bash
pip install rich textual pyzipper
```

---

## 🚀 Usage

Run the app directly using Python:

```bash
python main.py
```

### Steps:

1. Enter the **path to the ZIP file**
2. Enter the **destination folder** (will be created if not present)
3. Enter the **password** (if applicable)
4. Click **“Extract Zip..”**
5. See the **status message** below (success or error)

---

## 🧠 Code Overview

```python
from rich.traceback import install
from textual.app import App
from textual.widgets import Header, Footer, Input, Button, Label, Static
from pyzipper import AESZipFile
```

The program:

* Uses `Textual` for TUI layout and interaction
* Uses `pyzipper` for AES-encrypted zip extraction
* Handles missing files, incorrect passwords, and folder creation automatically

---

## 📁 Project Structure

```
zip-extractor/
├── main.py                # Main application code
├── requirements.txt       # Dependency list
└── README.md              # Documentation
```

---

## 🧾 Example Requirements File

```txt
rich
textual
pyzipper
```

---

## 🧱 Tech Stack

| Component    | Description                        |
| ------------ | ---------------------------------- |
| **Python**   | Core language                      |
| **Rich**     | Colored terminal text + tracebacks |
| **Textual**  | Terminal UI framework              |
| **Pyzipper** | AES ZIP extraction library         |

---

## 🛡️ Error Handling

* `[red]Incorrect Password. Try again[/red]` → Wrong password entered
* `[red]Enter Password[/red]` → Password missing
* `FileNotFoundError` → Invalid ZIP path
* `[green]Extracted[/green]` → Successful extraction

---

## 💡 Future Improvements

* [ ] Add drag-and-drop ZIP path input (GUI mode)
* [ ] Add ZIP compression (Create archives)
* [ ] Add history of recent extractions
* [ ] Add dark/light themes for the UI

---

## 🧑‍💻 Author

**Developed by:** [Pinaka](https://github.com/raxku2)
💬 *“A small utility to simplify encrypted ZIP extraction in style.”*

---

## 🪪 License

This project is licensed under the **MIT License**.
See the [LICENSE](LICENSE) file for more information.
