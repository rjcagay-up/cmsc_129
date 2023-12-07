import tkinter as tk
import os
from tkinter import filedialog
from tkinter.scrolledtext import ScrolledText
from tkinter import messagebox
from tkinter import *  

editor_path = None  # Variable to track the file path associated with the editor content
# Define a variable to track whether a new file has been created
new_file_created = False

class LexicalAnalyzer:
    def __init__(self):
        self.keywords = ('IOL', 'LOI', 'INTO', 'IS', 'BEG', 'PRINT', 'ADD', 'SUB', 'MULT', 'DIV', 'MOD', 'NEWLN')
        self.datatypes = ('INT', 'STR')
        self.tokens = []
        self.variables = set()
        
    def itISkeyword(self, word):
        if word in self.keywords:
            return True
        return False
    
    def itISdatatype(self, word):
        if word in self.datatypes:
            return True
        return False
    
    def itISvariable(self, word):
        
        if(len(self.variables) == 0):
            return False
        
        var_presence = [variable for variable, datatype in self.variables if variable == word]
        
        if(len(var_presence) == 0):
            return False
        
        return True

    def analyze(self, code):
        self.tokens = []
        self.variables = set()

        lines = code.split('\n')

        for i, line in enumerate(lines, start=1):
            words = line.split()
            for word in words:
                token = self.get_token(word)
                self.tokens.append((token, word, i))
                
                if token == 'IDENT' and not(self.itISvariable(word)) and len(self.tokens) != 1:
                    
                    prev = self.tokens[len(self.tokens)-2]
                        
                    if (self.itISdatatype(prev[0])):
                        self.variables.add((word, prev[0]))
                    else:
                        self.variables.add((word, 'null'))
                        
                elif token == 'IDENT' and len(self.tokens) == 1:
                    self.variables.add((word, 'null'))

    def get_token(self, word):
        if (self.itISkeyword(word)):
            return word
        elif(self.itISdatatype(word)):
            return word
        elif word.isdigit():
            return 'INT_LIT'
        elif word.isidentifier():
            return 'IDENT'
        else:
            return 'ERR_LEX'
        
    def show_errlex(self):
        errlex = [(word,line) for token, word, line in self.tokens if token == 'ERR_LEX']
        error_message = "Unknown words detected:"
        
        for error in errlex:
            error_message += "\nUnknown word '" + str(error[0]) + "' detected at line " + str(error[1])
            
        return error_message
        
tokenized_window = None  # Global variable to track the tokenized window
tokenized_code = None
compiled = False  # Variable to track compilation status

# Function for Compiling the code
def compile_code(event=None):
    global tokenized_code, compiled

    code = editor.get("1.0", tk.END)

    if editor.edit_modified():  # Check if the editor content has been modified
        response = messagebox.askyesnocancel("Unsaved Changes", "The code has been modified. Do you want to save before compiling?")

        if response is True:  # User chooses to save
            save_file()
        elif response is False:  # User chooses not to save
            pass
        else:  # User cancels compilation
            return

    # Check if there's a filename already
    if editor_path:
        with open(editor_path, 'w') as file:
            file.write(code)
    else:
        save_file()  # If no filename, prompt for save

    lexical_analyzer = LexicalAnalyzer()
    lexical_analyzer.analyze(code)

    tokenized_code = ' '.join(token for token, _, _ in lexical_analyzer.tokens)

    update_status("Code tokenized successfully")
    compiled = True

    if 'ERR_LEX' in tokenized_code:
         # Display where and what the lexical errors are
        error_indices = [i for i, token in enumerate(lexical_analyzer.tokens) if token[0] == 'ERR_LEX']
        error_messages = [f"Unknown word '{token[1]}' detected at line {token[2]}" for token in lexical_analyzer.tokens if token[0] == 'ERR_LEX']

        error_message = "Lexical Errors:\n"
        for i, index in enumerate(error_indices):
            error_message += f"Error {i + 1} - {error_messages[i]}\n"

        update_status(error_message)
        print(f"{error_message}")
    else:
        update_status("Code tokenized successfully")
    
    compiled = True
    # Save the compiled code to a .tkn file
    if editor_path:
        # Extract the file path without the extension and add .tkn
        file_base = editor_path[:editor_path.rfind('.')]
        tkn_path = file_base + ".tkn"

        with open(tkn_path, 'w') as tkn_file:
            tkn_file.write(tokenized_code)

        print(f"Compiled code saved as: {tkn_path}")
    else:
        print("No filename to save the compiled code.")

    display_variables(lexical_analyzer.variables)

# Function for showing the tokenized code
def show_tokenized_code(event=None):
    global tokenized_window, tokenized_code
    if not compiled:  # Check if code is compiled
        update_status("Compile the code first before showing tokenized code.")
    elif tokenized_window and tokenized_window.winfo_exists():
        update_status("Close the existing tokenized window before compiling again.")
    else:
        tokenized_window = tk.Toplevel(root)
        tokenized_window.title("Tokenized Code")
        tokenized_output = ScrolledText(tokenized_window, wrap=tk.WORD)
        tokenized_output.pack(fill=tk.BOTH, expand=True)
        tokenized_output.insert(tk.END, tokenized_code)

# Function for Executing the code
def execute_code(event=None):
    if not compiled:
        update_status("Compile the code first before executing.")
    else:
        print("Execute Code")

def display_variables(variables):
    table.delete(1.0, tk.END)
    table.insert(tk.END, "Variables Table:\n")
    for variable, v_type in variables:
        table.insert(tk.END, f"Variable: {variable}, Type: {v_type}\n")

def update_status(message):
    status.config(text=f"Status: {message}")


