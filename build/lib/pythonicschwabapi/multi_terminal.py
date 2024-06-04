import tkinter as tk
from tkinter import ttk
import threading


class MultiTerminal(threading.Thread):
    def __init__(self, title="Terminal", height=20, width=200, font=("Courier New", "12"), backgroundColor="gray5",
                 textColor="snow", allowClosing=True, ignoreClosedPrints=True):
        super().__init__(daemon=True)
        self.title = title
        self.height = height
        self.width = width
        self.font = font
        self.backgroundColor = backgroundColor
        self.textColor = textColor
        self.allowClosing = allowClosing
        self.ignoreClosedPrints = ignoreClosedPrints
        self.is_open = False
        self.start()

    def run(self):
        self.root = tk.Tk()
        self.root.title(self.title)
        self.root.protocol("WM_DELETE_WINDOW", self.close if self.allowClosing else lambda: None)
        self.text_box = tk.Text(self.root, height=self.height, width=self.width, font=self.font,
                                bg=self.backgroundColor, fg=self.textColor, state='disabled')
        self.text_box.pack(side="left", fill="both", expand=True)
        self.is_open = True
        self.root.mainloop()

    def close(self):
        if self.is_open:
            self.is_open = False
            self.root.destroy()

    def print(self, text, end="\n"):
        if not self.is_open:
            if not self.ignoreClosedPrints:
                raise Exception(f"Terminal '{self.title}' is closed.")
            return
        self.text_box.configure(state="normal")
        self.text_box.insert("end", text + end)
        self.text_box.configure(state="disabled")
        self.text_box.see("end")
