import tkinter as tk
from tkinter import ttk
import subprocess

# Initialize variables
variables = {
    "fps": 60,
    "res": 1920,
    "no_video": False,
    "no_control": False,
    "use_camera": False,
    "screen": 0,
    "device": "Default",
    "audio": "Default",
    "show_touches": False,
    "turn_screen_off": False,
    "stay_awake": False,
    "always_on_top": False
}

import os

def flag_builder():
    flags = []
    
    # No Video
    if variables["no_video"]:
        flags.append("--no-video")
    
    # Use Camera
    if variables["use_camera"]:
        flags.append("--video-source=camera")
        if variables["camera"] == "Back":
            flags.append("--camera-facing=back")
        else:
            flags.append("--camera-facing=front")
            
    # Audio
    if variables["audio"] != "Default":
        if variables["audio"] == "None":
            flags.append("--no-audio")
        if variables["audio"] == "Playback":
            flags.append("--audio-dup")
        if variables["audio"] == "Microphone":
            flags.append("--audio-source=mic")
            
    # No Control
    if variables["no_control"]:
        flags.append("--no-control")
        
    # Screen
    if variables["screen"] != 0:
        flags.append(f"--display-id={variables['screen']}")
        
    # Device
    if variables["device"] != "Default":
        if variables["device"] == "USB":
            flags.append("-d")
        elif variables["device"] == "TCP":
            flags.append("-e")
        
    # Stay Awake
    if variables["stay_awake"]:
        flags.append("--stay-awake")
        
    # Show Touches
    if variables["show_touches"]:
        flags.append("--show-touches")
        
    # Turn Screen Off
    if variables["turn_screen_off"]:
        flags.append("--turn-screen-off")
        
    # Always On Top
    if variables["always_on_top"]:
        flags.append("--always-on-top")
    
    # Max FPS
    if variables["fps"] != 0 and not variables["no_video"]:
        flags.append(f"--max-fps={variables['fps']}")
    
    # Max Resolution
    if variables["res"] != 0 and not variables["no_video"]:
        flags.append(f"--max-size={variables['res']}")
        
    # execute the command
    command = ["scrcpy"] + flags
    print("Executing command with flags:", command)
    fdir = os.path.dirname(os.path.realpath(__file__))
    print(fdir)
    
    # change directory to the script directory
    os.chdir(fdir)

    # execute the command
    subprocess.run(command)
    


# Update variables function
def update_variables():
    variables["fps"] = fps_var.get()
    variables["res"] = res_var.get()
    variables["no_video"] = no_video_var.get()
    variables["no_control"] = no_control_var.get() 
    variables["use_camera"] = use_camera_var.get()
    variables["camera"] = camera_var.get() if use_camera_var.get() else None
    variables["screen"] = screen_var.get()
    variables["device"] = device_var.get()
    variables["audio"] = audio_var.get()
    variables["show_touches"] = show_touches_var.get()
    variables["turn_screen_off"] = turn_screen_off_var.get()
    variables["stay_awake"] = stay_awake_var.get()
    variables["always_on_top"] = always_on_top_var.get()

# Submit function
def submit():
    
    update_variables()
    flag_builder()

# Toggle camera options
def toggle_camera_options():
    if use_camera_var.get():
        camera_combobox.grid(row=camera_row, column=1, padx=10, pady=5)
    else:
        camera_combobox.grid_remove()

# Initialize main window
root = tk.Tk()
root.title("SCRCPY Launcher")

# Dynamic row counter
current_row = 0

# Max FPS
ttk.Label(root, text="Max FPS (1 - 144)").grid(row=current_row, column=0, padx=10, pady=5)
fps_var = tk.IntVar(value=variables["fps"])
fps_spinbox = ttk.Spinbox(root, from_=0, to=144, increment=1, textvariable=fps_var, width=10)
fps_spinbox.grid(row=current_row, column=1, padx=10, pady=5)
current_row += 1

# Max Resolution
ttk.Label(root, text="Max Resolution (1 - 4096)").grid(row=current_row, column=0, padx=10, pady=5)
res_var = tk.IntVar(value=variables["res"])
res_spinbox = ttk.Spinbox(root, from_=0, to=4096, increment=1, textvariable=res_var, width=10)
res_spinbox.grid(row=current_row, column=1, padx=10, pady=5)
current_row += 1

