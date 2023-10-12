import tkinter as tk
from tkinter import filedialog
from tkinter.scrolledtext import ScrolledText

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

    def analyze(self, code):
        self.tokens = []
        self.variables = set()

        lines = code.split('\n')

        for i, line in enumerate(lines, start=1):
            words = line.split()
            for word in words:
                token = self.get_token(word)
                self.tokens.append((token, word, i))
                if token == 'IDENT' and len(self.tokens) != 1:
                    prev = self.tokens[len(self.tokens)-2]
                    if (self.itISdatatype(prev[0])):
                        self.variables.add((word, prev[0]))
                    else:
                        self.variables.add((word, 'null'))
                elif token == 'IDENT':
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
            
def show_tokenized_code(event=None):
    code = editor.get("1.0", tk.END)

    lexical_analyzer = LexicalAnalyzer()
    lexical_analyzer.analyze(code)

    output.delete(1.0, tk.END)

    tokenized_code = ' '.join(token for token, _, _ in lexical_analyzer.tokens)
    output.insert(tk.END, tokenized_code)

    if(tokenized_code.find('ERR_LEX') == -1):
        update_status("Code tokenized successfully")
    else:
        update_status(lexical_analyzer.show_errlex())

    display_variables(lexical_analyzer.variables)

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

# Buttons for file operations
new_button = tk.Button(toolbar, text="New File (Ctrl+N)", command=new_file, font=("Helvetica", 12))
new_button.pack(side=tk.LEFT, padx=5, pady=5)
new_button.bind("<Control-n>", new_file)

open_button = tk.Button(toolbar, text="Open File (Ctrl+O)", command=open_file, font=("Helvetica", 12))
open_button.pack(side=tk.LEFT, padx=5, pady=5)
open_button.bind("<Control-o>", open_file)

save_button = tk.Button(toolbar, text="Save (Ctrl+S)", command=save_file, font=("Helvetica", 12))
save_button.pack(side=tk.LEFT, padx=5, pady=5)
save_button.bind("<Control-s>", save_file)

tokenize_button = tk.Button(toolbar, text="Compile Code (Ctrl+T)", command=show_tokenized_code, font=("Helvetica", 12))
tokenize_button.pack(side=tk.LEFT, padx=5, pady=5)
tokenize_button.bind("<Control-t>", show_tokenized_code)

# Main UI components
main_frame = tk.Frame(root, bg="yellow")
main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Editor section
editor_frame = tk.Frame(main_frame, bg="yellow")
editor_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

editor_label = tk.Label(editor_frame, text="Editor", font=("Helvetica", 14), bg="yellow")
editor_label.pack()

editor = ScrolledText(editor_frame, wrap=tk.WORD)
editor.pack(fill=tk.BOTH, expand=True)

# Output section
space_frame = tk.Frame(main_frame, width=20)
space_frame.pack(side=tk.LEFT)

output_frame = tk.Frame(main_frame, bg="yellow")
output_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

output_label = tk.Label(output_frame, text="Tokenized Code", font=("Helvetica", 14), bg="yellow")
output_label.pack()

output = ScrolledText(output_frame, wrap=tk.WORD)
output.pack(fill=tk.BOTH, expand=True)

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
