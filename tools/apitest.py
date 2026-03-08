import customtkinter as ctk
import urllib.request
import urllib.error
import json

ctk.set_appearance_mode("dark")

class ApiTester(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Magnesium API Tester")
        self.geometry("900x600")
        self.resizable(False, False)
        self.configure(fg_color="#020617")
        self.build_ui()

    def build_ui(self):
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)
        header = ctk.CTkFrame(self, fg_color="#020617")
        header.grid(row=0, column=0, sticky="new", padx=10, pady=(10, 4))
        title = ctk.CTkLabel(header, text="API Tester", font=("Segoe UI Semibold", 20), text_color="#E5E7EB")
        title.pack(side="left", padx=(4, 10))
        self.status_label = ctk.CTkLabel(header, text="", font=("Segoe UI", 11), text_color="#9CA3AF")
        self.status_label.pack(side="left")
        top = ctk.CTkFrame(self, fg_color="#020617")
        top.grid(row=1, column=0, sticky="new", padx=10, pady=(0, 4))
        top.grid_columnconfigure(1, weight=1)
        self.method_var = ctk.StringVar(value="GET")
        method_box = ctk.CTkComboBox(top, values=["GET", "POST", "PUT", "DELETE"], variable=self.method_var, width=90)
        method_box.grid(row=0, column=0, padx=(0, 6), pady=4, sticky="w")
        self.url_entry = ctk.CTkEntry(top, placeholder_text="https://api.example.com/endpoint")
        self.url_entry.grid(row=0, column=1, padx=(0, 6), pady=4, sticky="ew")
        send_btn = ctk.CTkButton(top, text="Send", width=80, command=self.send_request)
        send_btn.grid(row=0, column=2, padx=(0, 0), pady=4, sticky="e")
        body = ctk.CTkFrame(self, fg_color="#020617")
        body.grid(row=2, column=0, sticky="nsew", padx=10, pady=(0, 10))
        body.grid_rowconfigure(0, weight=1)
        body.grid_rowconfigure(1, weight=1)
        body.grid_columnconfigure(0, weight=1)
        req_frame = ctk.CTkFrame(body, fg_color="#050816", corner_radius=10)
        req_frame.grid(row=0, column=0, sticky="nsew", padx=0, pady=(0, 4))
        req_frame.grid_rowconfigure(2, weight=1)
        req_frame.grid_columnconfigure(0, weight=1)
        req_title = ctk.CTkLabel(req_frame, text="Request", font=("Segoe UI Semibold", 14), text_color="#E5E7EB")
        req_title.grid(row=0, column=0, sticky="w", padx=10, pady=(8, 2))
        headers_label = ctk.CTkLabel(req_frame, text="Headers (JSON)", font=("Segoe UI", 11), text_color="#9CA3AF")
        headers_label.grid(row=1, column=0, sticky="w", padx=10, pady=(2, 0))
        self.headers_box = ctk.CTkTextbox(req_frame, height=70, fg_color="#020617", text_color="#E5E7EB", corner_radius=8)
        self.headers_box.grid(row=2, column=0, sticky="nsew", padx=10, pady=(2, 4))
        body_label = ctk.CTkLabel(req_frame, text="Body (JSON or raw)", font=("Segoe UI", 11), text_color="#9CA3AF")
        body_label.grid(row=3, column=0, sticky="w", padx=10, pady=(2, 0))
        self.body_box = ctk.CTkTextbox(req_frame, height=90, fg_color="#020617", text_color="#E5E7EB", corner_radius=8)
        self.body_box.grid(row=4, column=0, sticky="nsew", padx=10, pady=(2, 8))
        res_frame = ctk.CTkFrame(body, fg_color="#050816", corner_radius=10)
        res_frame.grid(row=1, column=0, sticky="nsew", padx=0, pady=(4, 0))
        res_frame.grid_rowconfigure(2, weight=1)
        res_frame.grid_columnconfigure(0, weight=1)
        res_title = ctk.CTkLabel(res_frame, text="Response", font=("Segoe UI Semibold", 14), text_color="#E5E7EB")
        res_title.grid(row=0, column=0, sticky="w", padx=10, pady=(8, 2))
        self.res_meta = ctk.CTkLabel(res_frame, text="", font=("Segoe UI", 11), text_color="#9CA3AF")
        self.res_meta.grid(row=1, column=0, sticky="w", padx=10, pady=(0, 2))
        self.res_box = ctk.CTkTextbox(res_frame, fg_color="#020617", text_color="#E5E7EB", corner_radius=8)
        self.res_box.grid(row=2, column=0, sticky="nsew", padx=10, pady=(2, 8))

    def send_request(self):
        method = self.method_var.get().upper()
        url = self.url_entry.get().strip()
        headers_raw = self.headers_box.get("1.0", "end").strip()
        body_raw = self.body_box.get("1.0", "end").strip()
        if not url:
            self.status_label.configure(text="URL is required")
            return
        headers = {}
        if headers_raw:
            try:
                headers = json.loads(headers_raw)
                if not isinstance(headers, dict):
                    headers = {}
            except:
                headers = {}
        data = None
        if body_raw:
            if method in ("POST", "PUT", "PATCH", "DELETE"):
                try:
                    json_body = json.loads(body_raw)
                    data = json.dumps(json_body).encode("utf-8")
                    if "Content-Type" not in headers:
                        headers["Content-Type"] = "application/json"
                except:
                    data = body_raw.encode("utf-8")
                    if "Content-Type" not in headers:
                        headers["Content-Type"] = "text/plain"
        req = urllib.request.Request(url=url, method=method)
        for k, v in headers.items():
            req.add_header(k, str(v))
        try:
            with urllib.request.urlopen(req, data=data, timeout=20) as resp:
                status = resp.status
                reason = getattr(resp, "reason", "")
                raw = resp.read()
                text = raw.decode("utf-8", errors="replace")
                pretty = self.try_pretty_json(text)
                self.res_box.configure(state="normal")
                self.res_box.delete("1.0", "end")
                self.res_box.insert("end", pretty)
                self.res_box.configure(state="normal")
                self.res_meta.configure(text=f"Status: {status} {reason}")
                self.status_label.configure(text="Request completed")
        except urllib.error.HTTPError as e:
            raw = e.read()
            text = raw.decode("utf-8", errors="replace")
            pretty = self.try_pretty_json(text)
            self.res_box.configure(state="normal")
            self.res_box.delete("1.0", "end")
            self.res_box.insert("end", pretty)
            self.res_box.configure(state="normal")
            self.res_meta.configure(text=f"HTTP Error: {e.code}")
            self.status_label.configure(text="HTTP error")
        except urllib.error.URLError as e:
            self.res_box.configure(state="normal")
            self.res_box.delete("1.0", "end")
            self.res_box.insert("end", str(e.reason))
            self.res_box.configure(state="normal")
            self.res_meta.configure(text="Connection error")
            self.status_label.configure(text="Connection error")
        except Exception as e:
            self.res_box.configure(state="normal")
            self.res_box.delete("1.0", "end")
            self.res_box.insert("end", str(e))
            self.res_box.configure(state="normal")
            self.res_meta.configure(text="Error")
            self.status_label.configure(text="Error")

    def try_pretty_json(self, text):
        try:
            obj = json.loads(text)
            return json.dumps(obj, indent=2, ensure_ascii=False)
        except:
            return text

if __name__ == "__main__":
    app = ApiTester()
    app.mainloop()
