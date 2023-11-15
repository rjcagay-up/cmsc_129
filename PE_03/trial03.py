import tkinter as tk
from tkinter import filedialog, ttk
import os


# Create the main Tkinter window
root = tk.Tk()
root.title("File Loader and Parser")

# Get the screen width and height
screen_width = root.winfo_screenwidth()-10
screen_height = root.winfo_screenheight()-100

# Set the window size to adapt to the screen
root.geometry(f"{screen_width}x{screen_height}+0+0")


# Arrays to store data from productions and parse table
prod_data = []
ptbl_data = []

def create_table(data, headers, label_text, tree_widget):
    # Clear existing content
    tree_widget.delete(*tree_widget.get_children())

    # Create columns
    tree_widget["columns"] = headers
    for header in headers:
        tree_widget.heading(header, text=header)
        tree_widget.column(header, anchor=tk.CENTER, minwidth=10, width=50)  # Adjust width as needed

    # Populate rows
    for row in data:
        tree_widget.insert("", tk.END, values=row)

    label_text.config(text=f"{label_text.cget('text')} ({len(data)} rows)")

def load_and_store_data(file_path, prod_data, ptbl_data):
    with open(file_path, 'r', encoding='utf-8') as file:
        file_content = file.read()
        data_array = []

        # Load data into a temporary array
        for row in file_content.splitlines():
            columns = tuple(row.split(','))  # Separate columns by commas
            data_array.append(columns)

        # Check if it's a production file and store data in prod_data
        if file_path.endswith('.prod'):
            prod_data.clear()
            prod_data.extend(data_array)
        elif file_path.endswith('.ptbl'):
            # Ensure that ptbl_data contains only data rows (exclude the header)
            ptbl_data.clear()
            ptbl_data.extend(data_array)

    return prod_data, ptbl_data

def load_files():
    # Separate arrays for production and parse table data
    prod_data = []
    ptbl_data = []
    headers = []

    files = filedialog.askopenfilenames(
        title="Select files",
        filetypes=[("Production files", "*.prod"), ("Parse Table files", "*.ptbl")]
    )

    for file_path in files:
        if file_path.endswith('.prod'):
            prod_data, _ = load_and_store_data(file_path, prod_data, [])
            create_table(prod_data, ["ID", "NT", "P"], production_label, production_tree)
        elif file_path.endswith('.ptbl'):
            _, ptbl_data = load_and_store_data(file_path, [], ptbl_data)
            # Extract headers from the first line of the parse table file
            headers = ptbl_data[0]
            create_table(ptbl_data[1:], headers, parse_table_label, parse_table_tree)

        status_var.set(f"LOADED: {os.path.basename(file_path)}")

# Function to handle parsing input (placeholder implementation)
def parse_input():
    input_text = input_entry.get()
    # Placeholder: Add your parsing logic here
    # For now, display the input in the status label
    parsing_status_var.set(f"PARSING: {input_text}")
    # Simulating parsing delay (you can replace this with your actual parsing logic)
    root.after(2000, lambda: parsing_status_var.set(""))  # Clear the status after 2000 milliseconds (2 seconds)

# Function to configure the border style for the production and parse table
def configure_tags():
    # Configure style for the production tree
    production_tree.tag_configure("border", background="white")
    production_tree["show"] = "headings"
    production_tree.heading("#0", text="", anchor="w")
    production_tree.column("#0", stretch=tk.NO, width=1)
    production_tree.tag_configure("border", background="white")

    # Configure style for the parse table tree
    parse_table_tree.tag_configure("border", background="white")
    parse_table_tree["show"] = "headings"
    parse_table_tree.heading("#0", text="", anchor="w")
    parse_table_tree.column("#0", stretch=tk.NO, width=1)
    parse_table_tree.tag_configure("border", background="white")



# Create a Treeview widget for displaying the production table
production_tree = ttk.Treeview(root, height=10)
production_tree.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
production_tree.config(xscrollcommand=lambda f, l: prodscrollbar.set(f, l))
production_label = tk.Label(root, text="Production:", font=("Arial", 14))
production_label.grid(row=0, column=0, padx=10, pady=5)

# Create a Treeview widget for displaying the parse table
parse_table_tree = ttk.Treeview(root, height=10)
parse_table_tree.grid(row=1, column=1, padx=10, pady=10, columnspan=1, sticky="nsew")
parse_table_tree.config(xscrollcommand=lambda f, l: parsescrollbar.set(f, l))
parse_table_label = tk.Label(root, text="Parse Table:", font=("Arial", 14))
parse_table_label.grid(row=0, column=1, padx=10, pady=5)

# Create a Frame for the production table and its scrollbar
production_frame = tk.Frame(root, width=(screen_width-100)/2,borderwidth=10)
production_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")


prodscrollbar = ttk.Scrollbar(production_frame, orient="horizontal")
prodscrollbar.grid(row=1, column=0, sticky="ew")

production_tree = ttk.Treeview(production_frame, height=10, show="headings", xscrollcommand = prodscrollbar.set)
production_tree.grid(row=0, column=0, sticky="nsew")
prodscrollbar.config(command=production_tree.xview)

# Create a Frame for the parse table and its scrollbar
parse_frame = tk.Frame(root)
parse_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

parse_table_tree = ttk.Treeview(parse_frame, height=10, show="headings")
parse_table_tree.grid(row=0, column=0, sticky="nsew")
parsescrollbar = ttk.Scrollbar(parse_frame, orient="horizontal", command=parse_table_tree.xview)
parsescrollbar.grid(row=1, column=0, sticky="ew")
parse_table_tree['xscrollcommand'] = parsescrollbar.set

# Create a button for loading files
load_button = tk.Button(root, text="LOAD", command=lambda: [load_files(), configure_tags()], font=("Arial", 14))
load_button.grid(row=2, column=2, pady=10, columnspan=2)

# Create a status label for displaying file loading information
status_var = tk.StringVar()
status_label = tk.Label(root, textvariable=status_var, fg="green", font=("Arial", 12))
status_label.grid(row=2, column=1, pady=5)

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
for i in range(3):
    root.grid_rowconfigure(i, weight=1)
    root.grid_columnconfigure(i, weight=1)

# Start the Tkinter event loop
root.mainloop()