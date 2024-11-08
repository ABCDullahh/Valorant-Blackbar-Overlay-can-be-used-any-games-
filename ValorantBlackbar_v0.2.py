import tkinter as tk
from tkinter import messagebox, ttk
import pygame
import sys
import win32gui
import win32con
import win32api
import ctypes
import psutil
import os
import keyboard
from time import sleep
from threading import Thread

# Masukkan nama proses game
game_process_name = 'VALORANT-Win64-Shipping.exe'

# Inisialisasi flag dan variabel
overlay_active = False
overlay_thread = None
shortcut_key = "F9"  # Default shortcut key
listening_for_key = False
DEFAULT_BLACK_BAR_WIDTH = 12.5  # Default width percentage (for 4:3)
black_bar_width_percentage = DEFAULT_BLACK_BAR_WIDTH



def set_game_priority_to_high():
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] == game_process_name:
            try:
                proc.nice(psutil.HIGH_PRIORITY_CLASS)
                print(f"Set priority of {game_process_name} to High")
            except psutil.AccessDenied:
                print("Access Denied: Run this script as administrator to set process priority.")
            return
    print(f"{game_process_name} not found. Ensure the game is running.")

def suggest_close_background_apps():
    print("Analyzing background applications for potential performance impact:")
    for proc in psutil.process_iter(['name', 'cpu_percent', 'memory_info']):
        if proc.info['cpu_percent'] > 1 or (proc.info['memory_info'] and proc.info['memory_info'].rss > 100 * 1024 * 1024):
            print(f"- {proc.info['name']}: CPU {proc.info['cpu_percent']}%, Memory {proc.info['memory_info'].rss / (1024 * 1024):.2f} MB")
    print("Consider manually closing these applications to improve game performance.")

def optimize_gpu_settings():
    try:
        os.system("nvidia-smi -pm 1")
        print("NVIDIA GPU set to maximum performance mode.")
    except Exception as e:
        print(f"Error optimizing GPU settings: {e}. Please manually adjust GPU settings.")

def update_black_bar_width(value):
    global black_bar_width_percentage
    black_bar_width_percentage = float(value)
    black_bar_label.config(text=f"Black Bar Width: {value}%")

def activate_overlay():
    global overlay_active, overlay_thread
    if not overlay_active:
        overlay_active = True
        overlay_thread = Thread(target=start_overlay)
        overlay_thread.start()
        print("Overlay activated.")
        status_label.config(text="Status: Active")
        
        # Disable black bar controls when overlay is active
        black_bar_slider.config(state='disabled')
        btn_reset_overlay.config(state='disabled')
        black_bar_label.config(text=f"Black Bar Width: {black_bar_width_percentage}% (Locked)")

def deactivate_overlay():
    global overlay_active
    overlay_active = False
    print("Overlay deactivated.")
    status_label.config(text="Status: Inactive")
    
    # Re-enable black bar controls when overlay is inactive
    black_bar_slider.config(state='normal')
    btn_reset_overlay.config(state='normal')
    black_bar_label.config(text=f"Black Bar Width: {black_bar_width_percentage}%")

def reset_overlay():
    global black_bar_width_percentage
    black_bar_width_percentage = DEFAULT_BLACK_BAR_WIDTH
    black_bar_slider.set(DEFAULT_BLACK_BAR_WIDTH)
    black_bar_label.config(text=f"Black Bar Width: {DEFAULT_BLACK_BAR_WIDTH}%")
    messagebox.showinfo("Reset Complete", "Overlay settings have been reset to default (4:3 ratio)")

def start_overlay():
    global overlay_active
    pygame.init()
    screen_info = pygame.display.Info()
    screen_width, screen_height = screen_info.current_w, screen_info.current_h
    
    # Hitung lebar bar berdasarkan persentase
    bar_width = int(screen_width * (black_bar_width_percentage / 100))

    screen = pygame.display.set_mode((screen_width, screen_height), pygame.NOFRAME)
    black = (0, 0, 0)
    hwnd = pygame.display.get_wm_info()['window']
    win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, screen_width, screen_height, 0)
    extended_style = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
    win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, extended_style | win32con.WS_EX_LAYERED | win32con.WS_EX_TRANSPARENT)
    ctypes.windll.user32.SetLayeredWindowAttributes(hwnd, win32api.RGB(255, 255, 255), 0, win32con.LWA_COLORKEY)
    
    p = psutil.Process()
    p.nice(psutil.IDLE_PRIORITY_CLASS)

    clock = pygame.time.Clock()
    first_draw = True

    while overlay_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                overlay_active = False

        if overlay_active and first_draw:
            screen.fill((255, 255, 255))
            pygame.draw.rect(screen, black, (0, 0, bar_width, screen_height))
            pygame.draw.rect(screen, black, (screen_width - bar_width, 0, bar_width, screen_height))
            pygame.display.update()
            first_draw = False
        elif not overlay_active:
            screen.fill((255, 255, 255))
            pygame.display.update()

        clock.tick(30)

    pygame.quit()
    sys.exit()

