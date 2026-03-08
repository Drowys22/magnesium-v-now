import customtkinter as ctk
from customtkinter import CTkImage
from PIL import Image
import subprocess
import json
import os
import math

GITHUB_REPO_URL = ""

app = None
output_box = None
entry = None
prompt_label = None
sidebar_open = False
sidebar_frame = None

PROMPT = "Magnesium > "

sidebar_icons_frame = None
sidebar_buttons = []

def create_sidebar_icons():
    global sidebar_icons_frame, sidebar_buttons
    config = load_main_config()
    sidebar_buttons = []
    if sidebar_icons_frame:
        sidebar_icons_frame.destroy()
    
    sidebar_icons_frame = ctk.CTkFrame(app, fg_color=config["bg_color"], width=50, corner_radius=0)
    sidebar_icons_frame.pack(side="left", fill="y")
    sidebar_icons_frame.pack_propagate(False)
    
    # Load icons
    help_icon = None
    if os.path.exists("showable/icons/info.png"):
        help_icon = CTkImage(Image.open("showable/icons/info.png"), size=(22, 22))
    
    filter_icon = None
    if os.path.exists("showable/icons/filter.png"):
        filter_icon = CTkImage(Image.open("showable/icons/filter.png"), size=(22, 22))
    
    database_icon = None
    if os.path.exists("showable/icons/database.png"):
        database_icon = CTkImage(Image.open("showable/icons/database.png"), size=(22, 22))
    
    folder_icon = None
    if os.path.exists("showable/icons/folder-open.png"):
        folder_icon = CTkImage(Image.open("showable/icons/folder-open.png"), size=(22, 22))
    
    workflow_icon = None
    if os.path.exists("showable/icons/workflow-alt.png"):
        workflow_icon = CTkImage(Image.open("showable/icons/workflow-alt.png"), size=(22, 22))
    
    shop_icon = None
    if os.path.exists("showable/icons/shop.png"):
        shop_icon = CTkImage(Image.open("showable/icons/shop.png"), size=(22, 22))
    
    pen_icon = None
    if os.path.exists("showable/icons/pen-clip.png"):
        pen_icon = CTkImage(Image.open("showable/icons/pen-clip.png"), size=(22, 22))
    
    tools = [
        ("", "Help", show_help_window, help_icon),
        ("", "Regex Tester", open_regex_tester, filter_icon),
        ("", "API Tester", open_api_tester, database_icon),
        ("", "File Explorer", open_file_explorer, folder_icon),
        ("", "Process Explorer", open_process_explorer, workflow_icon),
    ]
    
    for i, (icon_text, tooltip, cmd, img) in enumerate(tools):
        btn = ctk.CTkButton(sidebar_icons_frame, text=icon_text, command=cmd, fg_color=config["bg_color"], hover_color=config["accent_color"], text_color=config["fg_color"], font=("Segoe UI Symbol", 16), width=45, height=45, corner_radius=10, image=img)
        btn.pack(pady=4, padx=4)
        sidebar_buttons.append((btn, tooltip))
    
    sep = ctk.CTkFrame(sidebar_icons_frame, height=1, fg_color=config["fg_color"])
    sep.pack(fill="x", padx=5, pady=10)
    
    theme_icons = [
        ("", "Theme Store", open_store, shop_icon),
        ("", "Theme Creator", theme_creator, pen_icon),
    ]
    
    for i, (icon, tooltip, cmd, img) in enumerate(theme_icons):
        btn = ctk.CTkButton(sidebar_icons_frame, text=icon, command=cmd, fg_color=config["bg_color"], hover_color="#8B5CF6", text_color=config["fg_color"], font=("Segoe UI Symbol", 16), width=45, height=45, corner_radius=10, image=img)
        btn.pack(pady=4, padx=4)
        sidebar_buttons.append((btn, tooltip))

def toggle_sidebar():
    pass

def open_regex_tester():
    from tools.retest import RegexTester
    tester = RegexTester(app)

def open_api_tester():
    from tools.apitest import ApiTester
    tester = ApiTester(app)

def open_file_explorer():
    from tools.fiexpro import FileExplorerPro
    explorer = FileExplorerPro(app)

def open_process_explorer():
    from tools.proper import ProcessExplorer
    explorer = ProcessExplorer(app)

def load_main_config():
    if not os.path.exists("main_manager.json"):
        with open("main_manager.json", "w") as f:
            json.dump({"version": "v1.0.0", "last_shown_version": "", "bg_color": "#101010", "fg_color": "#E6E6E6", "accent_color": "#4A90E2", "entry_bg": "#181818", "entry_fg": "#FFFFFF", "license_key": "", "aliases": {}}, f, indent=4)
    with open("main_manager.json", "r") as f:
        data = json.load(f)
    if "version" not in data:
        data["version"] = "v1.0.0"
    if "last_shown_version" not in data:
        data["last_shown_version"] = ""
    if "license_key" not in data:
        data["license_key"] = ""
    if "aliases" not in data:
        data["aliases"] = {}
    return data

def save_main_config(data):
    with open("main_manager.json", "w") as f:
        json.dump(data, f, indent=4)

def list_theme_files():
    if not os.path.exists("themes"):
        os.makedirs("themes")
    return [f for f in os.listdir("themes") if f.endswith(".json")]

def install_theme(index):
    files = list_theme_files()
    if index < 1 or index > len(files):
        return "Invalid theme index.", None
    theme_path = os.path.join("themes", files[index - 1])
    with open(theme_path, "r") as f:
        theme_data = json.load(f)
    cfg = load_main_config()
    cfg.update({"bg_color": theme_data.get("bg_color", cfg["bg_color"]), "fg_color": theme_data.get("fg_color", cfg["fg_color"]), "accent_color": theme_data.get("accent_color", cfg["accent_color"]), "entry_bg": theme_data.get("entry_bg", cfg["entry_bg"]), "entry_fg": theme_data.get("entry_fg", cfg["entry_fg"])})
    save_main_config(cfg)
    return f"Theme '{files[index - 1]}' installed.", cfg

def run_cmd(command):
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.stdout if result.stdout else result.stderr
    except:
        return "Error executing command."

def apply_theme(theme):
    global prompt_label, top_bar, entry_frame
    app.configure(fg_color=theme["bg_color"])
    output_box.configure(fg_color=theme["bg_color"], text_color=theme["fg_color"])
    entry.configure(fg_color=theme["entry_bg"], text_color=theme["entry_fg"])
    if prompt_label:
        prompt_label.configure(text_color=theme["accent_color"])
    try:
        top_bar.configure(fg_color=theme["bg_color"])
        entry_frame.configure(fg_color=theme["bg_color"])
    except:
        pass

