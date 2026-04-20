import tkinter as tk
import time
import sys

class AggressiveBlocker:
    def __init__(self, duration_minutes):
        self.root = tk.Tk()
        self.duration = duration_minutes * 60
        self.time_left = self.duration

        # 1. Strip Openbox window decorations (No close/minimize buttons)
        self.root.overrideredirect(True)
        
        # 2. Force Fullscreen and Topmost
        self.root.attributes("-fullscreen", True)
        self.root.attributes("-topmost", True)
        
        # 3. Disable Alt+F4 and window closing protocols
        self.root.protocol("WM_DELETE_WINDOW", self.disable_event)
        
        # Styling
        self.root.configure(bg="#1e1e2e") # Dark background
        
        self.title_label = tk.Label(
            self.root, 
            text="󰈈 FOCUS SESSION ACTIVE", 
            font=("JetBrainsMono Nerd Font", 48, "bold"), 
            fg="#f38ba8", 
            bg="#1e1e2e"
        )
        self.title_label.pack(expand=True)

        self.timer_label = tk.Label(
            self.root, 
            text="", 
            font=("JetBrainsMono Nerd Font", 32), 
            fg="#cdd6f4", 
            bg="#1e1e2e"
        )
        self.timer_label.pack(pady=40)
        
        self.warning_label = tk.Label(
            self.root,
            text="Get back to work. This window cannot be closed.",
            font=("JetBrainsMono Nerd Font", 14),
            fg="#a6adc8",
            bg="#1e1e2e"
        )
        self.warning_label.pack(pady=20)

        # Start the aggressive loop and timer
        self.enforce_lock()
        self.update_timer()

    def disable_event(self):
        """Passes on delete events to prevent closing."""
        pass

    def enforce_lock(self):
        """Aggressively re-asserts dominance over the X11 window manager."""
        self.root.attributes("-topmost", True)
        self.root.lift()
        
        # Steal all mouse and keyboard input
        self.root.grab_set()
        self.root.focus_force()
        
        # Loop this check every 100ms so Openbox/LXQt panels can't override it
        self.root.after(100, self.enforce_lock)

    def update_timer(self):
        """Handles the countdown."""
        if self.time_left > 0:
            mins, secs = divmod(self.time_left, 60)
            self.timer_label.config(text=f"Time remaining: {mins:02d}:{secs:02d}")
            self.time_left -= 1
            self.root.after(1000, self.update_timer)
        else:
            # Release the grab and exit when time is up
            self.root.grab_release()
            self.root.destroy()
            sys.exit(0)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    # Set your focus time here (in minutes)
    WORK_SESSION_MINUTES = 25 
    
    print(f"Starting {WORK_SESSION_MINUTES}-minute focus session...")
    blocker = AggressiveBlocker(duration_minutes=WORK_SESSION_MINUTES)
    blocker.run()