# Function to open a PL file (.iol)
def open_file(event=None):
    global editor_path, new_file_created

    if new_file_created:
        response = messagebox.askyesnocancel("Open File", "Opening a new file will discard the unsaved changes. Do you want to proceed?")
        if response is None or response is False:
            return

    file_path = filedialog.askopenfilename(filetypes=[("PL Files", "*.iol")])
    if file_path:
        with open(file_path, 'r') as file:
            editor.config(state=tk.NORMAL)  # Enable editing
            editor.delete(1.0, tk.END)
            editor.insert(tk.END, file.read())
        update_status(f"File Opened: {file_path}")
        editor_path = file_path
        root.title(f"PL Compiler - {os.path.basename(file_path)}")
        new_file_created = False  # Reset new_file_created


def new_file(event=None):
    global new_file_created, editor_path

    if new_file_created:
        response = messagebox.askyesnocancel("New File", "Do you want to create a new file? Any unsaved changes will be lost.")
        if response is None or response is False:
            return

    editor.config(state=tk.NORMAL)  # Enable the editor
    editor.delete(1.0, tk.END)
    new_file_created = True

     # Get the directory of the currently executing script
    current_directory = os.path.dirname(os.path.abspath(__file__))

    # Set the editor_path to the new_default.iol file in the current directory
    editor_path = os.path.join(current_directory, "new_default.iol")

    # Create the new_default.iol file
    with open(editor_path, 'w') as new_file:
        new_file.write("Your new PL code here.")

    # Update the window title with the new file name
    root.title(f"PL Compiler - {os.path.basename(editor_path)}")

    # Update the status display with the file name
    update_status("New file created")

    print(f"Editor Path: {editor_path}")

def save_file(event=None):
    global editor_path

    if editor_path:
        with open(editor_path, 'w') as file:
            file.write(editor.get("1.0", tk.END))
        update_status(f"File Saved: {editor_path}")
    else:
        save_file_as()

def save_file_as(event=None):
    file_path = filedialog.asksaveasfilename(defaultextension=".iol", filetypes=[("PL Files", "*.iol")])
    if file_path:
        if not file_path.endswith(".iol"):  # Ensure the .iol extension
            file_path += ".iol"
        with open(file_path, 'w') as file:
            file.write(editor.get("1.0", tk.END))
        editor_path = file_path
        update_status(f"File Saved: {file_path}")
        root.title(f"PL Compiler - {file_path}")

def close_file(event=None):
    global new_file_created, editor_path

    if new_file_created:
        response = messagebox.askyesnocancel("Close File", "Do you want to close the current file? Any unsaved changes will be lost.")
        if response is None or response is False:
            return

    if editor_path:
        editor.delete(1.0, tk.END)
        editor_path = None
        update_status("File Closed")
        new_file_created = True
        root.title("PL Compiler")

# GUI setup
root = tk.Tk()
root.title("PL Compiler")
root.configure(bg="yellow")
toolbar = tk.Frame(root, bg="pink")
toolbar.pack(fill=tk.X)

# Main UI components
main_frame = tk.Frame(root, bg="yellow")
main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# create a toplevel menu  
menubar = tk.Menu(root)

file = tk.Menu(menubar, tearoff=0)
file.add_command(label="New (ctrl+n)", command=new_file, accelerator="ctrl+n")
file.add_command(label="Open (ctrl+o)", command=open_file, accelerator="ctrl+o")
file.add_command(label="Save (ctrl+s)", command=save_file, accelerator="ctrl+s")
file.add_command(label="Save as... (ctrl+a)",command=save_file_as, accelerator="ctrl+a")
file.add_command(label="Close (ctrl+q)", command=close_file, accelerator="ctrl+q")
file.add_separator()
menubar.add_cascade(label="File", menu=file)

compile = tk.Menu(menubar, tearoff=0)
compile.add_command(label="Compile Code (F9)", command=compile_code, accelerator="F9")
compile.add_command(label="Show Tokenized Code (F10)", command=show_tokenized_code, accelerator="F10")
compile.add_separator()
menubar.add_cascade(label="Compile", menu=compile, accelerator="F8")

menubar.add_command(label="Execute", command=execute_code, accelerator="F12")

root.bind('<Control-n>', new_file)
root.bind('<Control-o>', open_file)
root.bind('<Control-s>', save_file)
root.bind('<Control-a>', save_file_as)
root.bind('<Control-q>', close_file)
root.bind('<F9>', compile_code)
root.bind('<F10>', show_tokenized_code)
root.bind('<F12>', execute_code)

# display the menu  
root.config(menu=menubar)

# Editor section
editor_frame = tk.Frame(main_frame, bg="yellow")
editor_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

editor_label = tk.Label(editor_frame, text="Editor", font=("Helvetica", 14), bg="yellow")
editor_label.pack()

editor = ScrolledText(editor_frame, wrap=tk.WORD)
editor.pack(fill=tk.BOTH, expand=True)
editor.config(state=tk.DISABLED)  # Disable the editor initially

# Variables table section
table_frame = tk.Frame(main_frame, bg="yellow")
table_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

table_label = tk.Label(table_frame, text="Variables Table", font=("Helvetica", 14), bg="yellow")
table_label.pack()

table = ScrolledText(table_frame, wrap=tk.WORD)
table.pack(fill=tk.BOTH, expand=True)

# Status bar
status = tk.Label(root, text="Status: Create new file or open file to begin", bd=1, relief=tk.SUNKEN, anchor=tk.W, height=5, font=("Helvetica", 12), bg="pink")
status.pack(side=tk.BOTTOM, fill=tk.X)



root.mainloop()