def notify(message, level="info", duration=2600):
    # Enhanced color schemes with better contrast
    colors = {
        "info": ("#60A5FA", "#1E3A8A", "#2563EB"),      # icon bg, frame bg, accent
        "success": ("#4ADE80", "#166534", "#22C55E"),   # icon bg, frame bg, accent
        "warning": ("#FBBF24", "#92400E", "#F59E0B"),    # icon bg, frame bg, accent
        "error": ("#F87171", "#991B1B", "#EF4444"),      # icon bg, frame bg, accent
        "System": ("#818CF8", "#3730A3", "#6366F1"),     # icon bg, frame bg, accent
    }
    
    # Icon symbols (cleaner, no emoji)
    icons = {
        "info": "ℹ",
        "success": "✓",
        "warning": "⚠",
        "error": "✕",
        "System": "⚡"
    }
    
    icon = icons.get(level, "ℹ")
    icon_bg, frame_bg, accent = colors.get(level, ("#E5E7EB", "#1E293B", "#60A5FA"))
    
    # Determine notification size based on message length
    msg_len = len(message)
    if msg_len > 35:
        width, height = 400, 100
        wraplength = 300
    else:
        width, height = 360, 85
        wraplength = 260
    
    win = ctk.CTkToplevel(app)
    win.overrideredirect(True)
    win.attributes("-topmost", True)
    win.attributes("-alpha", 0.0)
    
    # Function to update position to bottom-right of main app
    def update_position():
        if win.winfo_exists():
            app.update_idletasks()
            ax, ay = app.winfo_x(), app.winfo_y()
            # Position at bottom-right with 20px margin
            win.geometry(f"{width}x{height}+{ax + app.winfo_width() - width - 20}+{ay + app.winfo_height() - height - 20}")
    
    # Initial positioning
    update_position()
    
    # Bind to app movement to follow the main window
    def on_app_move(event):
        update_position()
    
    # Use after_bind to ensure we catch the move event
    app.bind("<Configure>", on_app_move)
    
    # Main outer frame with border effect
    outer_frame = ctk.CTkFrame(win, fg_color=frame_bg, corner_radius=16, border_width=2, border_color=accent)
    outer_frame.pack(fill="both", expand=True, padx=4, pady=4)
    
    # Inner content frame
    content_frame = ctk.CTkFrame(outer_frame, fg_color="transparent")
    content_frame.pack(fill="both", expand=True, padx=16, pady=12)
    
    # Close button (X) in top right
    close_btn = ctk.CTkButton(
        content_frame, 
        text="✕", 
        command=win.destroy,
        width=24, height=24,
        fg_color="transparent",
        hover_color=accent,
        text_color="#FFFFFF",
        font=("Segoe UI", 12, "bold"),
        corner_radius=12
    )
    close_btn.place(relx=1.0, rely=0.0, anchor="ne", x=0, y=-5)
    
    # Left side: Icon with circular background
    icon_container = ctk.CTkFrame(content_frame, fg_color=icon_bg, corner_radius=25, width=50, height=50)
    icon_container.pack(side="left", padx=(0, 14), pady=0)
    icon_container.pack_propagate(False)
    
    icon_label = ctk.CTkLabel(
        icon_container, 
        text=icon, 
        font=("Segoe UI", 22, "bold"), 
        text_color="#000000"
    )
    icon_label.pack(expand=True)
    
    # Right side: Text content
    text_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
    text_frame.pack(side="left", fill="both", expand=True)
    
    # Title/Level
    title_label = ctk.CTkLabel(
        text_frame, 
        text=level.upper(), 
        text_color=accent, 
        font=("Segoe UI", 11, "bold"), 
        anchor="w"
    )
    title_label.pack(anchor="w")
    
    # Message
    message_label = ctk.CTkLabel(
        text_frame, 
        text=message, 
        text_color="#FFFFFF", 
        font=("Segoe UI", 13), 
        anchor="w", 
        justify="left", 
        wraplength=wraplength
    )
    message_label.pack(anchor="w", fill="x", pady=(4, 0))
    
    # Progress bar at bottom
    progress = ctk.CTkProgressBar(
        outer_frame, 
        width=width-40, 
        height=6, 
        progress_color=accent,
        corner_radius=3
    )
    progress.pack(side="bottom", pady=(8, 8), padx=16)
    progress.set(0)
    
    # Animation functions
    def fade_in(step=0):
        if not win.winfo_exists(): return
        a = step / 12
        win.attributes("-alpha", 0.98 if a > 0.98 else a)
        if a <= 0.98: win.after(12, lambda: fade_in(step + 1))
    
    def fade_out(step=12):
        if not win.winfo_exists(): return
        a = step / 12
        if a <= 0: 
            win.destroy()
        else: 
            win.attributes("-alpha", a)
            win.after(15, lambda: fade_out(step - 1))
    
    def animate_progress(current=0):
        if not win.winfo_exists(): return
        progress.set(current / duration)
        if current < duration: 
            win.after(50, lambda: animate_progress(current + 50))
        else:
            # Auto close after animation completes
            win.after(300, fade_out)
    
    # Start animations
    fade_in()
    animate_progress(0)

def typewriter_insert(text):
    for line in text.split("\n"):
        _type_line(line)
        output_box.insert("end", "\n")
        output_box.see("end")

def _type_line(line):
    def step(i):
        if not output_box.winfo_exists(): return
        if i > len(line):
            output_box.see("end")
            return
        output_box.insert("end", line[i - 1])
        output_box.see("end")
        output_box.after(8, lambda: step(i + 1))
    step(1)

def exit_animation():
    win = ctk.CTkToplevel(app)
    win.title("Exiting Magnesium...")
    win.geometry("800x500")
    win.resizable(False, False)
    win.attributes("-alpha", 0.0)
    canvas = ctk.CTkCanvas(win, width=800, height=500, bg="#050505", highlightthickness=0)
    canvas.pack(fill="both", expand=True)
    messages = ["Saving settings...", "Closing processes...", "Cleaning up...", "Finalizing...", "Goodbye!"]
    total_time, steps, interval = 5000, 100, 50
    state = {"step": 0}
    
    def fade_in():
        if not win.winfo_exists(): return
        a = win.attributes("-alpha")
        if a < 0.9: win.attributes("-alpha", a + 0.05); win.after(16, fade_in)
        else: win.attributes("-alpha", 0.9)
    fade_in()
    
    def anim():
        if not win.winfo_exists(): return
        canvas.delete("all")
        t = state["step"] / steps
        size = 90 + 30 * t
        x, y, offset = 400, 250, 25
        canvas.create_polygon(x-size, y-size, x+size, y-size, x+size+offset, y-size+offset, x-size+offset, y-size+offset, fill="#0B1120", outline="#1E293B")
        canvas.create_polygon(x+size, y-size, x+size, y+size, x+size+offset, y+size+offset, x+size+offset, y-size+offset, fill="#111827", outline="#1F2937")
        canvas.create_polygon(x-size, y+size, x+size, y+size, x+size+offset, y+size+offset, x-size+offset, y+size+offset, fill="#020617", outline="#020617")
        fill_h = int(2 * size * t)
        canvas.create_rectangle(x-size+8, y+size-fill_h, x+size-8, y+size-8, fill="#4A90E2", outline="")
        msg_index = min(int(t * len(messages)), len(messages) - 1)
        canvas.create_text(400, 90, text=messages[msg_index], fill="#E5E7EB", font=("Segoe UI", 22, "bold"))
        state["step"] += 1
        if state["step"] > steps: win.destroy(); os._exit(0); return
        win.after(interval, anim)
    anim()

def confirm_exit():
    win = ctk.CTkToplevel(app)
    win.title("Confirm Exit")
    win.geometry("400x200")
    win.resizable(False, False)
    win.attributes("-alpha", 0.95)
    label = ctk.CTkLabel(win, text="Are you sure you want to exit Magnesium?", font=("Segoe UI", 18))
    label.pack(pady=20)
    def yes(): win.destroy(); exit_animation()
    def no(): win.destroy()
    b1 = ctk.CTkButton(win, text="Yes", command=yes, width=120).pack(pady=5)
    b2 = ctk.CTkButton(win, text="No", command=no, width=120).pack(pady=5)

