import tkinter as tk
from tkinter import filedialog
from tkinter.scrolledtext import ScrolledText
from tkinter import messagebox
from tkinter import *  

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

    lexical_analyzer = LexicalAnalyzer()
    lexical_analyzer.analyze(code)

    tokenized_code = ' '.join(token for token, _, _ in lexical_analyzer.tokens)

    if tokenized_code.find('ERR_LEX') == -1:
        update_status("Code tokenized successfully")
        compiled = True  # Mark as compiled
    else:
        update_status(lexical_analyzer.show_errlex())
        compiled = False

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

def open_file(event=None):
    file_path = filedialog.askopenfilename(filetypes=[("Custom Files", "*.iol")])
    if file_path:
        with open(file_path, 'r') as file:
            editor.delete(1.0, tk.END)
            editor.insert(tk.END, file.read())
        update_status(f"File Opened: {file_path}")

def save_file(event=None):
    file_path = filedialog.asksaveasfilename(defaultextension=".iol", filetypes=[("Custom Files", "*.iol")])
    if file_path:
        with open(file_path, 'w') as file:
            file.write(editor.get("1.0", tk.END))
        update_status(f"File Saved as: {file_path}")

def new_file(event=None):
    editor.delete(1.0, tk.END)
    update_status("New file created")

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
menubar = Menu(root)  

file = Menu(menubar, tearoff=0)  
file.add_command(label="New", command=new_file)  
file.add_command(label="Open", command=open_file)  
file.add_command(label="Save", command=save_file)  
file.add_command(label="Save as...")  
file.add_command(label="Close")   
file.add_separator()  
menubar.add_cascade(label="File", menu=file)  

compile = Menu(menubar, tearoff=0)
compile.add_command(label="Compile Code", command=compile_code)
compile.add_command(label="Show Tokenized Code", command=show_tokenized_code)
compile.add_separator()
menubar.add_cascade(label="Compile", menu=compile)  

menubar.add_command(label="Execute", command=execute_code)  
  
# display the menu  
root.config(menu=menubar)  

# Editor section
editor_frame = tk.Frame(main_frame, bg="yellow")
editor_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

editor_label = tk.Label(editor_frame, text="Editor", font=("Helvetica", 14), bg="yellow")
editor_label.pack()

editor = ScrolledText(editor_frame, wrap=tk.WORD)
editor.pack(fill=tk.BOTH, expand=True)

# Variables table section
table_frame = tk.Frame(main_frame, bg="yellow")
table_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

table_label = tk.Label(table_frame, text="Variables Table", font=("Helvetica", 14), bg="yellow")
table_label.pack()

table = ScrolledText(table_frame, wrap=tk.WORD)
table.pack(fill=tk.BOTH, expand=True)

# Status bar
status = tk.Label(root, text="Status: Ready", bd=1, relief=tk.SUNKEN, anchor=tk.W, height=5, font=("Helvetica", 12), bg="pink")
status.pack(side=tk.BOTTOM, fill=tk.X)

root.mainloop()