# No Video Checkbox
no_video_var = tk.BooleanVar()
no_video_check = ttk.Checkbutton(root, text="No Video", variable=no_video_var)
no_video_check.grid(row=current_row, column=0, columnspan=1, padx=10, pady=5)

# No Control Checkbox
no_control_var = tk.BooleanVar()
no_control_check = ttk.Checkbutton(root, text="No Control", variable=no_control_var)
no_control_check.grid(row=current_row, column=1, columnspan=1, padx=10, pady=5)
current_row += 1

# Use Camera Checkbox
use_camera_var = tk.BooleanVar()
use_camera_check = ttk.Checkbutton(root, text="Use Camera", variable=use_camera_var)
use_camera_check.grid(row=current_row, column=0, columnspan=1, padx=10, pady=5)
use_camera_var.trace_add('write', lambda *args: toggle_camera_options())

# Camera options
cameras = ["Front", "Back"]
camera_var = tk.StringVar(value=cameras[0])
camera_combobox = ttk.Combobox(root, textvariable=camera_var, values=cameras, state='readonly')
camera_row = current_row
camera_combobox.grid(row=camera_row, column=1, padx=10, pady=5)
camera_combobox.grid_remove()
current_row += 1

# Audio options
ttk.Label(root, text="Audio").grid(row=current_row, column=0, padx=10, pady=5)
audio_options = ["Default", "None", "Playback", "Microphone"]
audio_var = tk.StringVar(value=variables["audio"])
audio_combobox = ttk.Combobox(root, textvariable=audio_var, values=audio_options, state='readonly')
audio_combobox.grid(row=current_row, column=1, padx=10, pady=5)
current_row += 1

# Screen Field
ttk.Label(root, text="Screen").grid(row=current_row, column=0, padx=10, pady=5)
screen_var = tk.IntVar(value=variables["screen"])
screen_entry = ttk.Spinbox(root, from_=0, to=4, textvariable=screen_var, width=10)
screen_entry.grid(row=current_row, column=1, padx=10, pady=5)
current_row += 1

# Device options
ttk.Label(root, text="Device").grid(row=current_row, column=0, padx=10, pady=5)
devices = ["Default", "USB", "TCP"]
device_var = tk.StringVar(value=variables["device"])
device_combobox = ttk.Combobox(root, textvariable=device_var, values=devices, state='readonly')
device_combobox.grid(row=current_row, column=1, padx=10, pady=5)
current_row += 1

# Stay Awake Checkbox
stay_awake_var = tk.BooleanVar()
stay_awake_check = ttk.Checkbutton(root, text="Stay Awake", variable=stay_awake_var)
stay_awake_check.grid(row=current_row, column=0, columnspan=1, padx=10, pady=5)

# Show Touches Checkbox
show_touches_var = tk.BooleanVar()
show_touches_check = ttk.Checkbutton(root, text="Show Touches", variable=show_touches_var)
show_touches_check.grid(row=current_row, column=1, columnspan=1, padx=10, pady=5)
current_row += 1

# Turn Screen Off Checkbox
turn_screen_off_var = tk.BooleanVar()
turn_screen_off_check = ttk.Checkbutton(root, text="Turn Screen Off", variable=turn_screen_off_var)
turn_screen_off_check.grid(row=current_row, column=0, columnspan=1, padx=10, pady=5)

# Always On Top Checkbox
always_on_top_var = tk.BooleanVar()
always_on_top_check = ttk.Checkbutton(root, text="Always On Top", variable=always_on_top_var)
always_on_top_check.grid(row=current_row, column=1, columnspan=1, padx=10, pady=5)
current_row += 1

# Submit Button
submit_button = ttk.Button(root, text="Submit", command=submit)
submit_button.grid(row=current_row, column=0, padx=10, pady=10)

# Cancel Button
cancel_button = ttk.Button(root, text="Cancel", command=root.destroy)
cancel_button.grid(row=current_row, column=1, padx=10, pady=10)

# Start the main loop
root.mainloop()