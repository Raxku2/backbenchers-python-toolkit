import time
import subprocess
import threading
import numpy as np
import pandas as pd
from pynput import keyboard
from sklearn.ensemble import IsolationForest

# --- CONFIGURATION ---
TRAINING_SAMPLES = 200  # Number of keystrokes to learn your rhythm
ANOMALY_THRESHOLD = 3   # Consecutive anomalies before locking
LOCK_COMMAND = ["xdg-screensaver", "lock"] # Standard X11/LXQt lock command
# Alternate if xdg fails on your setup: ["lxqt-leave", "--lockscreen"]

class KeystrokeSentinel:
    def __init__(self):
        self.key_press_times = {}
        self.last_release_time = None
        
        self.features = []      # Stores [dwell_time, flight_time]
        self.model = IsolationForest(contamination=0.05, random_state=42)
        self.is_trained = False
        self.anomaly_count = 0

    def lock_system(self):
        print("\n[!] ANOMALY DETECTED. LOCKING OS.")
        try:
            subprocess.run(LOCK_COMMAND, check=True)
            # Reset anomaly count after lock
            self.anomaly_count = 0 
        except Exception as e:
            print(f"Failed to lock: {e}")

    def on_press(self, key):
        self.key_press_times[key] = time.time()

    def on_release(self, key):
        current_time = time.time()
        
        # Calculate Dwell Time (How long the key was held)
        if key in self.key_press_times:
            dwell_time = current_time - self.key_press_times[key]
            del self.key_press_times[key]
        else:
            dwell_time = 0.1 # Fallback

        # Calculate Flight Time (Time between last release and this release)
        if self.last_release_time is not None:
            flight_time = current_time - self.last_release_time
        else:
            flight_time = 0.1 # Fallback
            
        self.last_release_time = current_time

        # Ignore abnormally long pauses (e.g., stopping to read)
        if flight_time > 2.0:
            return

        vector = [dwell_time, flight_time]
        
        if not self.is_trained:
            self.features.append(vector)
            print(f"Training... {len(self.features)}/{TRAINING_SAMPLES}", end="\r")
            
            if len(self.features) >= TRAINING_SAMPLES:
                self.train_model()
        else:
            self.evaluate_rhythm(vector)

    def train_model(self):
        print("\n[*] Training model on baseline typing rhythm...")
        df = pd.DataFrame(self.features, columns=['dwell', 'flight'])
        self.model.fit(df)
        self.is_trained = True
        print("[*] Sentinel Armed. Monitoring for anomalies.")

    def evaluate_rhythm(self, vector):
        df = pd.DataFrame([vector], columns=['dwell', 'flight'])
        prediction = self.model.predict(df)[0]
        
        # IsolationForest returns 1 for normal, -1 for anomaly
        if prediction == -1:
            self.anomaly_count += 1
            print(f"[!] Strike {self.anomaly_count}/{ANOMALY_THRESHOLD}")
            if self.anomaly_count >= ANOMALY_THRESHOLD:
                self.lock_system()
        else:
            # Decay the anomaly count if normal typing resumes
            self.anomaly_count = max(0, self.anomaly_count - 1)

    def start(self):
        print("[*] Starting Keystroke Sentinel...")
        print(f"[*] Type normally to build profile ({TRAINING_SAMPLES} strokes required).")
        with keyboard.Listener(on_press=self.on_press, on_release=self.on_release) as listener:
            listener.join()

if __name__ == "__main__":
    sentinel = KeystrokeSentinel()
    sentinel.start()