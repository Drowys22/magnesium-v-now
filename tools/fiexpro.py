import customtkinter as ctk
import os

ctk.set_appearance_mode("dark")

class FileExplorerPro(ctk.CTkToplevel):
    def __init__(self, parent, start_path=None):
        super().__init__(parent)
        self.title("Magnesium File Explorer Pro")
        self.geometry("900x560")
        self.resizable(False, False)
        self.configure(fg_color="#020617")
        self.current_path = os.path.abspath(start_path or os.getcwd())
        self.build_ui()
        self.load_directory(self.current_path)

    def build_ui(self):
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(1, weight=1)
        header = ctk.CTkFrame(self, fg_color="#020617")
        header.grid(row=0, column=0, columnspan=2, sticky="new", padx=10, pady=(10, 4))
        title = ctk.CTkLabel(header, text="File Explorer Pro", font=("Segoe UI Semibold", 20), text_color="#E5E7EB")
        title.pack(side="left", padx=(4, 10))
        self.path_entry = ctk.CTkEntry(header)
        self.path_entry.pack(side="left", fill="x", expand=True, padx=(0, 6))
        self.path_entry.insert(0, self.current_path)
        go_btn = ctk.CTkButton(header, text="Go", width=70, command=self.go_to_path)
        go_btn.pack(side="left", padx=(0, 4))
        up_btn = ctk.CTkButton(header, text="Up", width=70, command=self.go_up)
        up_btn.pack(side="left")
        sidebar = ctk.CTkFrame(self, fg_color="#020617", corner_radius=0, width=220)
        sidebar.grid(row=1, column=0, sticky="nsw", padx=(10, 4), pady=(0, 10))
        sidebar.grid_propagate(False)
        sidebar.grid_rowconfigure(1, weight=1)
        sidebar_title = ctk.CTkLabel(sidebar, text="Folders", font=("Segoe UI Semibold", 14), text_color="#E5E7EB")
        sidebar_title.grid(row=0, column=0, sticky="w", padx=8, pady=(8, 4))
        self.dir_list = ctk.CTkScrollableFrame(sidebar, fg_color="#050816", corner_radius=10)
        self.dir_list.grid(row=1, column=0, sticky="nsew", padx=4, pady=(0, 4))
        self.dir_list.grid_columnconfigure(0, weight=1)
        main = ctk.CTkFrame(self, fg_color="#020617", corner_radius=0)
        main.grid(row=1, column=1, sticky="nsew", padx=(4, 10), pady=(0, 10))
        main.grid_rowconfigure(1, weight=1)
        main.grid_columnconfigure(0, weight=1)
        files_header = ctk.CTkFrame(main, fg_color="#020617")
        files_header.grid(row=0, column=0, sticky="new")
        files_title = ctk.CTkLabel(files_header, text="Files", font=("Segoe UI Semibold", 14), text_color="#E5E7EB")
        files_title.pack(side="left", padx=8, pady=(8, 4))
        self.files_frame = ctk.CTkScrollableFrame(main, fg_color="#050816", corner_radius=10)
        self.files_frame.grid(row=1, column=0, sticky="nsew", padx=0, pady=(0, 4))
        self.files_frame.grid_columnconfigure(0, weight=1)
        preview_frame = ctk.CTkFrame(main, fg_color="#050816", corner_radius=10)
        preview_frame.grid(row=2, column=0, sticky="nsew", padx=0, pady=(4, 0))
        preview_frame.grid_rowconfigure(1, weight=1)
        preview_frame.grid_columnconfigure(0, weight=1)
        preview_title = ctk.CTkLabel(preview_frame, text="Preview", font=("Segoe UI Semibold", 14), text_color="#E5E7EB")
        preview_title.grid(row=0, column=0, sticky="w", padx=8, pady=(8, 2))
        self.preview_box = ctk.CTkTextbox(preview_frame, fg_color="#020617", text_color="#E5E7EB", corner_radius=8)
        self.preview_box.grid(row=1, column=0, sticky="nsew", padx=8, pady=(0, 8))

    def clear_dirs(self):
        for w in self.dir_list.winfo_children():
            w.destroy()

    def clear_files(self):
        for w in self.files_frame.winfo_children():
            w.destroy()

    def load_directory(self, path):
        try:
            entries = os.listdir(path)
        except:
            return
        self.current_path = os.path.abspath(path)
        self.path_entry.delete(0, "end")
        self.path_entry.insert(0, self.current_path)
        dirs = []
        files = []
        for e in entries:
            full = os.path.join(self.current_path, e)
            if os.path.isdir(full):
                dirs.append(e)
            else:
                files.append(e)
        dirs.sort()
        files.sort()
        self.clear_dirs()
        for d in dirs:
            btn = ctk.CTkButton(
                self.dir_list,
                text=d,
                fg_color="transparent",
                hover_color="#0B1120",
                anchor="w",
                command=lambda name=d: self.open_dir(name)
            )
            btn.pack(fill="x", padx=4, pady=1)
        self.clear_files()
        for f in files:
            btn = ctk.CTkButton(
                self.files_frame,
                text=f,
                fg_color="transparent",
                hover_color="#0B1120",
                anchor="w",
                command=lambda name=f: self.open_file(name)
            )
            btn.pack(fill="x", padx=4, pady=1)
        self.preview_box.configure(state="normal")
        self.preview_box.delete("1.0", "end")
        self.preview_box.insert("end", "Select a file to preview.")
        self.preview_box.configure(state="disabled")

    def open_dir(self, name):
        new_path = os.path.join(self.current_path, name)
        if os.path.isdir(new_path):
            self.load_directory(new_path)

    def open_file(self, name):
        full = os.path.join(self.current_path, name)
        self.preview_box.configure(state="normal")
        self.preview_box.delete("1.0", "end")
        if not os.path.isfile(full):
            self.preview_box.insert("end", "Not a file.")
            self.preview_box.configure(state="disabled")
            return
        try:
            with open(full, "r", encoding="utf-8", errors="replace") as f:
                data = f.read()
            if len(data) > 20000:
                data = data[:20000] + "\n\n[Truncated]"
            self.preview_box.insert("end", data)
        except:
            self.preview_box.insert("end", "Unable to read file.")
        self.preview_box.configure(state="disabled")

    def go_to_path(self):
        path = self.path_entry.get().strip()
        if not path:
            return
        if os.path.isdir(path):
            self.load_directory(path)

    def go_up(self):
        parent = os.path.dirname(self.current_path)
        if parent and os.path.isdir(parent):
            self.load_directory(parent)

if __name__ == "__main__":
    app = FileExplorerPro()
    app.mainloop()
