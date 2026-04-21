import os
import time
import subprocess
from notifypy import Notify
from datetime import datetime

LOG_FILE = "usb_intrusion_log.txt"
# Optional: Point this to a loud .wav file on your Pi for the "blaring" effect
ALARM_AUDIO_PATH = "" 

def get_connected_usbs():
    """Reads current USB devices and returns a set of Hardware IDs and Names."""
    devices = set()
    try:
        # lsusb outputs format: Bus 001 Device 002: ID 8087:0024 Intel Corp. ...
        result = subprocess.check_output(['lsusb'], text=True)
        for line in result.strip().split('\n'):
            if line:
                # Split at 'ID ' to extract the 'HardwareID DeviceName'
                parts = line.split("ID ")
                if len(parts) > 1:
                    hw_info = parts[1].strip()
                    # Filter out standard Linux Foundation root hubs to reduce noise
                    if "Linux Foundation" not in hw_info:
                        devices.add(hw_info)
    except Exception as e:
        print(f"[!] Error reading USB bus: {e}")
    return devices

def trigger_alarm(device_info):
    """Triggers the OS-level notification and logs the event."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] UNAUTHORIZED USB DETECTED: {device_info}\n"
    
    # 1. Log to file
    with open(LOG_FILE, "a") as f:
        f.write(log_entry)
    
    # 2. Print to terminal
    print(f"\033[91m{log_entry}\033[0m", end="")

    # 3. Fire OS Notification
    notification = Notify()
    notification.title = "⚠️ SECURITY ALERT: USB TRAP ⚠️"
    notification.message = f"Unauthorized device mounted:\n{device_info}"
    notification.icon = "/usr/share/icons/Papirus-Dark/48x48/status/dialog-warning.svg" # Uses your Papirus icon theme
    
    # Add audio if configured
    if ALARM_AUDIO_PATH and os.path.exists(ALARM_AUDIO_PATH):
        notification.audio = ALARM_AUDIO_PATH

    notification.send()

def main():
    print("[*] Initializing USB Booby Trap...")
    print(f"[*] OS: Debian 13 (Trixie) | Display: LXQt")
    
    # Establish the baseline of currently connected/authorized devices
    authorized_devices = get_connected_usbs()
    
    print(f"[*] Baseline established. {len(authorized_devices)} authorized device(s) found.")
    for dev in authorized_devices:
        print(f"    - {dev}")
        
    print("\n[*] Listening for unauthorized USB connections... (Ctrl+C to exit)")

    try:
        while True:
            time.sleep(1.5) # Polling interval
            current_devices = get_connected_usbs()
            
            # Find devices that are currently connected but weren't in our authorized list
            intruders = current_devices - authorized_devices
            
            if intruders:
                for intruder in intruders:
                    trigger_alarm(intruder)
                
                # Add intruder to known devices so the alarm doesn't loop infinitely 
                # until it is removed and plugged back in
                authorized_devices = current_devices
                
            # Handle removals (so if an authorized device is removed and an intruder 
            # spoofs it later, or if an intruder is unplugged, we reset state)
            removals = authorized_devices - current_devices
            if removals:
                authorized_devices = current_devices

    except KeyboardInterrupt:
        print("\n[*] USB Booby Trap disarmed. Shutting down.")

if __name__ == "__main__":
    main()