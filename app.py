import tkinter as tk
from tkinter import filedialog, messagebox

from pypdf import PdfReader
from docx import Document

from pii_anonymizer import anonymize_text

# -----------------------------------------
# Read uploaded file
# -----------------------------------------

def read_file(filename):

    if filename.lower().endswith(".txt"):
        with open(filename, "r", encoding="utf-8") as file:
            return file.read()

    elif filename.lower().endswith(".pdf"):
        reader = PdfReader(filename)

        text = ""

        for page in reader.pages:
            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

        return text

    elif filename.lower().endswith(".docx"):
        document = Document(filename)

        text = ""

        for paragraph in document.paragraphs:
            text += paragraph.text + "\n"

        return text

    return ""

# -----------------------------------------
# Paste text / clear input
# -----------------------------------------

def clear_input():
    input_box.delete("1.0", tk.END)

def clear_output():
    output_box.delete("1.0", tk.END)
    count_label.config(text="PII Detected: 0")

# -----------------------------------------
# Anonymize
# -----------------------------------------

def anonymize():

    text = input_box.get("1.0", tk.END).strip()

    if not text:
        messagebox.showwarning(
            "No Input",
            "Please enter or upload healthcare text."
        )
        return

    result, count = anonymize_text(text)

    output_box.delete("1.0", tk.END)
    output_box.insert(tk.END, result)

    count_label.config(
        text=f"PII Detected: {count}"
    )

# -----------------------------------------
# Upload file
# -----------------------------------------

def upload_file():

    filename = filedialog.askopenfilename(
        title="Select Healthcare Document",
        filetypes=[
            ("Supported files", "*.txt *.pdf *.docx"),
            ("Text files", "*.txt"),
            ("PDF files", "*.pdf"),
            ("Word documents", "*.docx")
        ]
    )

    if not filename:
        return

    try:
        text = read_file(filename)

        if not text.strip():
            messagebox.showwarning(
                "No Text",
                "No readable text was found in the file."
            )
            return

        input_box.delete("1.0", tk.END)
        input_box.insert(tk.END, text)

    except Exception as e:
        messagebox.showerror(
            "Error",
            f"Could not read the file.\n\n{e}"
        )

# -----------------------------------------
# Save de-identified text
# -----------------------------------------

def save_output():

    text = output_box.get("1.0", tk.END).strip()

    if not text:
        messagebox.showwarning(
            "No Output",
            "Please anonymize some text first."
        )
        return

    filename = filedialog.asksaveasfilename(
        title="Save De-identified Text",
        defaultextension=".txt",
        filetypes=[
            ("Text file", "*.txt")
        ]
    )

    if not filename:
        return

    with open(filename, "w", encoding="utf-8") as file:
        file.write(text)

    messagebox.showinfo(
        "Saved",
        "De-identified text saved successfully."
    )

# =========================================
# GUI
# =========================================

root = tk.Tk()

root.title("Healthcare PII De-identification")
root.geometry("950x700")
root.minsize(800, 600)

# Background
root.configure(bg="#f4f6f8")

# -----------------------------------------
# Title
# -----------------------------------------

title = tk.Label(
    root,
    text="Healthcare PII De-identification",
    font=("Arial", 24, "bold"),
    bg="#f4f6f8",
    fg="#1f2937"
)

title.pack(pady=(20, 5))

subtitle = tk.Label(
    root,
    text="Privacy-Preserving NLP for Healthcare Text",
    font=("Arial", 12),
    bg="#f4f6f8",
    fg="#6b7280"
)

subtitle.pack(pady=(0, 15))

# -----------------------------------------
# Input label
# -----------------------------------------

input_label = tk.Label(
    root,
    text="Healthcare Text / Document Content",
    font=("Arial", 12, "bold"),
    bg="#f4f6f8",
    fg="#1f2937"
)

input_label.pack(anchor="w", padx=30)

# -----------------------------------------
# Input box
# -----------------------------------------

input_box = tk.Text(
    root,
    height=10,
    font=("Arial", 11),
    wrap=tk.WORD
)

input_box.pack(
    fill="both",
    expand=True,
    padx=30,
    pady=8
)

# -----------------------------------------
# Buttons
# -----------------------------------------

button_frame = tk.Frame(
    root,
    bg="#f4f6f8"
)

button_frame.pack(pady=8)

tk.Button(
    button_frame,
    text="Upload File",
    command=upload_file,
    width=15,
    font=("Arial", 10, "bold")
).grid(row=0, column=0, padx=5)

tk.Button(
    button_frame,
    text="Anonymize",
    command=anonymize,
    width=15,
    font=("Arial", 10, "bold")
).grid(row=0, column=1, padx=5)

tk.Button(
    button_frame,
    text="Clear",
    command=clear_input,
    width=15,
    font=("Arial", 10)
).grid(row=0, column=2, padx=5)

# -----------------------------------------
# Output label
# -----------------------------------------

output_label = tk.Label(
    root,
    text="De-identified Output",
    font=("Arial", 12, "bold"),
    bg="#f4f6f8",
    fg="#1f2937"
)

output_label.pack(anchor="w", padx=30, pady=(12, 0))

# -----------------------------------------
# Output box
# -----------------------------------------

output_box = tk.Text(
    root,
    height=10,
    font=("Arial", 11),
    wrap=tk.WORD
)

output_box.pack(
    fill="both",
    expand=True,
    padx=30,
    pady=8
)

# -----------------------------------------
# Bottom controls
# -----------------------------------------

bottom_frame = tk.Frame(
    root,
    bg="#f4f6f8"
)

bottom_frame.pack(pady=10)

count_label = tk.Label(
    bottom_frame,
    text="PII Detected: 0",
    font=("Arial", 11, "bold"),
    bg="#f4f6f8",
    fg="#374151"
)

count_label.grid(row=0, column=0, padx=20)

tk.Button(
    bottom_frame,
    text="Save De-identified Text",
    command=save_output,
    width=22,
    font=("Arial", 10, "bold")
).grid(row=0, column=1, padx=10)

tk.Button(
    bottom_frame,
    text="Clear Output",
    command=clear_output,
    width=15,
    font=("Arial", 10)
).grid(row=0, column=2, padx=10)

# -----------------------------------------
# Start application
# -----------------------------------------

root.mainloop()