import tkinter as tk
from tkinter import filedialog
import os

def load_files():
    files = filedialog.askopenfilenames(title="Select files", filetypes=[("Production files", "*.prod"), ("Parse Table files", "*.ptbl")])

    for file_path in files:
        with open(file_path, 'r') as file:
            file_content = file.read()
            if file_path.endswith('.prod'):
                production_text.delete(1.0, tk.END)
                production_text.insert(tk.END, file_content)
                production_label.config(text=f"Production: {os.path.basename(file_path)}")
            elif file_path.endswith('.ptbl'):
                parse_table_text.delete(1.0, tk.END)
                parse_table_text.insert(tk.END, file_content)
                parse_table_label.config(text=f"Parse Table: {os.path.basename(file_path)}")

            status_var.set(f"LOADED: {file_path}")

def parse_input():
    input_text = input_entry.get()
    # Add your parsing logic here, for now, display it in the status label
    status_var.set(f"INPUT: {input_text}")

root = tk.Tk()
root.title("File Loader and Parser")
root.configure(bg="pink")  # Set background color to pink

production_text = tk.Text(root, wrap="none", height=10, width=50, bg="yellow", font=("Arial", 12))
production_text.grid(row=1, column=0, padx=10, pady=10)
production_label = tk.Label(root, text="Production:", font=("Arial", 14), bg="pink", fg="black")
production_label.grid(row=0, column=0, padx=10, pady=5)

parse_table_text = tk.Text(root, wrap="none", height=10, width=50, bg="yellow", font=("Arial", 12))
parse_table_text.grid(row=1, column=1, padx=10, pady=10, columnspan=2)  # Adjusted columnspan
parse_table_label = tk.Label(root, text="Parse Table:", font=("Arial", 14), bg="pink", fg="black")
parse_table_label.grid(row=0, column=1, padx=10, pady=5)

load_button = tk.Button(root, text="LOAD", command=load_files, font=("Arial", 14), bg="yellow", fg="black")
load_button.grid(row=2, column=2, pady=10)  # Adjusted column position

status_var = tk.StringVar()
status_label = tk.Label(root, textvariable=status_var, fg="green", font=("Arial", 12), bg="pink")
status_label.grid(row=2, column=1, pady=5)  # Adjusted column position

# Bottom row components
input_label = tk.Label(root, text="INPUT:", font=("Arial", 14), bg="pink", fg="black")
input_label.grid(row=3, column= 0, padx=10, pady=5, sticky=tk.E)  # Adjusted column position and sticky property

input_entry = tk.Entry(root, width=30, font=("Arial", 12))
input_entry.grid(row=3, column=1, padx=10, pady=5)

parse_button = tk.Button(root, text="PARSE", command=parse_input, font=("Arial", 14), bg="yellow", fg="black")
parse_button.grid(row=3, column=2, padx=10, pady=5)

root.mainloop()
