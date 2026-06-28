import hashlib
import os
import json
import datetime
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# ─── Core Functions ───────────────────────────────────────────────────────────

def compute_hash(filepath, algorithm="sha256"):
    h = hashlib.new(algorithm)
    try:
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                h.update(chunk)
        return h.hexdigest()
    except FileNotFoundError:
        return None

def save_baseline(files, algorithm, baseline_file="baseline.json"):
    baseline = {}
    for filepath in files:
        h = compute_hash(filepath, algorithm)
        if h:
            baseline[filepath] = {"hash": h, "algorithm": algorithm,
                                   "timestamp": str(datetime.datetime.now())}
    with open(baseline_file, "w") as f:
        json.dump(baseline, f, indent=4)
    return baseline

def verify_files(baseline_file="baseline.json"):
    if not os.path.exists(baseline_file):
        return None, "Baseline file not found."
    with open(baseline_file, "r") as f:
        baseline = json.load(f)
    results = []
    for filepath, data in baseline.items():
        current_hash = compute_hash(filepath, data["algorithm"])
        status = "✅ UNCHANGED" if current_hash == data["hash"] else "❌ MODIFIED"
        results.append({"file": filepath, "status": status,
                         "expected": data["hash"], "current": current_hash or "FILE NOT FOUND"})
    return results, None

def generate_pdf_report(results, algorithm):
    report_name = f"integrity_report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    c = canvas.Canvas(report_name, pagesize=letter)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, 750, "File Integrity Report")
    c.setFont("Helvetica", 12)
    c.drawString(50, 730, f"Generated: {datetime.datetime.now()}")
    c.drawString(50, 710, f"Algorithm: {algorithm.upper()}")
    c.line(50, 700, 560, 700)
    y = 680
    for r in results:
        c.setFont("Helvetica-Bold", 11)
        c.drawString(50, y, f"File: {os.path.basename(r['file'])}")
        c.setFont("Helvetica", 10)
        c.drawString(50, y - 15, f"Status: {r['status']}")
        c.drawString(50, y - 28, f"Expected: {r['expected'][:60]}...")
        c.drawString(50, y - 41, f"Current:  {r['current'][:60]}...")
        y -= 70
        if y < 100:
            c.showPage()
            y = 750
    c.save()
    return report_name

# ─── GUI ──────────────────────────────────────────────────────────────────────

class IntegrityCheckerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File Integrity Checker V2")
        self.root.geometry("700x550")
        self.root.configure(bg="#1e1e2e")
        self.selected_files = []
        self.algorithm = tk.StringVar(value="sha256")
        self.build_ui()

    def build_ui(self):
        # Title
        tk.Label(self.root, text="🔐 File Integrity Checker V2",
                 font=("Helvetica", 18, "bold"),
                 bg="#1e1e2e", fg="#cba6f7").pack(pady=15)

        # Algorithm selector
        algo_frame = tk.Frame(self.root, bg="#1e1e2e")
        algo_frame.pack()
        tk.Label(algo_frame, text="Algorithm:", bg="#1e1e2e",
                 fg="white", font=("Helvetica", 11)).pack(side="left", padx=5)
        for algo in ["md5", "sha1", "sha256", "sha512"]:
            tk.Radiobutton(algo_frame, text=algo.upper(), variable=self.algorithm,
                           value=algo, bg="#1e1e2e", fg="#a6e3a1",
                           selectcolor="#313244", font=("Helvetica", 10)).pack(side="left", padx=8)

        # Buttons
        btn_frame = tk.Frame(self.root, bg="#1e1e2e")
        btn_frame.pack(pady=15)

        tk.Button(btn_frame, text="📂 Select Files", command=self.select_files,
                  bg="#313244", fg="white", width=18,
                  font=("Helvetica", 10, "bold")).grid(row=0, column=0, padx=8)
        tk.Button(btn_frame, text="💾 Save Baseline", command=self.save_baseline,
                  bg="#313244", fg="white", width=18,
                  font=("Helvetica", 10, "bold")).grid(row=0, column=1, padx=8)
        tk.Button(btn_frame, text="🔍 Verify Files", command=self.verify,
                  bg="#313244", fg="white", width=18,
                  font=("Helvetica", 10, "bold")).grid(row=0, column=2, padx=8)
        tk.Button(btn_frame, text="📄 Export PDF", command=self.export_pdf,
                  bg="#313244", fg="white", width=18,
                  font=("Helvetica", 10, "bold")).grid(row=1, column=1, padx=8, pady=8)

        # File list
        tk.Label(self.root, text="Selected Files:",
                 bg="#1e1e2e", fg="#89b4fa",
                 font=("Helvetica", 11, "bold")).pack()
        self.file_listbox = tk.Listbox(self.root, width=80, height=5,
                                        bg="#313244", fg="white",
                                        font=("Helvetica", 9))
        self.file_listbox.pack(pady=5)

        # Results
        tk.Label(self.root, text="Results:",
                 bg="#1e1e2e", fg="#89b4fa",
                 font=("Helvetica", 11, "bold")).pack()
        self.result_box = tk.Text(self.root, width=80, height=12,
                                   bg="#181825", fg="#cdd6f4",
                                   font=("Courier", 9))
        self.result_box.pack(pady=5)

        self.last_results = []

    def select_files(self):
        files = filedialog.askopenfilenames(title="Select files to monitor")
        self.selected_files = list(files)
        self.file_listbox.delete(0, tk.END)
        for f in self.selected_files:
            self.file_listbox.insert(tk.END, f)

    def save_baseline(self):
        if not self.selected_files:
            messagebox.showwarning("No Files", "Please select files first.")
            return
        save_baseline(self.selected_files, self.algorithm.get())
        messagebox.showinfo("Saved", "Baseline saved to baseline.json ✅")

    def verify(self):
        results, error = verify_files()
        if error:
            messagebox.showerror("Error", error)
            return
        self.last_results = results
        self.result_box.delete(1.0, tk.END)
        for r in results:
            self.result_box.insert(tk.END,
                f"{r['status']} {os.path.basename(r['file'])}\n"
                f"   Expected: {r['expected'][:50]}...\n"
                f"   Current:  {r['current'][:50]}...\n\n")

    def export_pdf(self):
        if not self.last_results:
            messagebox.showwarning("No Results", "Please verify files first.")
            return
        report = generate_pdf_report(self.last_results, self.algorithm.get())
        messagebox.showinfo("PDF Exported", f"Report saved as:\n{report}")

# ─── Main ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    root = tk.Tk()
    app = IntegrityCheckerApp(root)
    root.mainloop()