def alias_menu():
    cfg = load_main_config()
    win = ctk.CTkToplevel(app)
    win.title("Magnesium Alias Manager")
    win.geometry("500x400")
    win.resizable(False, False)
    win.attributes("-alpha", 0.95)
    frame = ctk.CTkFrame(win, fg_color="#111827", corner_radius=12)
    frame.pack(fill="both", expand=True, padx=10, pady=10)
    ctk.CTkLabel(frame, text="Alias Manager", font=("Segoe UI", 20, "bold")).pack(pady=(15, 5))
    ctk.CTkLabel(frame, text="Create, edit and remove command aliases.", font=("Segoe UI", 12)).pack(pady=(0, 10))
    list_frame = ctk.CTkScrollableFrame(frame, fg_color="#020617", corner_radius=8, width=460, height=180)
    list_frame.pack(pady=5, padx=10)
    alias_labels = []
    
    def refresh_list():
        for w in alias_labels: w.destroy()
        alias_labels.clear()
        cfg2 = load_main_config()
        als = cfg2.get("aliases", {})
        if not als:
            lbl = ctk.CTkLabel(list_frame, text="No aliases defined.", font=("Consolas", 12))
            lbl.pack(anchor="w", padx=10, pady=2)
            alias_labels.append(lbl)
        else:
            for name, cmd in als.items():
                lbl = ctk.CTkLabel(list_frame, text=f"{name} -> {cmd}", font=("Consolas", 12))
                lbl.pack(anchor="w", padx=10, pady=2)
                alias_labels.append(lbl)
    refresh_list()
    
    key_entry = ctk.CTkEntry(frame, width=200, placeholder_text="Alias name").pack(pady=(10, 3))
    cmd_entry = ctk.CTkEntry(frame, width=200, placeholder_text="Command").pack(pady=3)
    msg_label = ctk.CTkLabel(frame, text="", font=("Segoe UI", 11)).pack(pady=(5, 5))
    
    def add_alias():
        name = key_entry.get().strip()
        cmd = cmd_entry.get().strip()
        if not name or not cmd:
            msg_label.configure(text="Both fields are required.", text_color="#F97373")
            return
        cfg3 = load_main_config()
        als = cfg3.get("aliases", {})
        als[name] = cmd
        cfg3["aliases"] = als
        save_main_config(cfg3)
        msg_label.configure(text="Alias saved.", text_color="#4ADE80")
        key_entry.delete(0, "end")
        cmd_entry.delete(0, "end")
        refresh_list()
    
    btn_frame = ctk.CTkFrame(frame, fg_color="#111827").pack(pady=(5, 15))
    ctk.CTkButton(btn_frame, text="Add / Update", command=add_alias, width=120).pack(side="left", padx=5)

