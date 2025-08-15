import tkinter as tk
from tkinter import ttk, messagebox
import difflib
import os

class MiniGitGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("MiniGit GUI")
        self.geometry("900x550")
        self.configure(bg='#2b2b2b')
        self.create_styles()
        self.create_widgets()
        self.load_data()

    def create_styles(self):
        style = ttk.Style(self)
        style.theme_use('clam')

        style.configure('TLabelFrame', background='#2b2b2b', foreground='white', font=('Segoe UI', 13, 'bold'), padding=10)
        style.configure('TLabelFrame.Label', font=('Segoe UI', 13, 'bold'), foreground='#ffa500')

        style.configure('TListbox', background='#1e1e1e', foreground='white', font=('Consolas', 11))
        style.configure('TButton', font=('Segoe UI', 11, 'bold'), background='#444', foreground='white')
        style.map('TButton',
            background=[('active', '#ff8c00')],
            foreground=[('active', 'black')]
        )

    def create_widgets(self):
        commit_frame = ttk.LabelFrame(self, text="Commit History")
        commit_frame.grid(row=0, column=0, sticky='nsew', padx=15, pady=15)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.commit_list = tk.Listbox(commit_frame, bg='#1e1e1e', fg='white', font=('Consolas', 11), selectbackground='#ff8c00', activestyle='none', highlightthickness=0, borderwidth=0)
        self.commit_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0,5), pady=5)
        self.commit_list.bind('<<ListboxSelect>>', self.on_commit_select)

        commit_scroll = ttk.Scrollbar(commit_frame, orient=tk.VERTICAL, command=self.commit_list.yview)
        commit_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.commit_list.config(yscrollcommand=commit_scroll.set)

        details_frame = ttk.Frame(self, padding=10)
        details_frame.grid(row=1, column=0, sticky='nsew', padx=15, pady=(0,15))
        self.grid_rowconfigure(1, weight=0)

        self.commit_details = tk.Text(details_frame, height=12, bg='#1e1e1e', fg='white', font=('Consolas', 10), wrap='word', borderwidth=0)
        self.commit_details.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        details_scroll = ttk.Scrollbar(details_frame, orient=tk.VERTICAL, command=self.commit_details.yview)
        details_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.commit_details.config(yscrollcommand=details_scroll.set)

        status_frame = ttk.LabelFrame(self, text="Staged Files")
        status_frame.grid(row=0, column=1, rowspan=2, sticky='nsew', padx=15, pady=15)
        self.grid_columnconfigure(1, weight=0)

        self.status_list = tk.Listbox(status_frame, bg='#1e1e1e', fg='white', font=('Consolas', 11), selectbackground='#ff8c00', activestyle='none', borderwidth=0)
        self.status_list.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.status_list.bind('<<ListboxSelect>>', self.on_file_select)

        status_scroll = ttk.Scrollbar(status_frame, orient=tk.VERTICAL, command=self.status_list.yview)
        status_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.status_list.config(yscrollcommand=status_scroll.set)

    def load_data(self):
        self.commits = []
        import os
        obj_dir = '.mygit/objects'
        if os.path.exists(obj_dir):
            for fname in os.listdir(obj_dir):
                if len(fname) == 40:
                    self.commits.append(fname)

        for commit_hash in self.commits:
            self.commit_list.insert(tk.END, commit_hash[:7])

        self.file_hash_map = {}  # filepath -> hash
        staged_files = []
        try:
            with open('.mygit/index', 'r') as f:
                lines = f.read().splitlines()
                for line in lines:
                    h, fpath = line.split(' ', 1)
                    staged_files.append(fpath)
                    self.file_hash_map[fpath] = h
        except:
            pass

        for f in staged_files:
            self.status_list.insert(tk.END, f)

    def on_commit_select(self, event):
        selection = event.widget.curselection()
        if selection:
            index = selection[0]
            commit_hash = self.commits[index]
            details = self.load_commit_details(commit_hash)
            self.commit_details.delete(1.0, tk.END)
            self.insert_colored_text(details)

    def load_commit_details(self, commit_hash):
        try:
            with open(f'.mygit/objects/{commit_hash}', 'r') as f:
                return f.read()
        except Exception as e:
            return f"Error loading commit details: {e}"

    def insert_colored_text(self, text):
        self.commit_details.tag_configure('hash', foreground='#ffa500')
        self.commit_details.tag_configure('keyword', foreground='#00ffff', font=('Consolas', 10, 'bold'))
        self.commit_details.tag_configure('error', foreground='#ff5555')
        import re

        lines = text.split('\n')
        for line in lines:
            if line.startswith('commit '):
                self.commit_details.insert(tk.END, line + '\n', 'hash')
            elif re.match(r'^(Author|Date|files:)', line):
                self.commit_details.insert(tk.END, line + '\n', 'keyword')
            elif line.lower().startswith('error'):
                self.commit_details.insert(tk.END, line + '\n', 'error')
            else:
                self.commit_details.insert(tk.END, line + '\n')

    def on_file_select(self, event):
        selection = event.widget.curselection()
        if not selection:
            return
        index = selection[0]
        filepath = self.status_list.get(index)
        self.show_file_diff(filepath)

    def show_file_diff(self, filepath):
        staged_hash = self.file_hash_map.get(filepath)
        if not staged_hash:
            messagebox.showinfo("Info", f"No staged version found for {filepath}")
            return

        staged_path = f'.mygit/objects/{staged_hash}'

        try:
            with open(staged_path, 'rb') as f:
                staged_bytes = f.read()
            staged_text = staged_bytes.decode('utf-8', errors='replace').splitlines()
        except Exception as e:
            messagebox.showerror("Error", f"Error loading staged file content:\n{e}")
            return

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                working_text = f.read().splitlines()
        except Exception as e:
            messagebox.showerror("Error", f"Error loading working file content:\n{e}")
            return

        diff_lines = list(difflib.unified_diff(staged_text, working_text, fromfile='staged', tofile='working', lineterm=''))

        if not diff_lines:
            messagebox.showinfo("Info", "No differences found between staged and working file.")
            return

        self.show_diff_popup(filepath, diff_lines)


    def show_diff_popup(self, filename, diff_lines):
        popup = tk.Toplevel(self)
        popup.title(f"Diff - {filename}")
        popup.geometry("700x500")
        popup.configure(bg='#2b2b2b')

        text = tk.Text(popup, bg='#1e1e1e', fg='white', font=('Consolas', 11), wrap='none')
        text.pack(fill=tk.BOTH, expand=True)

        scrollbar_y = ttk.Scrollbar(popup, orient=tk.VERTICAL, command=text.yview)
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        text.config(yscrollcommand=scrollbar_y.set)

        scrollbar_x = ttk.Scrollbar(popup, orient=tk.HORIZONTAL, command=text.xview)
        scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        text.config(xscrollcommand=scrollbar_x.set)

        # Define tags for coloring diff
        text.tag_configure('added', foreground='#00ff00')
        text.tag_configure('removed', foreground='#ff5555')
        text.tag_configure('info', foreground='#cccccc')

        for line in diff_lines:
            if line.startswith('+') and not line.startswith('+++'):
                text.insert(tk.END, line + '\n', 'added')
            elif line.startswith('-') and not line.startswith('---'):
                text.insert(tk.END, line + '\n', 'removed')
            else:
                text.insert(tk.END, line + '\n', 'info')

        text.config(state=tk.DISABLED)

if __name__ == "__main__":
    app = MiniGitGUI()
    app.mainloop()
