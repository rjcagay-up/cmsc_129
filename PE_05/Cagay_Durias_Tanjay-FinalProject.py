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
        self.error_statements = ''
        
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
        
        # var_presence = [variable for variable, datatype in self.variables if variable == word]
        
        # if(len(var_presence) == 0):
        #     return False
        
        for variable in self.variables:
            if(word == variable[0] and variable[1] != 'null'):
                return True
        
        return False
    
    def variableTYPEcheck(self, word):
        vari = dict(self.variables)
        
        if word in vari:
            return vari[word]
        else:
            return None

    def analyze(self, code):
        self.tokens = []
        self.variables = set()

        lines = code.split('\n')

        for i, line in enumerate(lines, start=1):
            words = line.split()
            token_list = []
            for word in words:
                token = self.get_token(word)
                # self.tokens.append((token, word, i))
                
                if token == 'IDENT' and self.itISvariable(word) == False:
                    prev = self.tokens[-1]
                    self.tokens.append((token, word, i))
                    
                    if (self.itISdatatype(prev[0])):
                        self.variables.add((word, prev[0]))
                        
                        # Camyl code
                        if prev[0] == 'INT':
                            token_stream.append((token, word, i, 0))
                        else:
                            token_stream.append((token, word, i, ''))
                        # Camyl code
                            
                    else:
                        self.variables.add((word, 'null'))
                        
                elif token == 'IDENT' and self.itISvariable(word) == True:
                    self.tokens.append((token, word, i))
                    for tok in token_stream:
                        if isinstance(tok, tuple) and tok[0] == 'IDENT' and tok[1] == word:
                            token_stream.append(tok)
                            break
                else:
                    self.tokens.append((token, word, i))
                    token_stream.append((token, word, i))

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
        # self.error_statements = ''
        
        # errlex = [(word,line) for token, word, line in self.tokens if token == 'ERR_LEX']
        # self.error_statements = "\nUnknown words detected:"
        
        # for error in errlex:
        #     self.error_statements += "\nUnknown word '" + str(error[0]) + "' detected at line " + str(error[1])
            
        error_indices = [i for i, token in enumerate(self.tokens) if token[0] == 'ERR_LEX']
        error_messages = [f"Unknown word '{token[1]}' detected at line {token[2]}" for token in self.tokens if token[0] == 'ERR_LEX']

        self.error_statements = "Unknown words detected:\n"
        for i, index in enumerate(error_indices):
            self.error_statements += f"Error {i + 1} - {error_messages[i]}\n"
    
