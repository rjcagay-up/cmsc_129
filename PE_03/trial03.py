import tkinter as tk
from tkinter import filedialog, ttk
import os

# Create the main Tkinter window
root = tk.Tk()
root.title("File Loader and Parser")

# Get the screen width and height
screen_width = root.winfo_screenwidth() - 10
screen_height = root.winfo_screenheight() - 100

# Set the window size to adapt to the screen
root.geometry(f"{screen_width}x{screen_height}+0+0")

# Initializing lists for state, production and parse lists
production_list = []  
parse_table_list = []  
state_list = []

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

def load_and_store_data(file_path, production_list, parse_table_list):
    with open(file_path, 'r', encoding='utf-8') as file:
        file_content = file.read()
        data_array = []

        # Load data into a temporary array
        for row in file_content.splitlines():
            columns = row.split(',')  # Separate columns by commas
            data_array.append(columns)

        # Check if it's a production file and store data in production_list
        if file_path.endswith('.prod'):
            # Clear existing content
            production_list.clear()

            # Parse each line and add rows to production_list
            for line in data_array:
                production_list.append(line)

        elif file_path.endswith('.ptbl'):
            # Clear existing content
            parse_table_list.clear()
            state_list.clear()

            # Parse each line and add rows to parse_table_list
            for line in data_array:
                parse_table_list.append(line)

            # Takes a list of all states
            for state in parse_table_list[1:]:
                state_list.append(state[0])

    return production_list, parse_table_list

def load_files():
    # Separate arrays for production and parse table data
    global production_list  # Update from prod_data to production_list
    global parse_table_list  # Update from _ptbl_data to parse_table_list
    headers = []

    files = filedialog.askopenfilenames(
        title="Select files",
        filetypes=[("All Files", "*.prod; *.ptbl"), ("Production files", "*.prod"), ("Parse Table files", "*.ptbl")]
    )

    for file_path in files:
        if file_path.endswith('.prod'):
            production_list, _ = load_and_store_data(file_path, production_list, [])
            headers = ["ID", "NT", "P"]
            create_table(production_list[1:], headers, production_label, production_tree)
            print(f"{production_list}")
        elif file_path.endswith('.ptbl'):
            _, parse_table_list = load_and_store_data(file_path, [], parse_table_list)
            # Extract headers from the first line of the parse table file
            headers = parse_table_list[0]
            create_table(parse_table_list[1:], headers, parse_table_label, parse_table_tree)
            print(f"{parse_table_list}")

        status_var.set(f"LOADED: {os.path.basename(file_path)}")

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
    
    parsing_status_var.set(f"PARSING: {input_text}")


    # Simulating parsing delay
    root.after(5000, lambda: parsing_status_var.set(""))  # Clear the status after 2000 milliseconds (2 seconds)
    
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

# Create Label for the Production Table
production_label = tk.Label(root, text="Production:", font=("Arial", 14))
production_label.grid(row=0, column=0, padx=2, pady=5)

# Create a Canvas for the production frame and color it pink
production_canvas = tk.Canvas(root, bg="pink", width=800)
production_canvas.grid(row=1, column=0, padx=2, pady=10, sticky="nsew")

# Create a Frame for the production table and its scrollbar
production_frame = tk.Frame(production_canvas, bg="yellow", width=800)
production_frame.grid(row=0, column=0, sticky="nsew")

# Create a Treeview for the production table inside the frame
production_tree = ttk.Treeview(production_frame, height=10, show="headings")
production_tree.grid(row=1, column=1, columnspan=2, sticky="nsew")

# Create a Canvas for the parse frame and color it blue
parse_canvas = tk.Canvas(root, bg="blue", width=500)
parse_canvas.grid(row=1, column=1, pady=5, sticky="nsew")

parse_table_label = tk.Label(root, text="Parse Table:", font=("Arial", 12))
parse_table_label.grid(row=0, column=1, padx=2, pady=5)

# Create a Frame for the parse table
parse_frame = tk.Frame(parse_canvas, bg="yellow")
parse_frame.grid(row=1, column=0, sticky="w")

# Create a Treeview for the parse table inside the frame
parse_table_tree = ttk.Treeview(parse_frame, height=10, show="headings")
parse_table_tree.grid(row=0, column=1, sticky="nsew")

# Create canvas for the load and status
statusLoad_canvas = tk.Canvas(root, bg="red", width=400, height=20)
statusLoad_canvas.grid(row=2, sticky="nsew")

# Create a button for loading files
load_button = tk.Button(root, text="LOAD", command=lambda: [load_files(), configure_tags()], font=("Arial", 14))
load_button.grid(row=2, column=1, pady=10, columnspan=1, sticky="e")

# Create a status label for displaying file loading information
status_var = tk.StringVar()
status_label = tk.Label(statusLoad_canvas, textvariable=status_var, fg="green", font=("Arial", 12))
status_label.grid(row=2, column=0, pady=5, sticky="nsew")

# Bottom row components
input_label = tk.Label(root, text="INPUT:", font=("Arial", 14), bg="pink", fg="black")
input_label.grid(row=3, column=0, padx=1, pady=5, sticky=tk.E)  # Adjusted column position and sticky property

# Create an entry for user input
input_entry = tk.Entry(root, width=20, font=("Arial Unicode MS", 12))
input_entry.grid(row=3, column=1, padx=2, pady=5, columnspan=1, sticky="w")  # Adjusted columnspan

# Create a button for parsing input
parse_button = tk.Button(root, text="PARSE", command=parse_input, font=("Arial", 14), bg="yellow", fg="black")
parse_button.grid(row=3, column=1, padx=10, pady=5)

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
