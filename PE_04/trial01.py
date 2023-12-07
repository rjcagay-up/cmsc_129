import tkinter as tk
from tkinter import scrolledtext, Menu, filedialog, messagebox

class SimpleEditor:
    def __init__(self, master):
        self.master = master
        self.master.title("Simple Text Editor")

        self.file_path = ""
        self.text_editor = None
        self.code_output = None

        self.setup_menu()
        self.setup_text_editor()
        self.setup_code_output()

    def setup_menu(self):
        menu_bar = Menu(self.master)

        file_menu = Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_command(label="Save As", command=self.save_file_as)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.exit_program)

        menu_bar.add_cascade(label="File", menu=file_menu)
        self.master.config(menu=menu_bar)

    def setup_text_editor(self):
        line_numbers = scrolledtext.ScrolledText(self.master, width=4, height=30, wrap=tk.NONE, bg="lightgray", state="disabled")
        line_numbers.grid(row=0, column=0, sticky="nsew")
        line_numbers.bind("<Configure>", self.sync_scroll)

        self.text_editor = scrolledtext.ScrolledText(self.master, wrap=tk.WORD, width=80, height=30)
        self.text_editor.grid(row=0, column=1, sticky="nsew")
        self.text_editor.bind("<Configure>", self.sync_scroll)

    def setup_code_output(self):
        self.code_output = scrolledtext.ScrolledText(self.master, height=10, borderwidth=2, relief="sunken")
        self.code_output.grid(row=1, column=0, columnspan=2, sticky='nsew')

    def sync_scroll(self, event=None):
        yscroll = self.text_editor.yview()[0]
        self.text_editor.yview_moveto(yscroll)

    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("All files", "*.*")])
        if file_path:
            with open(file_path, 'r') as file:
                content = file.read()
                self.text_editor.delete('1.0', tk.END)
                self.text_editor.insert('1.0', content)
                self.file_path = file_path

    def save_file(self):
        if self.file_path:
            with open(self.file_path, 'w') as file:
                file.write(self.text_editor.get('1.0', tk.END))
        else:
            self.save_file_as()

    def save_file_as(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All files", "*.*")])
        if file_path:
            with open(file_path, 'w') as file:
                file.write(self.text_editor.get('1.0', tk.END))
            self.file_path = file_path

    def exit_program(self):
        self.master.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    editor = SimpleEditor(root)
    root.mainloop()