class SyntaxAnalyzer:
    def __init__(self):
        # Production rules of the IOL PL
        self.iol_prod = [
            ["s", "IOL stmts LOI"],
            ["stmts", "stmt stmts"],
            ["stmts", "e"],
            ["stmt", "var"],
            ["stmt", "asn"],
            ["stmt", "out"],
            ["stmt", "NEWLN"],
            ["var", "INT IDENT varend"],
            ["var", "STR IDENT varend"],
            ["varend", "IS INT_LIT"],
            ["varend", "e"],
            ["asn", "INTO IDENT IS expr"],
            ["asn", "BEG IDENT"],
            ["out", "PRINT expr"],
            ["expr", "ADD expr expr"],
            ["expr", "SUB expr expr"],
            ["expr", "MULT expr expr"],
            ["expr", "DIV expr expr"],
            ["expr", "MOD expr expr"],
            ["expr", "IDENT"],
            ["expr", "INT_LIT"],
            ["stmt", "expr"]
        ]
        
        # List of terminals and parsing table of the IOL PL
        self.iol_ptbl = {
            "terminals": [
                "IOL",
                "INT",
                "STR",
                "INTO",
                "BEG",
                "PRINT",
                "NEWLN",
                "LOI",
                "IS",
                "ADD",
                "SUB",
                "MULT",
                "DIV",
                "MOD",
                "IDENT",
                "INT_LIT",
                "$"
            ],
            
            
            # This is the parse table of the given language, the inputs follows (from left to right) as the list above (from top to bottom)
            "s": [1, "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
            "stmts": ["", 2, 2, 2, 2, 2, 2, 3, "", 22, 22, 22, 22, 22, "", ""],
            "stmt": ["", 4, 4, 5, 5, 6, 7, "", "", "", "", "", "", "", "", ""],
            "var": ["", 8, 9, "", "", "", "", "", "", "", "", "", "", "", "", ""],
            "varend": ["", 11, 11, 11, 11, 11, 11, 11, 10, "", "", "", "", "", "", ""],
            "asn": ["", "", "", 12, 13, "", "", "", "", "", "", "", "", "", "", ""],
            "out": ["", "", "", "", "", 14, "", "", "", "", "", "", "", "", "", ""],
            "expr": ["", "", "", "", "", "", "", "", "", 15, 16, 17, 18, 19, 20, 21],
        }

    def analyze(self, tokens, error_statements, lexical_analyzer):
        
        # Initializing needed variables
        declared_vars = list()
        statement = list()
        semantic_case = None
        last_ident_token = None
        
        input_buffer = tokens
        input_buffer.append(('$','$',None))
        
        # Initializing stack with the initial state and '$'
        stack = [self.iol_prod[0][0],'$']
        
        # Initialize current production id to initial state
        current_production_id = 1
        
        # Camyl code
        index = 0
        # Camyl code
        
        # print initial stack and input buffer
        # print('Initial Stack:', stack)
        # print('Initial Input Buffer: [', ', '.join(token for token, _, _ in input_buffer), ']\n')
        
        # Goes through each of the tokens in the input buffer until nothing is left or an error occurs
        while len(input_buffer) != 0:
            
            if input_buffer[0][0] == 'ERR_LEX':
                input_buffer.pop(0)
                continue
        
            # Checks if current token in the input buffer exists as possible input  
            if not input_buffer[0][0] in self.iol_ptbl["terminals"]:
                error_statements += f"\n'{input_buffer[0][0]}' does not exist in the parse table\n" # Make error statement
                update_status(error_statements)
                return
            # if token exists, then get index for reference
            else:
                token_index = self.iol_ptbl["terminals"].index(input_buffer[0][0])
            
            # if first element on the stack is a state, then refer to parse table if state id exists for the given token
            if stack[0] in self.iol_ptbl and stack[0] != 'terminals':
                
                # takes content in given cell in the parse table
                parse_cell = self.iol_ptbl[stack[0]][token_index]
                
                # If cell is not empty, replace current production id with state id in the cell
                if parse_cell != '':
                    current_production_id = parse_cell
                    
                    # Camyl code
                    execution_order.append(stack.pop(0))
                    # Camyl code
                    
                    # replace state with appropriate production according to the state id in the parse table
                    production_by_id = self.iol_prod[current_production_id-1][1].split()
                    
                    # insert production atop the stack
                    count = 0
                    for production_element in production_by_id:
                        # if element is 'e' do not add anything
                        if production_element == 'e':
                            continue
                        else:
                            stack.insert(count, production_element)
                            count += 1
                # if cell is empty, then input string is INVALID
                else:
                    error_statements += f"Error in line '{input_buffer[0][2]}': Invalid literal"
                    update_status(error_statements)
                    return
  
            # if first element of the stack is not a state, match with the first element of the input buffer                
            else:
                # if they match, pop both elements from the stack and input buffer and continue
                if stack[0] == input_buffer[0][0]:
                    
                    # Camyl code
                    top = stack.pop(0)
                    if top == 'INT_LIT' or top == 'IDENT':
                        execution_order.append(token_stream[index])
                    else:
                        execution_order.append(top)
                    
                    popped_token = input_buffer.pop(0)
                    index += 1
                    # Camyl code
                    
                    # Depending on the scenario, different "if statements" are taken into account
                    # error_statements is used to store errors encountered by the lexical analyzer
                    match popped_token[0]:
                        case "INT" | "STR":
                            semantic_case = "DECLARE"
                            statement.clear()
                            statement.append(popped_token[1])
                        case "INTO":
                            semantic_case = "INTO"
                            statement.clear()
                            statement.append(popped_token[1])
                        case "ADD" | "SUB" | "MULT" | "DIV" | "MOD":
                            semantic_case = "MATH"
                            statement.append(popped_token[1])
                            status = last_ident_token is None
            
                            if status == False:
                                if last_ident_token[1] in declared_vars:
                                    if semantic_case == "IS" and lexical_analyzer.variableTYPEcheck(last_ident_token[1]) != "INT":
                                        error_statements += f"Type error '{' '.join(statement)}' in line '{popped_token[2]}' '{last_ident_token[1]} 'is of type '{lexical_analyzer.variableTYPEcheck(last_ident_token[1])}'\n"
                                        semantic_case = None
                        case "IS":
                            semantic_case = "IS"
                            statement.append(popped_token[1])
                        case "IDENT":
                            statement.append(popped_token[1])
                            if semantic_case == "DECLARE":
                                if popped_token[1] in declared_vars:
                                    error_statements += f"Duplicate variable declaration '{popped_token[1]}' in line '{popped_token[2]}'\n"
                                else:
                                    declared_vars.append(popped_token[1])
                                semantic_case = None
                            elif popped_token[1] not in declared_vars:
                                error_statements += f"Undefined variable '{popped_token[1]}' in line '{popped_token[2]}'\n"
                            elif semantic_case == "IS":
                                if lexical_analyzer.variableTYPEcheck(popped_token[1]) != lexical_analyzer.variableTYPEcheck(last_ident_token[0]):
                                    error_statements += f"Type error '{" ".join(statement)}' in line '{popped_token[2]}' '{last_ident_token[1]}' is of type '{lexical_analyzer.variableTYPEcheck(last_ident_token[1])}'\n"
                                semantic_case = None
                            elif semantic_case == "MATH":
                                
                                if lexical_analyzer.variableTYPEcheck(popped_token[1]) != "INT":
                                    error_statements += f"Type error '{" ".join(statement)}' in line '{popped_token[2]}' '{popped_token[1]}' is of type '{lexical_analyzer.variableTYPEcheck(last_ident_token[1])}'\n"
                                    semantic_case = None
                            last_ident_token = popped_token
                        case "INT_LIT":
                            statement.append(popped_token[1])
                            status = last_ident_token is None
            
                            if status == False:
                                if last_ident_token[1] in declared_vars:
                                    if semantic_case == "IS" and lexical_analyzer.variableTYPEcheck(last_ident_token[1]) != "INT":
                                        error_statements += f"Type error '{' '.join(statement)}' in line '{popped_token[2]}' '{last_ident_token[1]} 'is of type '{lexical_analyzer.variableTYPEcheck(last_ident_token[1])}'\n"
                                        semantic_case = None
                        case _:
                            statement.clear()
                            statement.append(popped_token[1])
                            semantic_case = None                           
                            
                # if they do not match, then input string is INVALID
                else:
                    error_statements += f"Error in line '{input_buffer[0][2]}': Expected syntax is:\n'{' '.join(self.iol_prod[current_production_id-1][1].split())}'\n"
                    update_status(error_statements)
                    return

        if error_statements:
            update_status(error_statements)
        else:
            update_status("The provided code is syntax valid!\n")
        
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
    
    print(tokenized_code)

    if 'ERR_LEX' in tokenized_code:
        lexical_analyzer.show_errlex()
    else:
        update_status("Code tokenized successfully without errors")
    
    compiled = True
    
    display_variables(lexical_analyzer.variables)
    
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
        
    # After compilation, syntax analysis
    
    syntax_analyzer = SyntaxAnalyzer()
    syntax_analyzer.analyze(lexical_analyzer.tokens, lexical_analyzer.error_statements, lexical_analyzer)

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
        execute(execution_order)
        

def display_variables(variables):
    table.delete(1.0, tk.END)
    table.insert(tk.END, "Variables Table:\n")
    for variable, v_type in variables:
        table.insert(tk.END, f"Variable: {variable}, Type: {v_type}\n")

def update_status(message):
    status.config(text=f"Status: {message}", wraplength=500)


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
        update_line_numbers()  # Call the function to update line numbers
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
def update_line_numbers(event=None):
    global linenum0

    line_num.delete("1.0", tk.END)  # Clear previous line numbers
    line_num.insert(tk.END, "1\n")

    # Get the number of lines in the editor
    num_lines = int(editor.index(tk.END).split('.')[0])

    for i in range(2, num_lines + 1):
        line_num.insert(tk.END, f"{i}\n")

    # Update linenum0 to the new number of lines
    linenum0 = num_lines

    # Adjust the yview to synchronize scrolling
    on_editor_scroll()


# Add the function to update line numbers on editor scroll
def on_editor_scroll(*args):
    # Set the yview of the line numbers to match the text editor's yview
    line_num.yview_moveto(editor.yview()[0])


# Recursive function for program execution
def execute(order):
    stack_top = order[0]
    
    while stack_top != '$':
        if stack_top == "var": # if variable is defined
            order.pop(0)            # pops var
            order.pop(0)            # pops INT or STR

            ident = list(order[0])  # takes the IDENT token 
            identName = ident[1]    # gets lexeme of IDENT token
            val = execute(order)    # gets value to be defined on IDENT

            ident[3] = val              # sets IDENT value
            order[0] = tuple(ident)
            
            order = update_tkn(order,identName,val) # updates IDENT token value
            
            order.pop(0)    # pops IDENT token
            order.pop(0)    # pops varend
            
            if order[0] == 'IS': #if variable definition is INT IDENT IS value
                order.pop(0)
                val = execute(order)
                # print(f"val: {val}")
                
                order = update_tkn(order,identName,val)
                
                order.pop(0)
            
            stack_top = order[0]    # Reinitializes stack_top
        elif stack_top == 'out':
            order.pop(0)
            order.pop(0)
            expr = execute(order)
            print(f"Expr out: {expr}")

            update_status(f" The result of the production is {expr}.")

            order.pop(0)
            stack_top = order[0]
        elif stack_top == 'asn':
            order.pop(0) # pops asn
            
            if order[0] == 'INTO':
                order.pop(0) # pop INTO
                ident = list(order[0])
                identName = ident[1]
                
                order.pop(0) # pop IDENT token
                order.pop(0) # pop IS
                
                expr = execute(order)
                
                order = update_tkn(order,identName,expr)
                        
                order.pop(0)
                stack_top = order[0]

            elif order[0] == 'BEG':
                order.pop(0)  # pop BEG

                ident = list(order[0])
                identName = ident[1]
                
                # Create a Tkinter window
                window = tk.Toplevel()
                window.title("User Input")

                # Initialize an input variable
                window.user_input = ""

                # Create an entry widget for user input
                entry = tk.Entry(window)
                entry.pack(pady=10)

                # Create a button to submit the input
                submit_button = tk.Button(window, text="Insert", command=lambda: get_user_input(window, entry.get()))
                submit_button.pack()

                # Start the Tkinter main loop
                window.wait_window(window)

                # Update the order with the user input
                order = update_tkn(order, identName, window.user_input)
                order.pop(0)
                stack_top = order[0]
        #    
        elif stack_top == 'expr':
            order.pop(0)
            expr = execute(order)
            return expr
        elif stack_top == 'NEWLN':
            print("\n")
            
            order.pop(0)
            stack_top = order[0]

        # Mathematical Operations
        elif stack_top == 'ADD': # Addtion
            order.pop(0)
            expr1 = execute(order)
            order.pop(0)
            if expr1 is False:
                return False

            expr2 = execute(order)
            order.pop(0)
            if expr2 is False:
                return False
            
            return expr1 + expr2
        elif stack_top == 'SUB': #Subtraction
            order.pop(0)
            expr1 = execute(order)
            order.pop(0)
            if expr1 is False:
                return False

            expr2 = execute(order)
            order.pop(0)
            if expr2 is False:
                return False
            return expr1 - expr2
        elif stack_top == 'MULT': #Multiplication
            order.pop(0)
            expr1 = execute(order)
            order.pop(0)
            if expr1 is False:
                return False

            expr2 = execute(order)
            order.pop(0)
            if expr2 is False:
                return False
            return expr1 * expr2
        elif stack_top == 'DIV': #Division
            order.pop(0)
            expr1 = execute(order)
            order.pop(0)
            if expr1 is False:
                return False

            expr2 = execute(order)
            order.pop(0)
            if expr2 is False:
                return False
            elif expr2 == 0:
                return False
            
            quotient = expr1 / expr2
            if isinstance(quotient,float):
                return round(quotient)
            else:
                return quotient
        

        elif stack_top[0] == 'INT_LIT':
            return int(stack_top[1]) 
        elif stack_top[0] == 'IDENT':
            return int(stack_top[3]) 
        else:
            # print(stack_top)
            order.pop(0)
            stack_top = order[0]

    # print(f"h: {order}")

def update_tkn(order,identName,val):
    for i, tok in enumerate(order):
        if isinstance(tok, tuple) and tok[0] == 'IDENT' and tok[1] == identName:
            token = list(tok)
            token[3] = val
            order[i] = tuple(token)
    return order

def get_user_input(window, entry):
    window.user_input = entry
    window.destroy()
    
# GUI setup
root = tk.Tk()
root.title("PL Compiler")
root.configure(bg="yellow")
toolbar = tk.Frame(root, bg="pink")
toolbar.pack(fill=tk.X)

# create a toplevel menu  
menubar = tk.Menu(root)
# Camyl code
execution_order = []
token_stream = []
# Camyl code

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

menubar.add_command(label="Execute (F12)", command=execute_code, accelerator="F12")

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

# Main UI components
main_frame = tk.Frame(root, bg="yellow")
main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Editor section
editor_frame = tk.Canvas(main_frame)
editor_frame.grid(row=1, column=1, sticky="nsew")

# Editor label outside the editor_frame
editor_label = tk.Label(main_frame, text="Editor", font=("Helvetica", 14), bg="yellow")
editor_label.grid(row=0, column=1, sticky="w")  # Highlighted change

editor = ScrolledText(editor_frame, wrap=tk.WORD, font=("Courier New", 12))
editor.pack(fill=tk.BOTH, expand=True)
editor.config(state=tk.DISABLED)  # Disable the editor initially

# Bind the editor's scrollbar drag event to update line numbers
editor.vbar.bind("<B1-Motion>", on_editor_scroll)

# Bind the yscroll command of the editor's scrollbar to update line numbers
editor.vbar.config(command=on_editor_scroll)

# Line Numbers section
line_frame = tk.Canvas(main_frame, width=2, bg="lightgrey")
line_frame.grid(row=1, column=0, sticky="nsew")

line_num = ScrolledText(line_frame, wrap=tk.WORD, font=("Courier New", 12), width=2, takefocus=0)
line_num.pack(fill=tk.BOTH, expand=True)

# Disable the y-scrollbar of line_num
line_num.vbar.configure(command=line_num.yview)
line_num.vbar.forget()

# Bind the <Key> and <KeyRelease> events to update line numbers
editor.bind("<Key>", update_line_numbers)
editor.bind("<KeyRelease>", update_line_numbers)

# Bind the editor's scrolling event to update line numbers
editor.bind("<Configure>", lambda event: update_line_numbers())
editor.bind("<MouseWheel>", lambda event: update_line_numbers())
editor.bind("<Button-4>", lambda event: update_line_numbers())
editor.bind("<Button-5>", lambda event: update_line_numbers())


# Initial population of line numbers
update_line_numbers()

# Status bar
status = tk.Label(main_frame, text="Status: Create new file or open file to begin", bd=1, relief=tk.SUNKEN, anchor=tk.W, height=5, font=("Helvetica", 12), bg="pink")
status.grid(row=2, column=0, columnspan=2, sticky="nsew")

# Variables table section
table_frame = tk.Frame(main_frame, bg="yellow")
table_frame.grid(row=0, column=2, rowspan=3, sticky="nsew")

table_label = tk.Label(table_frame, text="Variables Table", font=("Helvetica", 14), bg="yellow")
table_label.pack()

table = ScrolledText(table_frame, wrap=tk.WORD)
table.pack(fill=tk.BOTH, expand=True)

# Set column and row weights to make them resize properly
main_frame.columnconfigure(0, weight=0)
main_frame.columnconfigure(1, weight=1)
main_frame.columnconfigure(2, weight=1)
main_frame.rowconfigure(0, weight=1)
main_frame.rowconfigure(1, weight=1)



root.mainloop()