def activate_overlay():
    global overlay_active, overlay_thread
    if not overlay_active:
        overlay_active = True
        overlay_thread = Thread(target=start_overlay)
        overlay_thread.start()
        print("Overlay activated.")
        status_label.config(text="Status: Active")

def deactivate_overlay():
    global overlay_active
    overlay_active = False
    print("Overlay deactivated.")
    status_label.config(text="Status: Inactive")

def toggle_overlay():
    global overlay_active
    if overlay_active:
        deactivate_overlay()
    else:
        activate_overlay()

def start_listening_for_key():
    global listening_for_key
    listening_for_key = True
    shortcut_entry.config(state='normal')
    shortcut_entry.delete(0, tk.END)
    shortcut_entry.insert(0, "Press any key...")
    shortcut_entry.config(state='readonly')
    btn_set_shortcut.config(text="Cancel", command=stop_listening_for_key)
    
    # Disable other buttons while listening
    btn_optimize.config(state='disabled')
    btn_activate_overlay.config(state='disabled')
    btn_deactivate_overlay.config(state='disabled')
    btn_exit.config(state='disabled')
    black_bar_slider.config(state='disabled')

def stop_listening_for_key():
    global listening_for_key
    listening_for_key = False
    shortcut_entry.config(state='normal')
    shortcut_entry.delete(0, tk.END)
    shortcut_entry.insert(0, shortcut_key)
    shortcut_entry.config(state='readonly')
    btn_set_shortcut.config(text="Change Shortcut", command=start_listening_for_key)
    
    # Re-enable other buttons
    btn_optimize.config(state='normal')
    btn_activate_overlay.config(state='normal')
    btn_deactivate_overlay.config(state='normal')
    btn_exit.config(state='normal')
    black_bar_slider.config(state='normal')

def on_key_press(event):
    global shortcut_key, listening_for_key
    if listening_for_key and event.keysym != 'Escape':
        try:
            # Remove old shortcut
            keyboard.remove_hotkey(shortcut_key)
            # Update shortcut
            shortcut_key = event.keysym
            # Add new shortcut
            keyboard.add_hotkey(shortcut_key, toggle_overlay)
            # Update entry field
            shortcut_entry.config(state='normal')
            shortcut_entry.delete(0, tk.END)
            shortcut_entry.insert(0, shortcut_key)
            shortcut_entry.config(state='readonly')
            # Reset listening state
            stop_listening_for_key()
            messagebox.showinfo("Shortcut Updated", f"Shortcut updated to {shortcut_key}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to set shortcut: {str(e)}")
            stop_listening_for_key()
    elif listening_for_key and event.keysym == 'Escape':
        stop_listening_for_key()

def optimize_game_performance():
    print("Optimizing game performance...")
    set_game_priority_to_high()
    suggest_close_background_apps()
    optimize_gpu_settings()
    print("Optimization complete.")
    messagebox.showinfo("Optimization Complete", "Game performance optimization completed!")

def exit_app():
    deactivate_overlay()
    root.destroy()

# GUI Setup dengan tema modern
root = tk.Tk()
root.title("Game Overlay & Optimizer")
root.resizable(False, False)  # Membuat window fixed

# Set tema
style = ttk.Style()
style.theme_use('clam')

# Menghitung posisi untuk center window
window_width = 450
window_height = 670
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
center_x = int((screen_width - window_width) / 2)
center_y = int((screen_height - window_height) / 2)
root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')


# Bind key press event to root window
root.bind('<Key>', on_key_press)

# Main container dengan padding
main_container = ttk.Frame(root, padding="10")
main_container.pack(fill="both", expand=True)

