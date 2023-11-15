import tkinter as tk
from tkinter import *
from tkinter import filedialog
import os



def load_files():
    files = filedialog.askopenfilenames(title="Select files", filetypes=[("Production files", "*.prod"), ("Parse Table files", "*.ptbl")])

    for file_path in files:
        with open(file_path, 'r', encoding='utf-8') as file:
            file_content = file.read()
            if file_path.endswith('.prod'):
                production_text.delete(1.0, tk.END)
                generate_prod_table(file_content)
                production_label.config(text=f"Production: {os.path.basename(file_path)}")
            elif file_path.endswith('.ptbl'):
                parse_table_text.delete(1.0, tk.END)
                generate_ptbl_table(file_content)
                parse_table_label.config(text=f"Parse Table: {os.path.basename(file_path)}")

            status_var.set(f"LOADED: {os.path.basename(file_path)}")

# Function to generate a production table from file content
def generate_prod_table(file_content):
    # Clear existing content
    production_text.delete(1.0, tk.END)
    
    # Add headers to the production table
    production_text.insert(tk.END, "ID\t\tNT\t\tP\n")

    # Parse each line and add rows to the table
    for line in file_content.splitlines():
        # Split line based on commas
        line_parts = line.split(',')
        
        # Add cells to the table with borders on all sides
        for part in line_parts:
            production_text.insert(tk.END, f"{part}\t|\t", "border")
        
        # Move to the next line
        production_text.insert(tk.END, "\n")

# Function to generate a parse table from file content
def generate_ptbl_table(file_content):
    # Clear existing content
    parse_table_text.delete(1.0, tk.END)

    # Parse each line and add headers to the table based on the first line
    headers = file_content.splitlines()[0].split(',')
    for header in headers:
        parse_table_text.insert(tk.END, f"{header}\t|\t", "border")
    parse_table_text.insert(tk.END, "\n")

    # Parse each line and add rows to the table
    for line in file_content.splitlines()[1:]:
        # Split line based on commas
        line_parts = line.split(',')
        
        # Add cells to the table with borders on all sides
        for part in line_parts:
            parse_table_text.insert(tk.END, f"{part}\t|\t", "border")
        
        # Move to the next line
        parse_table_text.insert(tk.END, "\n")

# Function to configure the border style for the production and parse table
def configure_tags():
    production_text.tag_configure("border", borderwidth=1, relief="solid")
    parse_table_text.tag_configure("border", borderwidth=1, relief="solid")

# Function to handle parsing input (placeholder implementation)
def parse_input():
    input_text = input_entry.get()
    # Placeholder: Add your parsing logic here
    # For now, display the input in the status label
    parsing_status_var.set(f"PARSING: {input_text}")
    # Simulating parsing delay (you can replace this with your actual parsing logic)
    root.after(2000, lambda: parsing_status_var.set(""))  # Clear the status after 2000 milliseconds (2 seconds)

# Create the main Tkinter window
root = tk.Tk()
root.title("File Loader and Parser")
root.configure(bg="pink")  # Set background color to pink

# Create a Text widget for displaying the production table
production_text = tk.Text(root, wrap="none", height=10, width=50, bg="yellow", font=("Arial Unicode MS", 12))
production_text.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")  # Sticky set to "nsew" for expanding
production_label = tk.Label(root, text="Production:", font=("Arial", 14), bg="pink", fg="black")
production_label.grid(row=0, column=0, padx=10, pady=5)

# Create a Text widget for displaying the parse table
parse_table_text = tk.Text(root, wrap="none", height=10, width=100, bg="yellow", font=("Arial Unicode MS", 10))
parse_table_text.grid(row=1, column=1, padx=10, pady=10, columnspan=2, sticky="nsew")  # Sticky set to "nsew" for expanding
parse_table_label = tk.Label(root, text="Parse Table:", font=("Arial", 14), bg="pink", fg="black")
parse_table_label.grid(row=0, column=1, padx=10, pady=5)

# Create a button for loading files
load_button = tk.Button(root, text="LOAD", command=lambda: [load_files(), configure_tags()], font=("Arial", 14), bg="yellow", fg="black")
load_button.grid(row=2, column=2, pady=10, columnspan=2)  # Adjusted column position

# Create a status label for displaying file loading information
status_var = tk.StringVar()
status_label = tk.Label(root, textvariable=status_var, fg="green", font=("Arial", 12), bg="pink")
status_label.grid(row=2, column=1, pady=5)  # Adjusted column position

# Bottom row components
input_label = tk.Label(root, text="INPUT:", font=("Arial", 14), bg="pink", fg="black")
input_label.grid(row=3, column=0, padx=10, pady=5, sticky=tk.E)  # Adjusted column position and sticky property

# Create an entry for user input
input_entry = tk.Entry(root, width=30, font=("Arial Unicode MS", 12))
input_entry.grid(row=3, column=1, padx=10, pady=5, columnspan=1)  # Adjusted columnspan

# Create a button for parsing input
parse_button = tk.Button(root, text="PARSE", command=parse_input, font=("Arial", 14), bg="yellow", fg="black")
parse_button.grid(row=3, column=2, padx=10, pady=5)

# Create a parsing status label
parsing_status_var = tk.StringVar()
parsing_status_label = tk.Label(root, textvariable=parsing_status_var, font=("Arial", 12), bg="pink", fg="black")
parsing_status_label.grid(row=4, column=0, padx=10, pady=5, columnspan=3)  # Adjusted columnspan

# Create a Text widget for displaying parsed content
parsed_text = tk.Text(root, wrap="none", height=10, width=150, bg="lightblue", font=("Arial Unicode MS", 12))  # Adjusted width and font size
parsed_text.grid(row=5, column=0, padx=10, pady=10, columnspan=3, sticky="nsew")  # Sticky set to "nsew" for expanding

# Call configure_tags to apply the border style
configure_tags()

# Allow rows and columns to expand based on widget content
for i in range(6):
    root.grid_rowconfigure(i, weight=1)
    root.grid_columnconfigure(i, weight=1)

# Start the Tkinter event loop
root.mainloop()