def theme_creator():
    cfg = load_main_config()
    win = ctk.CTkToplevel(app)
    win.title("Magnesium Theme Creator")
    win.geometry("800x700")
    win.resizable(False, False)
    win.attributes("-alpha", 0.0)
    win.configure(fg_color="#0a0a0f")
    
    # Color name to hex mapping
    COLOR_NAMES = {
        "red": "#FF0000", "green": "#00FF00", "blue": "#0000FF",
        "yellow": "#FFFF00", "cyan": "#00FFFF", "magenta": "#FF00FF",
        "white": "#FFFFFF", "black": "#000000", "orange": "#FFA500",
        "purple": "#800080", "pink": "#FFC0CB", "brown": "#A52A2A",
        "gray": "#808080", "grey": "#808080", "lime": "#00FF00",
        "aqua": "#00FFFF", "olive": "#808000", "navy": "#000080",
        "teal": "#008080", "maroon": "#800000", "silver": "#C0C0C0",
        "gold": "#FFD700", "coral": "#FF7F50", "salmon": "#FA8072",
        "plum": "#DDA0DD", "violet": "#EE82EE", "indigo": "#4B0082",
        "beige": "#F5F5DC", "ivory": "#FFFFF0", "lavender": "#E6E6FA",
        "crimson": "#DC143C", "turquoise": "#40E0D0", "skyblue": "#87CEEB",
        "darkred": "#8B0000", "darkgreen": "#006400", "darkblue": "#00008B",
        "darkorange": "#FF8C00", "darkviolet": "#9400D3", "hotpink": "#FF69B4",
        "hacker": "#00FF41", "matrix": "#00FF00", "ocean": "#0A1929",
        "midnight": "#191970", "sunset": "#FD5E53", "forest": "#228B22",
        "cyber": "#FF073A", "neon": "#39FF14", "steel": "#4682B4",
        "amber": "#FFBF00", "slate": "#708090",
    }
    
    def get_color_from_input(color_input):
        color_input = color_input.strip().lower()
        if color_input.startswith("#"):
            return color_input
        return COLOR_NAMES.get(color_input, color_input)
    
    # Header
    header = ctk.CTkFrame(win, fg_color="#12121a", corner_radius=0)
    header.pack(fill="x", pady=(0, 0))
    header.pack_propagate(False)
    header.configure(height=60)
    
    title_frame = ctk.CTkFrame(header, fg_color="transparent")
    title_frame.pack(side="left", padx=20, pady=12)
    
    ctk.CTkLabel(title_frame, text="✏️", font=("Segoe UI", 24)).pack(side="left", padx=(0, 10))
    title_vbox = ctk.CTkFrame(title_frame, fg_color="transparent")
    title_vbox.pack(side="left")
    ctk.CTkLabel(title_vbox, text="Theme Creator", font=("Segoe UI", 18, "bold"), text_color="#ffffff").pack(anchor="w")
    ctk.CTkLabel(title_vbox, text="Create your custom theme", font=("Segoe UI", 10), text_color="#888899").pack(anchor="w")
    
    # Main content - split into two sides
    main_content = ctk.CTkFrame(win, fg_color="#0a0a0f", corner_radius=0)
    main_content.pack(fill="both", expand=True)
    
    # Left side - Controls
    left_panel = ctk.CTkFrame(main_content, fg_color="#12121a", corner_radius=0)
    left_panel.pack(side="left", fill="y", padx=0, pady=0)
    left_panel.pack_propagate(False)
    left_panel.configure(width=320)
    
    ctk.CTkLabel(left_panel, text="Theme Settings", font=("Segoe UI", 14, "bold"), text_color="#ffffff").pack(pady=(20, 15), padx=20, anchor="w")
    
    # Theme name
    ctk.CTkLabel(left_panel, text="Theme Name", font=("Segoe UI", 11), text_color="#888899").pack(pady=(10, 5), padx=20, anchor="w")
    name_entry = ctk.CTkEntry(left_panel, width=280, placeholder_text="my_awesome_theme", font=("Segoe UI", 11))
    name_entry.pack(pady=(0, 15), padx=20)
    
    # Color inputs with examples
    ctk.CTkLabel(left_panel, text="Background (e.g., #101010 or black)", font=("Segoe UI", 11), text_color="#888899").pack(pady=(10, 5), padx=20, anchor="w")
    bg_entry = ctk.CTkEntry(left_panel, width=280, placeholder_text="#101010", font=("Consolas", 11))
    bg_entry.pack(pady=(0, 5), padx=20)
    bg_entry.insert(0, cfg.get("bg_color", "#101010"))
    
    ctk.CTkLabel(left_panel, text="Text Color (e.g., #E6E6E6 or white)", font=("Segoe UI", 11), text_color="#888899").pack(pady=(10, 5), padx=20, anchor="w")
    fg_entry = ctk.CTkEntry(left_panel, width=280, placeholder_text="#E6E6E6", font=("Consolas", 11))
    fg_entry.pack(pady=(0, 5), padx=20)
    fg_entry.insert(0, cfg.get("fg_color", "#E6E6E6"))
    
    ctk.CTkLabel(left_panel, text="Accent Color (e.g., #4A90E2 or blue)", font=("Segoe UI", 11), text_color="#888899").pack(pady=(10, 5), padx=20, anchor="w")
    accent_entry = ctk.CTkEntry(left_panel, width=280, placeholder_text="#4A90E2", font=("Consolas", 11))
    accent_entry.pack(pady=(0, 5), padx=20)
    accent_entry.insert(0, cfg.get("accent_color", "#4A90E2"))
    
    ctk.CTkLabel(left_panel, text="Entry Background (e.g., #181818)", font=("Segoe UI", 11), text_color="#888899").pack(pady=(10, 5), padx=20, anchor="w")
    entry_bg_entry = ctk.CTkEntry(left_panel, width=280, placeholder_text="#181818", font=("Consolas", 11))
    entry_bg_entry.pack(pady=(0, 5), padx=20)
    entry_bg_entry.insert(0, cfg.get("entry_bg", "#181818"))
    
    ctk.CTkLabel(left_panel, text="Entry Text (e.g., #FFFFFF or white)", font=("Segoe UI", 11), text_color="#888899").pack(pady=(10, 5), padx=20, anchor="w")
    entry_fg_entry = ctk.CTkEntry(left_panel, width=280, placeholder_text="#FFFFFF", font=("Consolas", 11))
    entry_fg_entry.pack(pady=(0, 5), padx=20)
    entry_fg_entry.insert(0, cfg.get("entry_fg", "#FFFFFF"))
    
    msg_label = ctk.CTkLabel(left_panel, text="", font=("Segoe UI", 11))
    msg_label.pack(pady=(15, 5))
    
    # Buttons
    btn_frame = ctk.CTkFrame(left_panel, fg_color="transparent")
    btn_frame.pack(pady=(10, 20), padx=20)
    
    def save_theme():
        name = name_entry.get().strip()
        if not name:
            msg_label.configure(text="Theme name required!", text_color="#F97373")
            return
        bg = get_color_from_input(bg_entry.get()) or cfg["bg_color"]
        fg = get_color_from_input(fg_entry.get()) or cfg["fg_color"]
        accent = get_color_from_input(accent_entry.get()) or cfg["accent_color"]
        entry_bg = get_color_from_input(entry_bg_entry.get()) or cfg["entry_bg"]
        entry_fg = get_color_from_input(entry_fg_entry.get()) or cfg["entry_fg"]
        if not os.path.exists("themes"):
            os.makedirs("themes")
        path = os.path.join("themes", f"{name}.json")
        with open(path, "w") as f:
            json.dump({"bg_color": bg, "fg_color": fg, "accent_color": accent, "entry_bg": entry_bg, "entry_fg": entry_fg}, f, indent=4)
        msg_label.configure(text=f"Theme '{name}' saved!", text_color="#4ADE80")
        notify(f"Theme '{name}' saved.", "success")
    
    def apply_preview():
        bg = get_color_from_input(bg_entry.get()) or cfg["bg_color"]
        fg = get_color_from_input(fg_entry.get()) or cfg["fg_color"]
        accent = get_color_from_input(accent_entry.get()) or cfg["accent_color"]
        entry_bg = get_color_from_input(entry_bg_entry.get()) or cfg["entry_bg"]
        entry_fg = get_color_from_input(entry_fg_entry.get()) or cfg["entry_fg"]
        
        preview_bg.configure(fg_color=bg)
        preview_output.configure(fg_color=bg, text_color=fg)
        preview_prompt.configure(text_color=accent)
        preview_entry.configure(fg_color=entry_bg, text_color=entry_fg)
        
        swatch_bg.configure(fg_color=bg)
        swatch_fg.configure(fg_color=fg)
        swatch_accent.configure(fg_color=accent)
    
    ctk.CTkButton(btn_frame, text="🔍 Preview", command=apply_preview, width=130, height=36, font=("Segoe UI", 11, "bold"), fg_color="#2a2a3e", hover_color="#3a3a4e", text_color="#ffffff", corner_radius=8).pack(side="left", padx=5)
    ctk.CTkButton(btn_frame, text="💾 Save Theme", command=save_theme, width=130, height=36, font=("Segoe UI", 11, "bold"), fg_color="#6366f1", hover_color="#818cf8", text_color="#ffffff", corner_radius=8).pack(side="left", padx=5)
    
    # Right side - Live Preview
    right_panel = ctk.CTkFrame(main_content, fg_color="#0a0a0f", corner_radius=0)
    right_panel.pack(side="left", fill="both", expand=True, padx=0, pady=0)
    
    ctk.CTkLabel(right_panel, text="Live Preview", font=("Segoe UI", 14, "bold"), text_color="#ffffff").pack(pady=(20, 10), padx=20, anchor="w")
    
    preview_bg = ctk.CTkFrame(right_panel, fg_color=cfg.get("bg_color", "#101010"), corner_radius=12, border_width=1, border_color="#1e1e2e")
    preview_bg.pack(fill="both", expand=True, padx=20, pady=10)
    
    preview_top = ctk.CTkFrame(preview_bg, fg_color="transparent")
    preview_top.pack(fill="x", padx=15, pady=(15, 0))
    
    swatch_frame = ctk.CTkFrame(preview_top, fg_color="transparent")
    swatch_frame.pack(side="left")
    
    swatch_bg = ctk.CTkFrame(swatch_frame, fg_color=cfg.get("bg_color", "#101010"), width=20, height=20, corner_radius=10)
    swatch_bg.pack(side="left", padx=2)
    swatch_fg = ctk.CTkFrame(swatch_frame, fg_color=cfg.get("fg_color", "#E6E6E6"), width=16, height=16, corner_radius=8)
    swatch_fg.pack(side="left", padx=2)
    swatch_accent = ctk.CTkFrame(swatch_frame, fg_color=cfg.get("accent_color", "#4A90E2"), width=12, height=12, corner_radius=6)
    swatch_accent.pack(side="left", padx=2)
    
    ctk.CTkLabel(preview_top, text="Magnesium v1.0.0", font=("Segoe UI", 10), text_color="#666677").pack(side="left", padx=10)
    
    preview_output = ctk.CTkTextbox(preview_bg, fg_color=cfg.get("bg_color", "#101010"), text_color=cfg.get("fg_color", "#E6E6E6"), border_width=0, corner_radius=0, state="normal")
    preview_output.pack(fill="both", expand=True, padx=15, pady=10)
    preview_output.insert("end", "Magnesium > help\n\nWelcome to Magnesium terminal!\nType 'help' to see all commands.\n\nMagnesium > cmd echo Hello World\n\nHello World\n\nMagnesium > ")
    preview_output.configure(state="disabled")
    
    preview_input_frame = ctk.CTkFrame(preview_bg, fg_color="transparent")
    preview_input_frame.pack(fill="x", padx=15, pady=(0, 15))
    
    preview_prompt = ctk.CTkLabel(preview_input_frame, text="Magnesium > ", text_color=cfg.get("accent_color", "#4A90E2"), font=("Consolas", 11))
    preview_prompt.pack(side="left")
    
    preview_entry = ctk.CTkEntry(preview_input_frame, fg_color=cfg.get("entry_bg", "#181818"), text_color=cfg.get("entry_fg", "#FFFFFF"), border_width=0, corner_radius=4)
    preview_entry.pack(side="left", fill="x", expand=True)
    preview_entry.insert(0, "type command...")
    
    # Footer
    footer = ctk.CTkFrame(win, fg_color="#12121a", corner_radius=0)
    footer.pack(fill="x", pady=(0, 0))
    footer.configure(height=50)
    
    footer_frame = ctk.CTkFrame(footer, fg_color="transparent")
    footer_frame.pack(expand=True, pady=8)
    
    ctk.CTkLabel(footer_frame, text="💡 Tip: Use color names like 'red', 'blue', 'green', 'gold' or hex codes like #FF0000", font=("Segoe UI", 10), text_color="#666677").pack()
    
    def fade_in(step=0):
        if not win.winfo_exists():
            return
        a = win.attributes("-alpha")
        if a < 0.97:
            win.attributes("-alpha", a + 0.05)
            win.after(16, lambda: fade_in(step + 1))
    
    fade_in()
    
    def on_color_change(event=None):
        apply_preview()
    
    bg_entry.bind("<KeyRelease>", on_color_change)
    fg_entry.bind("<KeyRelease>", on_color_change)
    accent_entry.bind("<KeyRelease>", on_color_change)
    entry_bg_entry.bind("<KeyRelease>", on_color_change)
    entry_fg_entry.bind("<KeyRelease>", on_color_change)

