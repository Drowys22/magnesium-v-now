import customtkinter as ctk
import subprocess
import csv
import io
import platform

ctk.set_appearance_mode("dark")

class ProcessExplorer(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Magnesium Process Explorer")
        self.geometry("800x500")
        self.resizable(False, False)
        self.configure(fg_color="#020617")
        self.build_ui()
        self.refresh_processes()

    def build_ui(self):
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        header = ctk.CTkFrame(self, fg_color="#020617")
        header.grid(row=0, column=0, sticky="new", padx=10, pady=(10, 4))
        title = ctk.CTkLabel(header, text="Process Explorer", font=("Segoe UI Semibold", 20), text_color="#E5E7EB")
        title.pack(side="left", padx=(4, 10))
        self.info_label = ctk.CTkLabel(header, text="", font=("Segoe UI", 11), text_color="#9CA3AF")
        self.info_label.pack(side="left")
        refresh_btn = ctk.CTkButton(header, text="Refresh", width=90, command=self.refresh_processes)
        refresh_btn.pack(side="right", padx=4)
        body = ctk.CTkFrame(self, fg_color="#020617")
        body.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
        body.grid_rowconfigure(0, weight=1)
        body.grid_columnconfigure(0, weight=1)
        self.table = ctk.CTkTextbox(body, fg_color="#050816", text_color="#E5E7EB", corner_radius=10)
        self.table.grid(row=0, column=0, sticky="nsew")
        self.table.configure(state="disabled", font=("Consolas", 11))

    def refresh_processes(self):
        rows = self.get_process_list()
        self.table.configure(state="normal")
        self.table.delete("1.0", "end")
        header = f"{'PID':>8}  {'Name':<32}  {'Memory':>10}\n"
        self.table.insert("end", header)
        self.table.insert("end", "-" * 60 + "\n")
        for pid, name, mem in rows:
            line = f"{pid:>8}  {name:<32.32}  {mem:>10}\n"
            self.table.insert("end", line)
        self.table.configure(state="disabled")
        self.info_label.configure(text=f"{len(rows)} processes")

    def get_process_list(self):
        system = platform.system().lower()
        if "windows" in system:
            return self.get_process_list_windows()
        else:
            return self.get_process_list_unix()

    def get_process_list_windows(self):
        try:
            result = subprocess.run(
                ["tasklist", "/fo", "csv", "/nh"],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="ignore"
            )
            data = result.stdout
            f = io.StringIO(data)
            reader = csv.reader(f)
            rows = []
            for row in reader:
                if len(row) < 5:
                    continue
                name = row[0].strip('"')
                pid = row[1].strip('"')
                mem = row[4].strip('"').replace(" K", "").replace(",", "")
                try:
                    pid_int = int(pid)
                except:
                    continue
                try:
                    mem_int = int(mem)
                    mem_str = f"{mem_int // 1024} MB"
                except:
                    mem_str = mem
                rows.append((pid_int, name, mem_str))
            rows.sort(key=lambda x: x[0])
            return rows
        except:
            return []

    def get_process_list_unix(self):
        try:
            result = subprocess.run(
                ["ps", "-eo", "pid,comm,rss"],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="ignore"
            )
            lines = result.stdout.splitlines()[1:]
            rows = []
            for line in lines:
                parts = line.split(None, 2)
                if len(parts) < 3:
                    continue
                pid, name, rss = parts
                try:
                    pid_int = int(pid)
                except:
                    continue
                try:
                    rss_int = int(rss)
                    mem_str = f"{rss_int // 1024} MB"
                except:
                    mem_str = rss
                rows.append((pid_int, name, mem_str))
            rows.sort(key=lambda x: x[0])
            return rows
        except:
            return []

if __name__ == "__main__":
    app = ProcessExplorer()
    app.mainloop()