# Judul
title_frame = ttk.Frame(main_container)
title_frame.pack(fill="x", pady=(0, 10))
label = ttk.Label(title_frame, text="Game Overlay & Optimizer", font=("Arial", 16, "bold"))
label.pack()

# Status Label
status_label = ttk.Label(title_frame, text="Status: Inactive", font=("Arial", 10))
status_label.pack(pady=(5, 0))

# Modify black bar frame for better user feedback
black_bar_frame = ttk.LabelFrame(main_container, text="Black Bar Settings", padding=10)
black_bar_frame.pack(fill="x", pady=(0, 10))

# Info label
info_label = ttk.Label(black_bar_frame, 
                      text="Note: Black bar settings cannot be changed while overlay is active",
                      font=("Arial", 8),
                      wraplength=400)
info_label.pack(pady=(0, 5))

# Label untuk black bar width
black_bar_label = ttk.Label(black_bar_frame, text=f"Black Bar Width: {black_bar_width_percentage}%")
black_bar_label.pack()

# Slider untuk black bar width
black_bar_slider = ttk.Scale(
    black_bar_frame,
    from_=0,
    to=25,  # Maximum 25% of screen width
    value=black_bar_width_percentage,
    orient="horizontal",
    command=update_black_bar_width
)
black_bar_slider.pack(fill="x", pady=5)

# Tombol Reset overlay
btn_reset_overlay = ttk.Button(black_bar_frame, text="Reset to 4:3 (Default)", command=reset_overlay)
btn_reset_overlay.pack(fill="x", pady=(5, 0))

# Frame untuk shortcut control
shortcut_frame = ttk.LabelFrame(main_container, text="Shortcut Settings", padding=10)
shortcut_frame.pack(fill="x", pady=(0, 10))

shortcut_entry = ttk.Entry(shortcut_frame)
shortcut_entry.insert(0, shortcut_key)
shortcut_entry.config(state='readonly')
shortcut_entry.pack(fill="x", pady=5)

btn_set_shortcut = ttk.Button(shortcut_frame, text="Change Shortcut", command=start_listening_for_key)
btn_set_shortcut.pack(fill="x")

# Frame untuk control buttons
control_frame = ttk.LabelFrame(main_container, text="Controls", padding=10)
control_frame.pack(fill="x")

btn_optimize = ttk.Button(control_frame, text="Optimize Performance", command=optimize_game_performance)
btn_optimize.pack(fill="x", pady=(0, 5))

btn_activate_overlay = ttk.Button(control_frame, text="Activate Overlay", command=activate_overlay)
btn_activate_overlay.pack(fill="x", pady=5)

btn_deactivate_overlay = ttk.Button(control_frame, text="Deactivate Overlay", command=deactivate_overlay)
btn_deactivate_overlay.pack(fill="x", pady=5)

btn_exit = ttk.Button(control_frame, text="Exit", command=exit_app)
btn_exit.pack(fill="x", pady=(5, 0))

# Modified start_listening_for_key to disable reset button
def start_listening_for_key():
    global listening_for_key
    listening_for_key = True
    shortcut_entry.config(state='normal')
    shortcut_entry.delete(0, tk.END)
    shortcut_entry.insert(0, "Press any key...")
    shortcut_entry.config(state='readonly')
    btn_set_shortcut.config(text="Cancel", command=stop_listening_for_key)
    
    # Disable other buttons while listening
    btn_optimize.config(state='disabled')
    btn_activate_overlay.config(state='disabled')
    btn_deactivate_overlay.config(state='disabled')
    btn_exit.config(state='disabled')
    black_bar_slider.config(state='disabled')
    btn_reset_overlay.config(state='disabled')  # Disable reset button



keyboard.add_hotkey(shortcut_key, toggle_overlay)

credits_frame = ttk.LabelFrame(main_container, text="Credits", padding=10)
credits_frame.pack(fill="x", pady=(10, 0))

author_label = ttk.Label(credits_frame, text="ABCDullahh", font=("Arial", 10))
author_label.pack()

github_link = ttk.Label(credits_frame, text="GitHub", font=("Arial", 9), foreground="blue", cursor="hand2")
github_link.pack()
github_link.bind("<Button-1>", lambda e: os.system("start https://github.com/ABCDullahh"))

# Jalankan aplikasi GUI
if __name__ == "__main__":
    root.mainloop()