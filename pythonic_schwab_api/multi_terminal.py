"""
This module provides a MultiTerminal class that creates a simple
multi-threaded terminal window using Tkinter.
"""

import tkinter as tk
import threading


class MultiTerminal(threading.Thread):
    """
    A class to create a multi-threaded terminal window using Tkinter.

    Attributes:
        title (str): The title of the terminal window.
        height (int): The height of the terminal window.
        width (int): The width of the terminal window.
        font (tuple): The font of the text in the terminal window.
        backgroundColor (str): The background color of the terminal window.
        textColor (str): The text color in the terminal window.
        allowClosing (bool): Whether the terminal window can be closed.
        ignoreClosedPrints (bool): Whether to ignore prints when the terminal
                                is closed.
    """

    def __init__(self, title="Terminal", height=20, width=200, font=("Courier New", "12"),
                backgroundColor="gray5", textColor="snow", allowClosing=True,
                ignoreClosedPrints=True):
        """
        Initializes the MultiTerminal with the given parameters.

        Args:
            title (str): The title of the terminal window.
            height (int): The height of the terminal window.
            width (int): The width of the terminal window.
            font (tuple): The font of the text in the terminal window.
            backgroundColor (str): The background color of the terminal window.
            textColor (str): The text color in the terminal window.
            allowClosing (bool): Whether the terminal window can be closed.
            ignoreClosedPrints (bool): Whether to ignore prints when the terminal
                                    is closed.
        """
        super().__init__(daemon=True)
        self.title = title
        self.height = height
        self.width = width
        self.font = font
        self.background_color = backgroundColor
        self.text_color = textColor
        self.allow_closing = allowClosing
        self.ignore_closed_prints = ignoreClosedPrints
        self.is_open = False
        self.root = None
        self.text_box = None
        self.start()

    def run(self):
        """Runs the Tkinter main loop to display the terminal window."""
        self.root = tk.Tk()
        self.root.title(self.title)
        self.root.protocol("WM_DELETE_WINDOW", self.close if self.allow_closing else lambda: None)
        self.text_box = tk.Text(self.root, height=self.height, width=self.width, font=self.font,
                                bg=self.background_color, fg=self.text_color, state='disabled')
        self.text_box.pack(side="left", fill="both", expand=True)
        self.is_open = True
        self.root.mainloop()

    def close(self):
        """Closes the terminal window."""
        if self.is_open:
            self.is_open = False
            self.root.destroy()

    def print(self, text, end="\n"):
        """
        Prints the given text to the terminal window.

        Args:
            text (str): The text to print.
            end (str): The end character to append after the text.
        """
        if not self.is_open:
            if not self.ignore_closed_prints:
                raise Exception(f"Terminal '{self.title}' is closed.")
            return
        self.text_box.configure(state="normal")
        self.text_box.insert("end", text + end)
        self.text_box.configure(state="disabled")
        self.text_box.see("end")
