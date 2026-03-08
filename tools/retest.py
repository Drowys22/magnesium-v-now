import customtkinter as ctk
import re

ctk.set_appearance_mode("dark")

class RegexTester(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Magnesium Regex Tester")
        self.geometry("900x560")
        self.resizable(False, False)
        self.configure(fg_color="#020617")
        self.build_ui()

    def build_ui(self):
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)
        header = ctk.CTkFrame(self, fg_color="#020617")
        header.grid(row=0, column=0, sticky="new", padx=10, pady=(10, 4))
        title = ctk.CTkLabel(header, text="Regex Tester", font=("Segoe UI Semibold", 20), text_color="#E5E7EB")
        title.pack(side="left", padx=(4, 10))
        self.status_label = ctk.CTkLabel(header, text="", font=("Segoe UI", 11), text_color="#9CA3AF")
        self.status_label.pack(side="left")
        body = ctk.CTkFrame(self, fg_color="#020617")
        body.grid(row=1, column=0, sticky="new", padx=10, pady=(0, 4))
        body.grid_columnconfigure(1, weight=1)
        pattern_label = ctk.CTkLabel(body, text="Pattern", font=("Segoe UI", 11), text_color="#E5E7EB")
        pattern_label.grid(row=0, column=0, sticky="w", padx=(0, 4), pady=(4, 2))
        self.pattern_entry = ctk.CTkEntry(body, placeholder_text=r"\w+")
        self.pattern_entry.grid(row=0, column=1, sticky="ew", padx=(0, 4), pady=(4, 2))
        flags_label = ctk.CTkLabel(body, text="Flags", font=("Segoe UI", 11), text_color="#E5E7EB")
        flags_label.grid(row=0, column=2, sticky="w", padx=(0, 4), pady=(4, 2))
        self.flag_ignorecase = ctk.CTkCheckBox(body, text="IGNORECASE")
        self.flag_ignorecase.grid(row=0, column=3, padx=(0, 4), pady=(4, 2))
        self.flag_multiline = ctk.CTkCheckBox(body, text="MULTILINE")
        self.flag_multiline.grid(row=0, column=4, padx=(0, 4), pady=(4, 2))
        self.flag_dotall = ctk.CTkCheckBox(body, text="DOTALL")
        self.flag_dotall.grid(row=0, column=5, padx=(0, 4), pady=(4, 2))
        test_label = ctk.CTkLabel(body, text="Test text", font=("Segoe UI", 11), text_color="#E5E7EB")
        test_label.grid(row=1, column=0, sticky="w", padx=(0, 4), pady=(2, 2))
        self.test_box = ctk.CTkTextbox(body, height=120, fg_color="#050816", text_color="#E5E7EB", corner_radius=8)
        self.test_box.grid(row=1, column=1, columnspan=5, sticky="ew", padx=(0, 4), pady=(2, 4))
        self.test_box.insert("end", "Sample text 123\nAnother line 456\nRegex test line.")
        run_btn = ctk.CTkButton(body, text="Run", width=80, command=self.run_regex)
        run_btn.grid(row=0, column=6, padx=(4, 0), pady=(4, 2))
        main = ctk.CTkFrame(self, fg_color="#020617")
        main.grid(row=2, column=0, sticky="nsew", padx=10, pady=(0, 10))
        main.grid_rowconfigure(0, weight=1)
        main.grid_rowconfigure(1, weight=1)
        main.grid_columnconfigure(0, weight=1)
        matches_frame = ctk.CTkFrame(main, fg_color="#050816", corner_radius=10)
        matches_frame.grid(row=0, column=0, sticky="nsew", padx=0, pady=(0, 4))
        matches_frame.grid_rowconfigure(1, weight=1)
        matches_frame.grid_columnconfigure(0, weight=1)
        matches_title = ctk.CTkLabel(matches_frame, text="Matches", font=("Segoe UI Semibold", 14), text_color="#E5E7EB")
        matches_title.grid(row=0, column=0, sticky="w", padx=8, pady=(8, 2))
        self.matches_box = ctk.CTkTextbox(matches_frame, fg_color="#020617", text_color="#E5E7EB", corner_radius=8)
        self.matches_box.grid(row=1, column=0, sticky="nsew", padx=8, pady=(0, 8))
        explain_frame = ctk.CTkFrame(main, fg_color="#050816", corner_radius=10)
        explain_frame.grid(row=1, column=0, sticky="nsew", padx=0, pady=(4, 0))
        explain_frame.grid_rowconfigure(1, weight=1)
        explain_frame.grid_columnconfigure(0, weight=1)
        explain_title = ctk.CTkLabel(explain_frame, text="Explanation", font=("Segoe UI Semibold", 14), text_color="#E5E7EB")
        explain_title.grid(row=0, column=0, sticky="w", padx=8, pady=(8, 2))
        self.explain_box = ctk.CTkTextbox(explain_frame, fg_color="#020617", text_color="#E5E7EB", corner_radius=8)
        self.explain_box.grid(row=1, column=0, sticky="nsew", padx=8, pady=(0, 8))
        self.explain_box.insert("end", "Basic regex tester. No automatic explanation implemented.")

    def run_regex(self):
        pattern = self.pattern_entry.get()
        text = self.test_box.get("1.0", "end")
        flags = 0
        if self.flag_ignorecase.get():
            flags |= re.IGNORECASE
        if self.flag_multiline.get():
            flags |= re.MULTILINE
        if self.flag_dotall.get():
            flags |= re.DOTALL
        self.matches_box.configure(state="normal")
        self.matches_box.delete("1.0", "end")
        try:
            regex = re.compile(pattern, flags)
        except re.error as e:
            self.matches_box.insert("end", f"Regex error: {e}")
            self.matches_box.configure(state="disabled")
            self.status_label.configure(text="Invalid pattern")
            return
        matches = list(regex.finditer(text))
        if not matches:
            self.matches_box.insert("end", "No matches.")
            self.matches_box.configure(state="disabled")
            self.status_label.configure(text="No matches")
            return
        for i, m in enumerate(matches, start=1):
            span = m.span()
            self.matches_box.insert("end", f"Match {i}: {m.group()}  at {span}\n")
            groups = m.groups()
            if groups:
                for gi, g in enumerate(groups, start=1):
                    self.matches_box.insert("end", f"  Group {gi}: {g}\n")
        self.matches_box.configure(state="disabled")
        self.status_label.configure(text=f"{len(matches)} matches")

if __name__ == "__main__":
    app = RegexTester()
    app.mainloop()
