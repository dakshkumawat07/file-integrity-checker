# 🔐 File Integrity Checker V2

> A professional-grade file integrity monitoring tool with GUI interface,
> built as part of my cybersecurity learning journey for IIT Kanpur B.Cyber.

![Python](https://img.shields.io/badge/Python-3.x-blue)
![Security](https://img.shields.io/badge/Security-File%20Integrity-red)
![GUI](https://img.shields.io/badge/GUI-Tkinter-green)
![PDF](https://img.shields.io/badge/Reports-PDF-orange)

---

## 🆕 What's New in V2

| Feature | V1 | V2 |
|---------|----|----|
| Interface | CLI only | ✅ GUI + CLI |
| Algorithms | SHA-256 only | ✅ MD5, SHA-1, SHA-256, SHA-512 |
| File Support | Single file | ✅ Batch verification |
| Reports | Terminal output | ✅ PDF export |

---

## ✨ Features

- 🖥️ **Clean dark-themed GUI** built with Tkinter
- 🔑 **4 hashing algorithms** — MD5, SHA-1, SHA-256, SHA-512
- 📂 **Batch file monitoring** — select multiple files at once
- 💾 **Baseline saved to JSON** — persistent across sessions
- ❌ **Instant tamper detection** — flags any file modification
- 📄 **PDF report export** — professional integrity reports

---

## 🚀 Installation & Usage

### Install dependencies
```bash
pip install reportlab
```

### Run the tool
```bash
python3 file_integrity.py
```

### How to use
1. 📂 Click **Select Files** to choose files to monitor
2. 🔑 Choose your **hashing algorithm** (SHA-256 recommended)
3. 💾 Click **Save Baseline** to record original hashes
4. 🔍 Click **Verify Files** anytime to detect changes
5. 📄 Click **Export PDF** to generate an integrity report

---

## 🧠 Concepts Learned

- 🔐 Cryptographic hashing (MD5, SHA-1, SHA-256, SHA-512)
- 🛡️ File integrity monitoring techniques
- 🖥️ GUI development with Tkinter
- 📄 PDF generation with ReportLab
- 🔍 Detecting unauthorized file modifications
- 📦 JSON for persistent data storage

---

## 📸 Screenshots

### ✅ File Unchanged
> Hash matches baseline — file is safe

### ❌ Tampering Detected
> Hash mismatch detected — file has been modified

---
## 🔍 How It Works in Action

### ✅ File Unchanged
When you verify a file that hasn't been modified,
the tool computes its current hash and compares it
with the saved baseline hash. If they match perfectly,
it confirms the file is safe and untampered.

### ❌ Tampering Detected
If any change is made to the file — even a single
character added or removed — the hash changes completely.
The tool instantly flags it as MODIFIED, proving
unauthorized changes have occurred.

### 📄 PDF Report
After verification, you can export a detailed PDF report
containing the file name, expected hash, current hash,
status, and timestamp — useful as forensic evidence.
---

## ⚠️ Legal Notice
This tool is intended for **educational purposes only**.
Only monitor files you own or have explicit permission to monitor.

---

## 👨‍💻 Author
**Daksh Kumawat** | Cybersecurity Enthusiast
🔗 [GitHub](https://github.com/dakshkumawat07)