def open_store():
    cfg = load_main_config()
    win = ctk.CTkToplevel(app)
    win.title("Magnesium Theme Store")
    win.geometry("900x620")
    win.resizable(False, False)
    win.attributes("-alpha", 0.0)
    win.configure(fg_color="#0a0a0f")
    
    header = ctk.CTkFrame(win, fg_color="#12121a", corner_radius=0)
    header.pack(fill="x", pady=(0, 0))
    header.pack_propagate(False)
    header.configure(height=80)
    
    title_frame = ctk.CTkFrame(header, fg_color="transparent")
    title_frame.pack(side="left", padx=20, pady=15)
    
    ctk.CTkLabel(title_frame, text="🎨", font=("Segoe UI", 28)).pack(side="left", padx=(0, 10))
    title_vbox = ctk.CTkFrame(title_frame, fg_color="transparent")
    title_vbox.pack(side="left")
    ctk.CTkLabel(title_vbox, text="Magnesium Store", font=("Segoe UI", 20, "bold"), text_color="#ffffff").pack(anchor="w")
    ctk.CTkLabel(title_vbox, text="Browse and install beautiful themes", font=("Segoe UI", 11), text_color="#888899").pack(anchor="w")
    
    search_frame = ctk.CTkFrame(header, fg_color="transparent")
    search_frame.pack(side="right", padx=20, pady=20)
    
    search_entry = ctk.CTkEntry(search_frame, width=220, height=36, placeholder_text="Search themes...", font=("Segoe UI", 12))
    search_entry.pack()
    search_entry.configure(corner_radius=18)
    
    stats_bar = ctk.CTkFrame(win, fg_color="#0d0d14", corner_radius=0)
    stats_bar.pack(fill="x", padx=0, pady=0)
    stats_bar.configure(height=40)
    
    files = list_theme_files()
    stats_label = ctk.CTkLabel(stats_bar, text=f"📦 {len(files)} themes available", font=("Segoe UI", 11), text_color="#666677")
    stats_label.pack(side="left", padx=20, pady=8)
    
    body = ctk.CTkScrollableFrame(win, fg_color="#0a0a0f", corner_radius=0, scrollbar_button_color="#1a1a2e", scrollbar_button_hover_color="#2a2a3e")
    body.pack(fill="both", expand=True, padx=15, pady=15)
    
    theme_widgets = []
    
    def load_themes(filter_text=""):
        for w in theme_widgets: w.destroy()
        theme_widgets.clear()
        files = list_theme_files()
        
        if not files:
            empty_frame = ctk.CTkFrame(body, fg_color="transparent")
            empty_frame.pack(pady=60)
            ctk.CTkLabel(empty_frame, text="📭", font=("Segoe UI", 48)).pack()
            ctk.CTkLabel(empty_frame, text="No themes found", font=("Segoe UI", 16, "bold"), text_color="#444455").pack(pady=(10, 5))
            ctk.CTkLabel(empty_frame, text="Create your own theme using the Theme Creator!", font=("Segoe UI", 12), text_color="#555566").pack()
            theme_widgets.append(empty_frame)
            return
        
        ft = filter_text.lower().strip()
        
        for i, f in enumerate(files):
            name = os.path.splitext(f)[0]
            if ft and ft not in name.lower():
                continue
            
            theme_path = os.path.join("themes", f)
            try:
                with open(theme_path, "r") as tf:
                    theme_data = json.load(tf)
                    bg = theme_data.get("bg_color", "#1a1a2e")
                    fg = theme_data.get("fg_color", "#ffffff")
                    accent = theme_data.get("accent_color", "#4A90E2")
            except:
                bg, fg, accent = "#1a1a2e", "#ffffff", "#4A90E2"
            
            card = ctk.CTkFrame(body, fg_color="#12121a", corner_radius=16, border_width=1, border_color="#1e1e2e")
            card.pack(fill="x", padx=5, pady=8, ipady=5)
            theme_widgets.append(card)
            
            inner = ctk.CTkFrame(card, fg_color="transparent")
            inner.pack(fill="x", padx=15, pady=12)
            
            swatch_frame = ctk.CTkFrame(inner, fg_color="transparent")
            swatch_frame.pack(side="left", padx=(0, 15))
            
            for color, size in [(bg, 28), (fg, 20), (accent, 14)]:
                swatch = ctk.CTkFrame(swatch_frame, fg_color=color, width=size, height=size, corner_radius=size//2)
                swatch.pack(side="left", padx=2)
            
            info_frame = ctk.CTkFrame(inner, fg_color="transparent")
            info_frame.pack(side="left", fill="x", expand=True)
            
            ctk.CTkLabel(info_frame, text=name.replace("_", " ").title(), font=("Segoe UI", 14, "bold"), text_color="#ffffff").pack(anchor="w")
            
            color_codes = f"#{bg[1:4]} · #{fg[1:4]} · #{accent[1:4]}"
            ctk.CTkLabel(info_frame, text=color_codes, font=("Consolas", 9), text_color="#555566").pack(anchor="w", pady=(2, 0))
            
            current_idx, current_theme_name = i + 1, name
            def make_install(idx=current_idx, theme_name=current_theme_name):
                def _do():
                    msg, theme = install_theme(idx)
                    if theme:
                        apply_theme(theme)
                        notify(f"Installed '{theme_name}' theme!", "success")
                return _do
            
            btn = ctk.CTkButton(inner, text="Install", width=90, height=32, font=("Segoe UI", 11, "bold"), fg_color="#2a2a3e", hover_color="#3a3a4e", text_color="#ffffff", corner_radius=8, command=make_install())
            btn.pack(side="right", padx=5)
            
            if cfg.get("bg_color") == bg and cfg.get("fg_color") == fg:
                ctk.CTkLabel(inner, text="✓ Active", font=("Segoe UI", 10, "bold"), text_color="#4ADE80").pack(side="right", padx=10)
    
    def on_search_change(event=None):
        load_themes(search_entry.get())
    
    search_entry.bind("<KeyRelease>", on_search_change)
    load_themes()
    
    footer = ctk.CTkFrame(win, fg_color="#12121a", corner_radius=0)
    footer.pack(fill="x", pady=(0, 0))
    footer.configure(height=50)
    
    footer_frame = ctk.CTkFrame(footer, fg_color="transparent")
    footer_frame.pack(expand=True, pady=8)
    
    ctk.CTkButton(footer_frame, text="+ Create New Theme", command=lambda: [win.destroy(), theme_creator()], width=160, height=32, font=("Segoe UI", 11, "bold"), fg_color="#6366f1", hover_color="#818cf8", text_color="#ffffff", corner_radius=8).pack(side="left", padx=5)
    ctk.CTkButton(footer_frame, text="↻ Refresh Store", command=lambda: load_themes(search_entry.get()), width=140, height=32, font=("Segoe UI", 11), fg_color="#1e1e2e", hover_color="#2e2e3e", text_color="#888899", corner_radius=8).pack(side="left", padx=5)
    
    def fade_in(step=0):
        if not win.winfo_exists():
            return
        a = win.attributes("-alpha")
        if a < 0.97:
            win.attributes("-alpha", a + 0.05)
            win.after(16, lambda: fade_in(step + 1))
    fade_in()

def show_help_window():
    win = ctk.CTkToplevel(app)
    win.title("Magnesium Help")
    win.geometry("500x450")
    win.resizable(False, False)
    win.attributes("-alpha", 0.0)
    win.configure(fg_color="#000000")
    
    main_frame = ctk.CTkFrame(win, fg_color="transparent", corner_radius=12, border_width=1, border_color="#00FF41")
    main_frame.pack(fill="both", expand=True, padx=2, pady=2)
    header = ctk.CTkFrame(main_frame, fg_color="transparent")
    header.pack(fill="x", padx=20, pady=(20, 10))
    ctk.CTkLabel(header, text="Magnesium Help", font=("Consolas", 20, "bold"), text_color="#00FF41").pack(side="left")
    content = ctk.CTkScrollableFrame(main_frame, fg_color="transparent")
    content.pack(fill="both", expand=True, padx=20, pady=10)
    
    def add_help_section(parent, title_text, commands):
        ctk.CTkLabel(parent, text=title_text, font=("Consolas", 12, "bold"), text_color="#00FF41").pack(anchor="w", pady=(15, 8))
        for cmd, desc in commands:
            cmd_frame = ctk.CTkFrame(parent, fg_color="#0D0D0D", corner_radius=4)
            cmd_frame.pack(fill="x", pady=3, ipady=4)
            ctk.CTkLabel(cmd_frame, text=cmd, font=("Consolas", 10, "bold"), text_color="#00FF41", anchor="w").pack(side="left", padx=(10, 0), fill="x", expand=True)
            ctk.CTkLabel(cmd_frame, text=desc, font=("Consolas", 9), text_color="#00CC33", anchor="e").pack(side="right", padx=(0, 10))
    
    add_help_section(content, "SYSTEM", [("help", "Show help"), ("exit", "Exit")])
    add_help_section(content, "THEMES", [("view --fxthemes", "List themes"), ("install --fxthemes <id>", "Install theme"), ("view --store", "Open Store")])
    add_help_section(content, "ALIASES", [("alias list", "List aliases"), ("alias add <name> <cmd>", "Add alias")])
    add_help_section(content, "SHELL", [("cmd <command>", "Run CMD"), ("ps <command>", "Run PowerShell"), ("linux <command>", "Run Linux (WSL)")])
    
    def fade_in(step=0):
        if not win.winfo_exists(): return
        win.attributes("-alpha", 0.95 if step/10 > 0.95 else step/10)
        if step <= 9: win.after(20, lambda: fade_in(step + 1))
    fade_in()

def process_command(cmd):
    cfg = load_main_config()
    aliases = cfg.get("aliases", {})
    parts = cmd.split()
    if parts and parts[0] in aliases:
        cmd = aliases[parts[0]] + (" " + " ".join(parts[1:]) if len(parts) > 1 else "")
    
    if cmd == "help": show_help_window(); return
    if cmd == "exit": confirm_exit(); return ""
    if cmd.startswith("view --fxthemes"):
        files = list_theme_files()
        return "Themes:\n" + "\n".join(f"{i}. {os.path.splitext(f)[0]}" for i, f in enumerate(files, start=1)) if files else "No themes found."
    if cmd.startswith("install --fxthemes"):
        try:
            idx = int(cmd.split()[2])
            msg, theme = install_theme(idx)
            if theme: apply_theme(theme); notify(msg, "success")
            return msg
        except: return "Invalid index."
    if cmd == "view --store": open_store(); return
    if cmd == "alias list": als = cfg.get("aliases", {}); return "Aliases:\n" + "\n".join(f"  {k} -> {v}" for k, v in als.items()) if als else "No aliases."
    if cmd.startswith("alias add "):
        parts = cmd.split(maxsplit=3)
        if len(parts) < 4: return "Usage: alias add <name> <command>"
        cfg["aliases"][parts[2]] = parts[3]
        save_main_config(cfg)
        return f"Alias '{parts[2]}' added."
    if cmd.startswith("cmd "): return run_cmd(cmd[4:])
    if cmd.startswith("ps "): return run_cmd(f"powershell {cmd[3:]}")
    if cmd.startswith("linux "): return run_cmd(f"wsl {cmd[6:]}")
    return "Unknown command. Type 'help'."

def show_quick_tutorial():
    cfg = load_main_config()
    if cfg.get("tutorial_shown", False):
        return
    
    cfg["tutorial_shown"] = True
    save_main_config(cfg)
    
    win = ctk.CTkToplevel(app)
    win.title("Quick Tutorial")
    win.geometry("550x400")
    win.resizable(False, False)
    win.attributes("-alpha", 0.95)
    win.configure(fg_color="#050505")
    
    frame = ctk.CTkFrame(win, fg_color="#111827", corner_radius=12)
    frame.pack(fill="both", expand=True, padx=10, pady=10)
    
    ctk.CTkLabel(frame, text="Welcome to Magnesium!", font=("Segoe UI", 20, "bold")).pack(pady=(15, 10))
    
    tutorial_steps = [
        ("Getting Started", "Type 'help' for all commands\nUse 'view --store' to browse themes\nUse 'alias add <name> <cmd>' for shortcuts"),
        ("Running Commands", "'cmd <command>' - Run CMD\n'ps <command>' - Run PowerShell\n'linux <command>' - Run Linux (WSL)"),
        ("Tips", "Click sidebar icons for quick access\nCreate custom aliases for frequent commands\nCustomize themes in the store"),
    ]
    
    for title, content in tutorial_steps:
        ctk.CTkLabel(frame, text=title, font=("Segoe UI", 14, "bold")).pack(anchor="w", padx=20, pady=(10, 5))
        ctk.CTkLabel(frame, text=content, font=("Segoe UI", 11), text_color="#94A3B8", justify="left").pack(anchor="w", padx=25, pady=(0, 5))
    
    ctk.CTkButton(frame, text="Got it!", command=win.destroy, width=120).pack(pady=(15, 10))

def show_changelog_if_needed():
    cfg = load_main_config()
    version = cfg.get("version", "v1.0.0")
    last = cfg.get("last_shown_version", "")
    if last == version: return
    text = open("changelog.txt", "r", encoding="utf-8", errors="ignore").read() if os.path.exists("changelog.txt") else ""
    if not text.strip():
        cfg["last_shown_version"] = version
        save_main_config(cfg)
        return
    win = ctk.CTkToplevel(app)
    win.title("Changelog")
    win.geometry("600x400")
    win.resizable(False, False)
    win.attributes("-alpha", 0.95)
    frame = ctk.CTkFrame(win, fg_color="#020617", corner_radius=12)
    frame.pack(fill="both", expand=True, padx=10, pady=10)
    ctk.CTkLabel(frame, text=f"Changelog – {version}", font=("Segoe UI", 18, "bold")).pack(pady=(10, 5))
    box = ctk.CTkTextbox(frame, fg_color="#020617", text_color="#E5E7EB")
    box.pack(fill="both", expand=True, padx=10, pady=10)
    box.insert("end", text)
    box.configure(state="disabled")
    def close_and_save():
        cfg2 = load_main_config()
        cfg2["last_shown_version"] = version
        save_main_config(cfg2)
        win.destroy()
    ctk.CTkButton(frame, text="Close", command=close_and_save, width=100).pack(pady=(0, 10))

def build_terminal():
    global output_box, entry, prompt_label, top_bar, entry_frame
    for w in app.winfo_children(): w.destroy()
    config = load_main_config()
    app.configure(fg_color=config["bg_color"])
    app.attributes("-alpha", 0.0)
    create_sidebar_icons()
    
    top_bar = ctk.CTkFrame(app, fg_color=config["bg_color"])
    top_bar.pack(fill="x", padx=10, pady=(8, 0))
    ctk.CTkLabel(top_bar, text=f"Magnesium {config['version']}", text_color=config["fg_color"], font=("Segoe UI", 12)).pack(side="left")
    
    # Check license key and show appropriate notification
    license_key = config.get("license_key", "")
    if license_key.upper() == "FREE":
        notify("Free build detected. Upgrade to PRO for more features!", "warning", 4000)
    elif not GITHUB_REPO_URL:
        notify("Beta build detected.", "warning", 3200)
    else:
        notify("Welcome back!", "System", 3200)
    
    output_box = ctk.CTkTextbox(app, fg_color=config["bg_color"], text_color=config["fg_color"], corner_radius=0, border_width=0, state="disabled")
    output_box.pack(fill="both", expand=True, padx=10, pady=10)
    entry_frame = ctk.CTkFrame(app, fg_color=config["bg_color"])
    entry_frame.pack(fill="x", padx=10, pady=(0, 10))
    prompt_label = ctk.CTkLabel(entry_frame, text=PROMPT, text_color=config["accent_color"], font=("Consolas", 13))
    prompt_label.pack(side="left")
    entry = ctk.CTkEntry(entry_frame, fg_color=config["entry_bg"], text_color=config["entry_fg"], border_width=0, corner_radius=6)
    entry.pack(side="left", fill="x", expand=True)
    
    def on_enter(event=None):
        cmd = entry.get()
        entry.delete(0, "end")
        if cmd.strip() == "": return
        result = process_command(cmd)
        if result:
            output_box.configure(state="normal")
            output_box.insert("end", PROMPT + cmd + "\n")
            output_box.insert("end", result + "\n\n")
            output_box.see("end")
            output_box.configure(state="disabled")
    
    entry.bind("<Return>", on_enter)
    
    def fade_in():
        if not app.winfo_exists(): return
        alpha = app.attributes("-alpha")
        if alpha < 0.9: app.attributes("-alpha", alpha + 0.05); app.after(16, fade_in)
        else: entry.focus_set()
    fade_in()
    show_quick_tutorial()
    show_changelog_if_needed()

# ================= LICENSE KEY SYSTEM =================
LICENSE_KEYS = [
    {
        "key": "FREE",
        "expiry": "2099-12-31",
        "used": True,
        "ip": None,
        "activated_at": "Free access for everyone"
    },
    {
        "key": "MAGNUM-2024-KEY-001",
        "expiry": "2025-12-31",
        "used": False,
        "ip": None,
        "activated_at": None
    },
    {
        "key": "MAGNUM-2024-KEY-002",
        "expiry": "2025-12-31",
        "used": False,
        "ip": None,
        "activated_at": None
    },
    {
        "key": "MAGNUM-2024-KEY-003",
        "expiry": "2025-12-31",
        "used": False,
        "ip": None,
        "activated_at": None
    },
    {
        "key": "DEV-KEY-FOR-TESTING",
        "expiry": "2026-12-31",
        "used": True,
        "ip": "10.252.12.182",
        "activated_at": "2026-02-22 14:52:57"
    },
    {
        "key": "DEV-KEY-FOR-TESTING-2",
        "expiry": "2028-12-12",
        "used": False,
        "ip": None,
        "activated_at": None
    }

]

def get_local_ip():
    import socket
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

def load_license_keys():
    return LICENSE_KEYS

def save_license_keys(keys):
    global LICENSE_KEYS
    LICENSE_KEYS = keys

def activate_license_key(key):
    import datetime
    keys = load_license_keys()
    key_found, key_index = None, -1
    for i, k in enumerate(keys):
        if k.get("key", "").upper() == key.upper():
            key_found, key_index = k, i
            break
    if not key_found: return {"success": False, "message": "Invalid license key"}, 404
    if key_found.get("used", False):
        stored_ip = key_found.get("ip")
        current_ip = get_local_ip()
        # If ip is None, it's a free key with no IP restriction
        if stored_ip is None:
            return {"success": True, "message": "Free access granted!", "key": key, "activated_at": key_found.get("activated_at"), "ip_address": "N/A (Free key)", "reactivated": True}, 200
        if stored_ip == current_ip:
            return {"success": True, "message": "Key already activated for this machine", "key": key, "activated_at": key_found.get("activated_at"), "ip_address": stored_ip, "reactivated": True}, 200
        else:
            return {"success": False, "message": f"Key already used. Can only be used from IP: {stored_ip}", "original_ip": stored_ip}, 403
    expiry = key_found.get("expiry", "")
    if expiry:
        try:
            expiry_date = datetime.datetime.strptime(expiry, "%Y-%m-%d").date()
            if datetime.date.today() > expiry_date:
                return {"success": False, "message": f"License key expired on {expiry}"}, 403
        except: pass
    current_ip = get_local_ip()
    activation_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    keys[key_index]["used"] = True
    keys[key_index]["ip"] = current_ip
    keys[key_index]["activated_at"] = activation_date
    save_license_keys(keys)
    return {"success": True, "message": "License key activated successfully!", "key": key, "activated_at": activation_date, "ip_address": current_ip}, 200

def verify_license_key(key):
    keys = load_license_keys()
    key_found = None
    for k in keys:
        if k.get("key", "").upper() == key.upper():
            key_found = k
            break
    if not key_found: return {"valid": False, "message": "Invalid license key"}, 404
    if not key_found.get("used", False): return {"valid": False, "message": "License key not activated yet"}, 403
    stored_ip = key_found.get("ip")
    current_ip = get_local_ip()
    if stored_ip != current_ip: return {"valid": False, "message": f"Access denied. Key bound to IP: {stored_ip}"}, 403
    return {"valid": True, "message": "License key is valid", "key": key, "ip_address": stored_ip, "activated_at": key_found.get("activated_at")}, 200

def auth_screen():
    for w in app.winfo_children(): w.destroy()
    cfg = load_main_config()
    app.configure(fg_color="#050505")
    app.attributes("-alpha", 0.9)
    
    frame = ctk.CTkFrame(app, fg_color="#111827", corner_radius=12)
    frame.place(relx=0.5, rely=0.5, anchor="center")
    
    ctk.CTkLabel(frame, text="License Activation", font=("Segoe UI", 22, "bold")).pack(pady=(25, 5), padx=30)
    ctk.CTkLabel(frame, text="Enter your license key to activate Magnesium", font=("Segoe UI", 12), text_color="#94A3B8").pack(pady=(0, 20), padx=30)
    
    key_entry = ctk.CTkEntry(frame, width=300, placeholder_text="XXXX-XXXX-XXXX-XXXX", font=("Consolas", 14))
    key_entry.pack(pady=10, padx=30)
    
    msg_label = ctk.CTkLabel(frame, text="", font=("Segoe UI", 11))
    msg_label.pack(pady=(5, 10))
    
    loading_label = ctk.CTkLabel(frame, text="", font=("Segoe UI", 11))
    loading_label.pack(pady=5)
    
    def do_login():
        key = key_entry.get().strip().upper()
        if not key:
            msg_label.configure(text="Please enter a license key.", text_color="#F97373")
            return
        loading_label.configure(text="Verifying license...", text_color="#60A5FA")
        frame.update()
        result, status_code = activate_license_key(key)
        if result.get("success"):
            if result.get("reactivated"):
                msg_label.configure(text=f"Welcome back! Key activated: {result.get('activated_at', '')}", text_color="#4ADE80")
            else:
                msg_label.configure(text="License activated successfully!", text_color="#4ADE80")
            cfg["license_key"] = key
            save_main_config(cfg)
            frame.after(800, build_terminal)
        else:
            error_msg = result.get("message", "Unknown error")
            msg_label.configure(text=error_msg, text_color="#F97373")
            if "already used" in error_msg.lower():
                loading_label.configure(text="Checking existing activation...", text_color="#60A5FA")
                frame.update()
                verify_result, verify_status = verify_license_key(key)
                if verify_result.get("valid"):
                    msg_label.configure(text="Access granted from registered IP!", text_color="#4ADE80")
                    cfg["license_key"] = key
                    save_main_config(cfg)
                    frame.after(800, build_terminal)
                else:
                    msg_label.configure(text=verify_result.get("message", "Verification failed"), text_color="#F97373")
        loading_label.configure(text="")
    
    ctk.CTkButton(frame, text="Activate / Login", command=do_login, width=180, height=40, font=("Segoe UI", 12, "bold")).pack(pady=(10, 15))
    ctk.CTkLabel(frame, text="Need support? Join our discord server!", font=("Consolas", 9), text_color="#64748B").pack(pady=(0, 15))
    
    key_entry.bind("<Return>", lambda e: do_login())
    key_entry.focus()

def loading_screen():
    for w in app.winfo_children(): w.destroy()
    app.configure(fg_color="#050505")
    app.attributes("-alpha", 0.0)
    canvas = ctk.CTkCanvas(app, width=800, height=500, bg="#050505", highlightthickness=0)
    canvas.pack(fill="both", expand=True)
    bar = ctk.CTkProgressBar(app, width=400, progress_color="#4A90E2")
    bar.place(relx=0.5, rely=0.85, anchor="center")
    bar.set(0)
    state = {"t": 0.0, "p": 0.0}
    
    def fade_in_window():
        if not app.winfo_exists(): return
        alpha = app.attributes("-alpha")
        if alpha < 0.9: app.attributes("-alpha", alpha + 0.05); app.after(16, fade_in_window)
        else: app.attributes("-alpha", 0.9)
    fade_in_window()
    
    def anim():
        if not app.winfo_exists(): return
        canvas.delete("all")
        t = state["t"]
        cx, cy = 400, 230
        base = 55
        open_factor = min(t / 60, 1.0)
        angle = t * 0.08
        cos_a, sin_a = math.cos(angle), math.sin(angle)
        def rot(px, py): return cx + px * cos_a - py * sin_a, cy + px * sin_a + py * cos_a
        s = base
        core = []
        for px, py in [(-s, -s), (s, -s), (s, s), (-s, s)]: core.extend(rot(px, py))
        top_offset = -s * (1 + 0.9 * open_factor)
        bottom_offset = s * (1 + 0.9 * open_factor)
        left_offset = -s * (1 + 0.9 * open_factor)
        right_offset = s * (1 + 0.9 * open_factor)
        top = []
        for px, py in [(-s, -s), (s, -s), (s, -s + 18), (-s, -s + 18)]: x, y = rot(px, py + top_offset + s); top.extend((x, y))
        bottom = []
        for px, py in [(-s, s - 18), (s, s - 18), (s, s), (-s, s)]: x, y = rot(px, py + bottom_offset - s); bottom.extend((x, y))
        left = []
        for px, py in [(-s, -s), (-s + 18, -s), (-s + 18, s), (-s, s)]: x, y = rot(px + left_offset + s, py); left.extend((x, y))
        right = []
        for px, py in [(s - 18, -s), (s, -s), (s, s), (s - 18, s)]: x, y = rot(px + right_offset - s, py); right.extend((x, y))
        canvas.create_polygon(core, fill="#E5E7EB", outline="#9CA3AF")
        canvas.create_polygon(top, fill="#111827", outline="#1F2937")
        canvas.create_polygon(bottom, fill="#020617", outline="#020617")
        canvas.create_polygon(left, fill="#0F172A", outline="#111827")
        canvas.create_polygon(right, fill="#1F2937", outline="#111827")
        canvas.create_text(400, 90, text="Loading Magnesium...", fill="#E5E7EB", font=("Segoe UI", 20, "bold"))
        state["t"] += 1
        state["p"] += 0.015
        if state["p"] > 1: state["p"] = 1
        bar.set(state["p"])
        if state["p"] >= 1: auth_screen(); return
        app.after(16, anim)
    anim()

def main():
    global app
    ctk.set_appearance_mode("dark")
    app = ctk.CTk()
    cfg = load_main_config()
    app.title(f"Have a nice day, Junior :D")
    app.geometry("800x500")
    app.resizable(False, False)
    app.attributes("-alpha", 0.0)
    loading_screen()
    app.mainloop()

if __name__ == "__main__":
    main()
