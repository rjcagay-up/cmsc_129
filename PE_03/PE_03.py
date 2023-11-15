import tkinter as tk
from tkinter import *
from tkinter import filedialog
import os

# Initializing lists for state, production and parse lists
production_list = []
parse_table_list = []
state_list = []

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
    
    # Clear existing production list
    production_list.clear()
    
    # Add headers to the production table
    production_text.insert(tk.END, "ID\t\tNT\t\tP\n")

    # Parse each line and add rows to the table
    for line in file_content.splitlines():
        # Split line based on commas
        line_parts = line.split(',')
        
        production_list.append(line_parts)
        
        # Add cells to the table with borders on all sides
        for part in line_parts:
            production_text.insert(tk.END, f"{part}\t|\t", "border")
        
        # Move to the next line
        production_text.insert(tk.END, "\n")
        
    print('Production List:', production_list, '\n')

# Function to generate a parse table from file content
def generate_ptbl_table(file_content):
    # Clear existing content
    parse_table_text.delete(1.0, tk.END)
    
    # Clear existing state and parse table list
    parse_table_list.clear()
    state_list.clear()

    # Parse each line and add headers to the table based on the first line
    headers = file_content.splitlines()[0].split(',')
    for header in headers:
        parse_table_text.insert(tk.END, f"{header}\t|\t", "border")
    parse_table_text.insert(tk.END, "\n")
    
    parse_table_list.append(headers)

    # Parse each line and add rows to the table
    for line in file_content.splitlines()[1:]:
        # Split line based on commas
        line_parts = line.split(',')
        
        parse_table_list.append(line_parts)
        
        # Add cells to the table with borders on all sides
        for part in line_parts:
            parse_table_text.insert(tk.END, f"{part}\t|\t", "border")
        
        # Move to the next line
        parse_table_text.insert(tk.END, "\n")
    
    print('Parse Table List:', parse_table_list, '\n')
    
    # Takes a list of all states
    for state in parse_table_list[1:]:
        state_list.append(state[0])
        
    print('State List: ', state_list, '\n')

# Function to configure the border style for the production and parse table
def configure_tags():
    production_text.tag_configure("border", borderwidth=1, relief="solid")
    parse_table_text.tag_configure("border", borderwidth=1, relief="solid")

# Function to handle parsing input (placeholder implementation)
def parse_input():
   # Checks if production and parse tree table exist for parsing input string
    if not production_list:
        print("Production File Missing")
        return
    if not parse_table_list:
        print("Parse Tree File Missing")
        return
    
    input_text = input_entry.get()
    # Placeholder: Add your parsing logic here
    # For now, display the input in the status label
    parsing_status_var.set(f"PARSING: {input_text}")
    # Simulating parsing delay (you can replace this with your actual parsing logic)
    root.after(2000, lambda: parsing_status_var.set(""))  # Clear the status after 2000 milliseconds (2 seconds)
    
    # Splits the input text by white space into a list and appends '$' at the end to create the input buffer
    input_buffer = input_text.split()
    input_buffer.append('$')
    
    # Initializing stack with the initial state and '$'
    stack = [production_list[0][1],'$'] 
    
    # Initialize current production id to initial state
    current_production_id = 1
    
    # print initial stack and input buffer
    print('Initial Stack:', stack)
    print('Initial Input Buffer', input_buffer, '\n')
    
    # Goes through each of the tokens in the input buffer until nothing is left or an error occurs
    while len(input_buffer) != 0:
        
        # clears and initializes action string
        action_string = 'No action'
        
        # Checks if current token in the input buffer exists as possible input  
        if not input_buffer[0] in parse_table_list[0][1:]:
            print("\n'", input_buffer[0], "' does not exist in the parse table")
            return
        # if token exists, then get index for reference
        else:
            token_index = parse_table_list[0][1:].index(input_buffer[0])
        
        # if first element on the stack is a state, then refer to parse table if state id exists for the given token
        if stack[0] in state_list:
            # takes content in given cell in the parse table
            parse_cell = parse_table_list[state_list.index(stack[0]) + 1][token_index+1]
            
            # If cell is not empty, replace current production id with state id in the cell
            if parse_cell != '':
                current_production_id = parse_cell
                
                # set action string to substituting state with appropriate production
                action_string = 'Output ' + stack[0] + ' > ' + production_list[int(current_production_id) - 1][2]
                
                # replace state with appropriate production according to the state id in the parse table
                stack.pop(0)
                production_by_id = production_list[int(current_production_id) - 1][2].split(' ')
                
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
                # Di ko sure actually kung tama ning pag state nako
                print("Production is not able to produce given input token")
                print("Input String is INVALID")
                return

        # if first element of the stack is not a state, match with the first element of the input buffer
        else:
            # if they match, pop both elements from the stack and input buffer and continue
            if stack[0] == input_buffer[0]:
                # set action string to matching given token
                action_string = 'Match ' + stack[0]
                
                input_buffer.pop(0)
                stack.pop(0)
            # if they do not match, then input string is INVALID
            else:
                print('\n', stack[0], " and ", input_buffer[0], ' do not match!')
                print("Input String is INVALID")
                return

        # print current stack, input buffer, and action string
        print('Stack:', stack)
        print('Input Buffer', input_buffer)
        print('Action: ', action_string, '\n')

    # if code reaches this point, input string is VALID
    print("Given Input String is VALID")

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
