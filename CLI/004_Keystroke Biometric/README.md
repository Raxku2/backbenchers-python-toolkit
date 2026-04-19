# 🛡️ Keystroke Biometric Sentinel

A lightweight, machine-learning-powered security daemon that learns your unique typing rhythm and automatically locks your operating system if a different user tries to type on your machine.

Unlike traditional security tools, the Sentinel uses **Behavioral Biometrics**. It doesn't care *what* you type; it cares *how* you type.

## 🧠 How It Works

The Sentinel monitors two critical hardware metrics in real-time:
1. **Dwell Time:** The exact duration a specific key is held down (press to release).
2. **Flight Time:** The latency between releasing one key and pressing the next.

**The Pipeline:**
* **Phase 1: Profiling (Training)** - The script runs silently in the background, capturing your next *N* keystrokes to build a multidimensional baseline of your normal typing behavior.
* **Phase 2: Monitoring (Inference)** - Using `scikit-learn`'s `IsolationForest` algorithm, the Sentinel compares real-time keystrokes against your established baseline. 
* **Phase 3: Action** - If it detects consecutive anomalies (e.g., someone with heavier fingers or a slower cadence), it triggers an immediate OS-level lock.

## 🚀 Features
* **Zero-Latency ML:** Uses classical Machine Learning (no heavy LLMs or GPUs required), making it perfect for low-resource hardware like the Raspberry Pi.
* **Privacy First:** Logs *timing data only*. It does not record or store the actual characters you type.
* **Completely Local:** No cloud APIs, no network requests.

## 🛠️ Prerequisites

* Python 3.8+
* An X11-based Desktop Environment (Tested on Debian/LXQt/Openbox). *Note: Wayland support for global keylogging requires different system-level hooks.*

### Dependencies
Install the required Python libraries:
```bash
pip install pynput pandas scikit-learn numpy
```
*(If you are on Debian 12+, you may need to run this inside a `venv` or use `--break-system-packages` if you prefer installing globally at your own risk).*

## ⚙️ Configuration

You can tweak the core behavior by modifying the variables at the top of `sentinel.py`:

```python
TRAINING_SAMPLES = 200  # Number of keystrokes needed to build your profile.
ANOMALY_THRESHOLD = 3   # How many weird keystrokes trigger the lock.
LOCK_COMMAND = ["xdg-screensaver", "lock"] # The OS lock command.
```
*Tip for LXQt users: If `xdg-screensaver` fails, change the `LOCK_COMMAND` to `["lxqt-leave", "--lockscreen"]`.*

## 🏃 Usage

Start the sentinel from your terminal:

```bash
python3 sentinel.py
```

1. **Keep typing normally.** The terminal will show a progress counter (e.g., `Training... 45/200`).
2. Once the baseline is established, it will output `[*] Sentinel Armed.`
3. **Test it:** Ask a friend to type a few sentences, or try typing with a drastically different posture/speed using only two fingers. The screen should lock.

## ⚠️ Troubleshooting & X11 Notes

Because `pynput` hooks directly into the X server's input stream, **you must run this script natively in your GUI user space.**
* **SSH Sessions:** If you start this script via an SSH session to your machine, it will likely fail to capture keystrokes or fail to lock the screen because it doesn't have access to the `$DISPLAY` environment variable.
* **Terminal Emulators:** Run it directly inside `xfce4-terminal` or your preferred terminal emulator on your actual desktop.
