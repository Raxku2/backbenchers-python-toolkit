# 󰈈 Aggressive Focus Blocker

An unforgiving, full-screen focus tool for Linux (X11) that physically prevents you from accessing distracting applications during work sessions. 

Unlike other focus apps that can be easily closed or bypassed, this script strips window decorations, forces itself to the top of the stack, and uses X11 input grabbing to steal all mouse and keyboard events. 

**Once it starts, you are forced to focus.**

## 🚀 Features

* **Complete Input Hijacking:** Swallows all X11 mouse and keyboard inputs (`grab_set()`). Alt-Tab, Super keys, and clicking elsewhere will not work.
* **Un-Killable via UI:** Strips window decorations (`overrideredirect`) so there is no "X" button, and ignores standard `Alt+F4` close requests.
* **Visual Silence:** Forces a full-screen, topmost overlay covering all taskbars, notifications, and other windows.
* **Productive Boredom:** Leaves you with only two options: stare at the timer or do your actual work.

## 📋 Requirements

* **OS:** Linux (Designed for X11 window managers like Openbox, i3, xfce, LXQt). *Note: Wayland restricts input grabbing by design, so this script relies heavily on X11 architecture.*
* **Python:** Python 3.x
* **Libraries:** `tkinter` (Standard library, but often requires a separate package installation on Debian/Ubuntu).
* **Fonts (Optional but Recommended):** JetBrainsMono Nerd Font (for the UI icons).

## 🛠️ Installation

1.  Ensure Python 3 and Tkinter are installed:
    ```bash
    sudo apt update
    sudo apt install python3-tk
    ```
2.  Clone or download the `focus_blocker.py` script.

## 💻 Usage

1.  Open `focus_blocker.py` and set your desired focus duration at the bottom of the script:
    ```python
    WORK_SESSION_MINUTES = 25 
    ```
2.  Run the script:
    ```bash
    python3 focus_blocker.py
    ```

## 🚨 Emergency Escape Hatch (READ THIS)

Because this script literally steals all X11 inputs, you cannot use standard shortcuts to kill it. If you accidentally set the timer for 500 minutes or encounter a bug, do not panic. 

**To force quit:**
1.  Drop into a TTY terminal by pressing `Ctrl + Alt + F3` (or F4/F5).
2.  Log in with your user credentials.
3.  Kill the python process:
    ```bash
    killall python3
    ```
    *(Or use `htop` to find the specific PID if you have other Python scripts running).*
4.  Return to your graphical desktop by pressing `Ctrl + Alt + F7` (or F1/F2 depending on your display manager).

## ⚙️ Customization

The script is just raw Python/Tkinter, making it highly customizable:
* **Colors:** Change the hex codes in the `bg` and `fg` parameters to match your system theme (currently defaults to a Catppuccin-inspired dark theme).
* **Fonts:** Modify the `font=` tuples to use your preferred system font.
