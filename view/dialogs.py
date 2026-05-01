import tkinter as tk
from tkinter import simpledialog, messagebox


class NewGraphDialog(simpledialog.Dialog):
    def body(self, master):
        self.directed_var = tk.BooleanVar(value=False)
        self.weighted_var = tk.BooleanVar(value=False)
        tk.Checkbutton(master, text="Có hướng (directed)", variable=self.directed_var).pack(anchor="w", padx=10, pady=2)
        tk.Checkbutton(master, text="Có trọng số (weighted)", variable=self.weighted_var).pack(anchor="w", padx=10, pady=2)
        return None

    def apply(self):
        self.result = (self.directed_var.get(), self.weighted_var.get())


def ask_weight(parent):
    return simpledialog.askfloat("Trọng số", "Nhập trọng số cạnh:",
                                  parent=parent, minvalue=0)


def ask_node_name(parent, default: str = ""):
    return simpledialog.askstring("Tên đỉnh", "Tên đỉnh:",
                                   parent=parent, initialvalue=default)


def info(parent, title: str, msg: str):
    messagebox.showinfo(title, msg, parent=parent)


def warn(parent, title: str, msg: str):
    messagebox.showwarning(title, msg, parent=parent)
