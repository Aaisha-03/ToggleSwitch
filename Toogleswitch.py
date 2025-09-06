import tkinter as tk
from datetime import datetime
import threading
import time
import winsound  # For Windows sound — optional

# Create main window
root = tk.Tk()
root.title("Advanced Toggle Switch")
root.geometry("400x400")
root.configure(bg="white")

# Global state variables
is_on = False
toggle_count = 0
dark_mode = False

# --- Functions ---

# Function to play sound (only on Windows)
def play_sound():
    try:
        winsound.Beep(1000, 100)  # frequency, duration
    except:
        pass  # If on another OS, just skip

# Function to auto-turn-off after 10 seconds
def auto_off_timer():
    global is_on
    time.sleep(10)
    if is_on:
        toggle_state(auto_off=True)

# Toggle function
def toggle_state(auto_off=False):
    global is_on, toggle_count

    is_on = not is_on if not auto_off else False
    play_sound()

    if is_on:
        toggle_button.config(text="ON", bg="green", fg="white")
        status_label.config(text="Switch is ON", fg="green")
        toggle_count += 1
        log_to_file("ON")
        threading.Thread(target=auto_off_timer, daemon=True).start()
    else:
        toggle_button.config(text="OFF", bg="red", fg="white")
        status_label.config(text="Switch is OFF", fg="red")
        if not auto_off:
            toggle_count += 1
        log_to_file("OFF")

    time_label.config(text="Last toggled: " + datetime.now().strftime("%H:%M:%S"))
    count_label.config(text=f"Toggle Count: {toggle_count}")

# Theme toggle
def toggle_theme():
    global dark_mode
    dark_mode = not dark_mode

    bg_color = "black" if dark_mode else "white"
    fg_color = "white" if dark_mode else "black"

    root.configure(bg=bg_color)
    for widget in root.winfo_children():
        if isinstance(widget, tk.Label) or isinstance(widget, tk.Button):
            widget.configure(bg=bg_color, fg=fg_color if widget != toggle_button else widget.cget("fg"))

# Reset function
def reset_all():
    global toggle_count, is_on
    toggle_count = 0
    is_on = False
    toggle_button.config(text="OFF", bg="red", fg="white")
    status_label.config(text="Switch is OFF", fg="red")
    count_label.config(text="Toggle Count: 0")
    time_label.config(text="Last toggled: N/A")
    log_to_file("RESET")

# Save toggle logs
def log_to_file(state):
    with open("toggle_log.txt", "a") as f:
        f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Switch turned {state}\n")

# --- Widgets ---

toggle_button = tk.Button(root, text="OFF", width=12, height=2, bg="red", fg="white", command=toggle_state)
toggle_button.pack(pady=20)

status_label = tk.Label(root, text="Switch is OFF", font=("Arial", 12), fg="red", bg="white")
status_label.pack()

time_label = tk.Label(root, text="Last toggled: N/A", font=("Arial", 10), bg="white")
time_label.pack(pady=5)

count_label = tk.Label(root, text="Toggle Count: 0", font=("Arial", 10), bg="white")
count_label.pack(pady=5)

# Reset Button
reset_button = tk.Button(root, text="Reset", command=reset_all, bg="blue", fg="white")
reset_button.pack(pady=10)

# Theme Toggle
theme_button = tk.Button(root, text="Toggle Dark Mode", command=toggle_theme, bg="gray", fg="white")
theme_button.pack(pady=10)

# Exit Button
exit_button = tk.Button(root, text="Exit", command=root.destroy, bg="black", fg="white")
exit_button.pack(pady=10)

# Start the app
root.mainloop()
