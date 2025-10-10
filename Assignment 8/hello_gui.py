"""
CIS 216 – Assignment 8 (GUI)
Author: Amtoj Singh

Tiny “Hello World” GUI to get comfortable with Tkinter widgets,
layout, and event handling.

Non-Wikiversity reference:
- Tkinter intro (official docs): https://docs.python.org/3/library/tkinter.html
"""

import tkinter as tk
from tkinter import ttk


def main() -> None:
    root = tk.Tk()
    root.title("Hello GUI – CIS216")
    root.geometry("360x180")

    # Frame for padding (grid makes resizing nicer)
    container = ttk.Frame(root, padding=16)
    container.grid(sticky="nsew")
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    msg = tk.StringVar(value="👋 Click the button!")

    lbl = ttk.Label(container, textvariable=msg, font=("Segoe UI", 12))
    lbl.grid(row=0, column=0, padx=4, pady=8, sticky="w")

    # TODO(amtoj): maybe add a textbox to let the user type a custom greeting next time
    # (keeping v1 simple so I don’t overcomplicate the intro example)
    def on_click():
        # Simple event handler (changes the label)
        msg.set("Hello, world! ✅")

    btn = ttk.Button(container, text="Say Hello", command=on_click)
    btn.grid(row=1, column=0, padx=4, pady=8, sticky="w")

    # A quit button for convenience (shows multiple widgets + events)
    ttk.Button(container, text="Quit", command=root.destroy).grid(
        row=2, column=0, padx=4, pady=8, sticky="w"
    )

    root.mainloop()


if __name__ == "__main__":
    main()
