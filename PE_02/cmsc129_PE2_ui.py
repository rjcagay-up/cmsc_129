# Import necessary modules from the tkinter library
import tkinter as tk
from tkinter import filedialog
from tkinter.scrolledtext import ScrolledText
import re  # Import the re module for regular expressions

# Function to open a file
def open_file():
    # Use the filedialog module to open a file dialog that allows the user to select a file
    file_path = filedialog.askopenfilename(filetypes=[("Python Files", "*.iol")])
    if file_path:  # Check if a file was selected
        # Open the selected file in read mode
        with open(file_path, 'r') as file:
            # Clear the editor (text input) widget and insert the content of the selected file
            editor.delete(1.0, tk.END)
            editor.insert(tk.END, file.read())
        # Update the status bar with a message indicating the opened file
        update_status(f"Opened file: {file_path}")

# Function to save the current content to a file
def save_file():
    # Use the filedialog module to open a file dialog that allows the user to choose where to save the file
    file_path = filedialog.asksaveasfilename(filetypes=[("Python Files", "*.iol")])
    if file_path:  # Check if a file path was chosen
        # Open the selected file in write mode and write the content of the editor widget to it
        with open(file_path, 'w') as file:
            file.write(editor.get("1.0", tk.END))
        # Update the status bar with a message indicating the saved file
        update_status(f"Saved file as: {file_path}")

# Function to create a new file
def new_file():
    # Clear the editor (text input) widget
    editor.delete(1.0, tk.END)
    # Update the status bar with a message indicating the new file
    update_status("New file created")

# Function to show tokenized code in the output placeholder and update the status bar
def show_tokenized_code():
    # Get the content of the editor widget
    code = editor.get("1.0", tk.END)
    
    # Tokenize the code to find variables used (a simple example using regular expressions)
    # Replace this with a more comprehensive tokenizer as per your requirements
    variable_pattern = r'\b[a-zA-Z_][a-zA-Z0-9_]*\b'  # Regular expression to match variables
    variables_used = set(re.findall(variable_pattern, code))
    
    # Update the output widget with the variables used
    output.delete(1.0, tk.END)
    output.insert(tk.END, "Variables Used:\n")
    for var in variables_used:
        output.insert(tk.END, var + '\n')

    # Update the status bar with a message indicating the tokenization
    update_status("Variables Used extracted successfully")

# Function to update the status bar
def update_status(message):
    # Update the text displayed in the status bar with the provided message
    status.config(text=f"Status: {message}")

# Create the main window
root = tk.Tk()
root.title("IDE Compiler")  # Updated title

# Configure the theme (yellow and pink)
root.configure(bg="yellow")

# Create a toolbar with buttons for each function
toolbar = tk.Frame(root, bg="pink")
toolbar.pack(fill=tk.X)

# Create "New File" button and associate it with the new_file function
new_button = tk.Button(toolbar, text="New File", command=new_file, font=("Helvetica", 12))
new_button.pack(side=tk.LEFT, padx=5, pady=5)

# Create "Open File" button and associate it with the open_file function
open_button = tk.Button(toolbar, text="Open File", command=open_file, font=("Helvetica", 12))
open_button.pack(side=tk.LEFT, padx=5, pady=5)

# Create "Save" button and associate it with the save_file function
save_button = tk.Button(toolbar, text="Save", command=save_file, font=("Helvetica", 12))
save_button.pack(side=tk.LEFT, padx=5, pady=5)

# Create "Save As" button and associate it with the save_file function (same as Save for simplicity)
save_as_button = tk.Button(toolbar, text="Save As", command=save_file, font=("Helvetica", 12))
save_as_button.pack(side=tk.LEFT, padx=5, pady=5)

# Create "Show Tokenized Code" button and associate it with the show_tokenized_code function
tokenize_button = tk.Button(toolbar, text="Show Tokenized Code", command=show_tokenized_code, font=("Helvetica", 12))
tokenize_button.pack(side=tk.LEFT, padx=5, pady=5)

# Create the main frame
main_frame = tk.Frame(root, bg="yellow")
main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Create the editor area
editor_frame = tk.Frame(main_frame, bg="yellow")
editor_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Create a label to describe the editor
editor_label = tk.Label(editor_frame, text="Editor", font=("Helvetica", 14), bg="yellow")
editor_label.pack()

# Create a scrolled text widget (text input) for code editing
editor = ScrolledText(editor_frame, wrap=tk.WORD)
editor.pack(fill=tk.BOTH, expand=True)

# Add space between the editor and output
space_frame = tk.Frame(main_frame, width=20)
space_frame.pack(side=tk.LEFT)

# Create the output placeholder
output_frame = tk.Frame(main_frame, bg="yellow")
output_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Create a label to describe the variables used
output_label = tk.Label(output_frame, text="Variables Used", font=("Helvetica", 14), bg="yellow")
output_label.pack()

# Create a scrolled text widget (text display) for showing the tokenized code
output = ScrolledText(output_frame, wrap=tk.WORD)
output.pack(fill=tk.BOTH, expand=True)

# Create the status bar with increased height
status = tk.Label(root, text="Status: Ready", bd=1, relief=tk.SUNKEN, anchor=tk.W, height=2, font=("Helvetica", 12))
status.pack(side=tk.BOTTOM, fill=tk.X)

# Start the main loop to run the tkinter application
root.mainloop()
