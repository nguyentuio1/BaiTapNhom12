import tkinter as tk
from tkinter import scrolledtext


class LogPanel(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        tk.Label(self, text="Log thuật toán", anchor="w").pack(fill=tk.X)
        self.text = scrolledtext.ScrolledText(self, height=6, state=tk.DISABLED, wrap=tk.WORD)
        self.text.pack(fill=tk.BOTH, expand=True)

    def append(self, msg: str):
        self.text.config(state=tk.NORMAL)
        self.text.insert(tk.END, msg + "\n")
        self.text.see(tk.END)
        self.text.config(state=tk.DISABLED)

    def clear(self):
        self.text.config(state=tk.NORMAL)
        self.text.delete("1.0", tk.END)
        self.text.config(state=tk.DISABLED)
