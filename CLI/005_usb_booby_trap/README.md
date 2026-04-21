# 🚨 USB Booby Trap — Hardware Intrusion Detection System
A lightweight, background-running Python script that monitors your system's USB bus. 

Protects your machine by listening for unauthorized USB mounting (like rogue flash drives or Rubber Duckies) and triggering a blaring OS-level notification while logging the device's hardware ID. Perfectly tailored for Linux environments like the Raspberry Pi 5.

## 🧰 Features
✅ **Instant Intrusion Detection:** Polls the USB bus for unauthorized devices.
✅ **Secure Baseline:** Automatically snapshots currently connected devices at launch as "authorized."
✅ **Native OS Notifications:** Uses `notify-py` to fire visual alerts directly to your Desktop Environment (e.g., LXQt).
✅ **Audio Alarms:** Supports triggering custom loud `.wav` files alongside the visual alert.
✅ **Persistent Logging:** Records the exact timestamp and hardware ID of the intruder to a local text file.
✅ **Lightweight:** Avoids complex `udev` rules by parsing standard `lsusb` output.

## 🖼️ Preview
⚙️ **Terminal Execution & Logging Example**
```text
+-------------------------------------------------------------------------+
| [USB Booby Trap]                                             23:13:20 🕒|
| ----------------------------------------------------------------------- |
| [*] Initializing USB Booby Trap...                                      |
| [*] OS: Debian 13 (Trixie) | Display: LXQt                                |
| [*] Baseline established. 2 authorized device(s) found.                 |
|     - 8087:0024 Intel Corp. Integrated Rate Matching Hub                |
|     - 046d:c52b Logitech, Inc. Unifying Receiver                        |
|                                                                         |
| [*] Listening for unauthorized USB connections... (Ctrl+C to exit)      |
|                                                                         |
| ⚠️ [2026-04-21 23:14:05] UNAUTHORIZED USB DETECTED: 0781:5581 SanDisk ⚠️|
| +-----------------------------------------------------------------------+
```
*(A native desktop notification with a warning icon and audio alert will fire simultaneously)*

## 🧑‍💻 Installation
Since modern Linux distributions (like Debian 13 Trixie) enforce PEP 668 for Python packages, it is recommended to run this inside a virtual environment.

```bash
# Clone or create your project directory
mkdir ~/usb-trap && cd ~/usb-trap

# Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate

# Install the required dependencies
pip install -r requirements.txt
```

## 🧩 Requirements
Make sure you have these packages installed:
```bash
pip install notify-py
```
*(Note: Ensure your Linux distribution has the `usbutils` package installed for `lsusb` access, which is standard on Debian/Raspberry Pi OS).*

## 🚀 Usage
Run the app directly using Python from within your virtual environment:

```bash
python3 usb_trap.py
```

**Steps to use:**
1. Ensure only your *trusted* USB devices are plugged in.
2. Run the script. It will establish a baseline of authorized devices.
3. Leave the terminal window open in the background (or run via `nohup` / `tmux`).
4. If an unauthorized device is plugged in, the alarm will trigger and log the event.
5. Press `Ctrl+C` to disarm and exit.

## 🧠 Code Overview
```python
import os
import time
import subprocess
from notifypy import Notify
from datetime import datetime
```
The program:
* Uses standard `subprocess.check_output(['lsusb'])` to read the USB bus.
* Uses Python `sets` to calculate the difference between the initial baseline and the current polling cycle.
* Uses `notify-py` to pipe visual and audio alerts to the OS notification daemon.
* Handles device removals automatically so the state remains accurate.

## 📁 Project Structure
```text
usb-trap/
├── usb_trap.py            # Main detection and alarm script
├── requirements.txt       # Dependency list
├── README.md              # Documentation
├── siren.wav              # (Optional) Audio file for the alarm
└── usb_intrusion_log.txt  # Auto-generated log of unauthorized devices
```

## 🧾 Example Requirements File
```text
notify-py
```

## 🧱 Tech Stack

| Component | Description |
| :--- | :--- |
| **Python** | Core scripting language |
| **notify-py** | Cross-platform OS-level notification library |
| **lsusb (usbutils)** | Linux utility for displaying information about USB buses |
| **LXQt / X11** | Target Desktop Environment for visual alerts |

## 🛡️ Event Handling & Alerts
* `[*] Baseline established.` → Safe state, script is armed.
* `[red]UNAUTHORIZED USB DETECTED[/red]` → Rogue device plugged in. Triggers alert and log.
* `[!] Error reading USB bus` → Failsafe if `lsusb` is interrupted or missing.

## 💡 Future Improvements
- [ ] Run as a background `systemd` service on boot.
- [ ] Automatically attempt to unbind/disable the rogue USB port via sysfs (`/sys/bus/usb/drivers/usb/unbind`).
- [ ] Send push notifications to a mobile device (via Telegram bot or Pushover) when away from the keyboard.
- [ ] Take a webcam snapshot using `fswebcam` when the trap is triggered.
