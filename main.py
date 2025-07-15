import os
import csv
import json
import tkinter as tk
from tkinter import filedialog, messagebox, PhotoImage, Label
from PIL import Image, ImageTk

CONFIG_FILE = "config.json"

def load_last_output_dir():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f).get("output_dir", "")
    return ""

def save_last_output_dir(output_path):
    output_dir = os.path.dirname(output_path)
    with open(CONFIG_FILE, "w") as f:
        json.dump({"output_dir": output_dir}, f)

# Global variable to remember filename suggestion
suggested_bin_filename = ""

def browse_input():
    global suggested_bin_filename

    file = filedialog.askopenfilename(
        title="Select CSV File",
        filetypes=[("CSV Files", "*.csv")]
    )
    if file:
        input_entry.delete(0, tk.END)
        input_entry.insert(0, file)

        base_name = os.path.splitext(os.path.basename(file))[0]
        suggested_bin_filename = base_name + ".bin"

        output_dir = load_last_output_dir()
        if output_dir and os.path.isdir(output_dir):
            output_path = os.path.join(output_dir, suggested_bin_filename)
            output_entry.delete(0, tk.END)
            output_entry.insert(0, output_path)

def browse_output():
    file = filedialog.asksaveasfilename(
        title="Save Binary File As",
        defaultextension=".bin",
        filetypes=[("Binary Files", "*.bin")],
        initialfile=suggested_bin_filename or "output.bin"
    )
    if file:
        output_entry.delete(0, tk.END)
        output_entry.insert(0, file)

def convert_csv_to_bin():
    input_csv = input_entry.get().strip()
    output_bin = output_entry.get().strip()

    if not input_csv or not output_bin:
        messagebox.showerror("Error", "Please specify both input and output paths.")
        return

    # Check if the output file already exists
    if os.path.exists(output_bin):
        confirm = messagebox.askyesno(
            "File Exists",
            f"The file '{os.path.basename(output_bin)}' already exists.\nDo you want to overwrite it?"
        )
        if not confirm:
            return

    try:
        with open(input_csv, 'r') as csvfile, open(output_bin, 'wb') as binfile:
            reader = csv.reader(csvfile)
            for row in reader:
                for value in row:
                    if value.strip():
                        binfile.write(bytes([int(value.strip(), 16)]))
        save_last_output_dir(output_bin)
        messagebox.showinfo("Success", f"Binary file saved to:\n{output_bin}")
    except Exception as e:
        messagebox.showerror("Error", f"Conversion failed:\n{e}")

# Setup GUI
root = tk.Tk()
root.title("CSV to BIN Converter")
root.geometry("500x280")

icon_dir = os.path.join(os.path.dirname(__file__), "icons")

def load_icon(filename, size=(64, 64)):
    path = os.path.join(icon_dir, filename)
    img = Image.open(path).resize(size, Image.Resampling.LANCZOS)
    return ImageTk.PhotoImage(img)

icon1 = load_icon("csv.png")
icon2 = load_icon("arrow.png")
icon3 = load_icon("bin.png")

icon_frame = tk.Frame(root)
icon_frame.pack(pady=10)

Label(icon_frame, image=icon1).pack(side='left', padx=10)
Label(icon_frame, image=icon2).pack(side='left', padx=10)
Label(icon_frame, image=icon3).pack(side='left', padx=10)

root.icon_images = [icon1, icon2, icon3]

# Input Path
tk.Label(root, text="Input CSV File:").pack(anchor='w', padx=10, pady=(10, 0))
input_frame = tk.Frame(root)
input_frame.pack(fill='x', padx=10)
input_entry = tk.Entry(input_frame)
input_entry.pack(side='left', fill='x', expand=True)
tk.Button(input_frame, text="Browse", command=browse_input).pack(side='right', padx=5)

# Output Path
tk.Label(root, text="Output BIN File:").pack(anchor='w', padx=10, pady=(10, 0))
output_frame = tk.Frame(root)
output_frame.pack(fill='x', padx=10)
output_entry = tk.Entry(output_frame)
output_entry.pack(side='left', fill='x', expand=True)
tk.Button(output_frame, text="Browse", command=browse_output).pack(side='right', padx=5)

# Convert Button
tk.Button(root, text="Convert", command=convert_csv_to_bin, height=2).pack(pady=20)

root.mainloop()