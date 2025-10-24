"""
CIS 216 – Assignment 10 (Standard Dialog Boxes)
Author: Amtoj Singh

Goal:
  Extend the text editor with standard dialogs:
    - File > Open, Save, Save As…  (file dialogs)
    - Format > Text Color… (color chooser)
    - Format > Font Size… (simple dialog)
  Keep it straightforward and readable, with small UX touches.

Non-Wikiversity references (syntax/how-to only):
  - tkinter.filedialog: https://docs.python.org/3/library/dialog.html#module-tkinter.filedialog
  - tkinter.colorchooser: https://docs.python.org/3/library/dialog.html#module-tkinter.colorchooser
  - tkinter.simpledialog: https://docs.python.org/3/library/dialog.html#tkinter.simpledialog
  - Tkinter Text: https://tkdocs.com/shipman/text.html

Notes:
  - Horizontal scrolling needs wrap='none' to function.
  - Using utf-8 for file I/O (fine for class work).
"""

from __future__ import annotations
import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, colorchooser, simpledialog
from tkinter import font as tkfont


class EditorWithDialogs(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("CIS216 – Text Editor (Standard Dialogs)")
        self.geometry("900x600")

        # current file (None means “Unsaved/Untitled”)
        self.current_path: str | None = None

        # font state for the editor (family+size)
        # NOTE: using a tkfont.Font so changes apply immediately
        self.text_font = tkfont.Font(family="Consolas", size=12)

        self._build_layout()
        self._build_menus()
        self._bind_shortcuts()
        self._update_status()

    # ---------- layout ----------
    def _build_layout(self) -> None:
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        frame = ttk.Frame(self, padding=(8, 6))
        frame.grid(row=0, column=0, sticky="nsew")
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(0, weight=1)

        # editor area
        self.text = tk.Text(
            frame,
            wrap="none",          # so H-scrollbar is useful
            undo=True,
            font=self.text_font,
        )
        self.text.grid(row=0, column=0, sticky="nsew")

        # scrollbars
        yscroll = ttk.Scrollbar(frame, orient="vertical", command=self.text.yview)
        xscroll = ttk.Scrollbar(frame, orient="horizontal", command=self.text.xview)
        yscroll.grid(row=0, column=1, sticky="ns")
        xscroll.grid(row=1, column=0, sticky="ew")
        self.text.configure(yscrollcommand=yscroll.set, xscrollcommand=xscroll.set)

        # status bar
        self.status = tk.StringVar(value="Ready")
        status_bar = ttk.Label(self, textvariable=self.status, anchor="w", padding=(8, 2))
        status_bar.grid(row=1, column=0, sticky="ew")

        # update status on edits/movement
        self.text.bind("<<Modified>>", self._on_modified)
        self.text.bind("<KeyRelease>", lambda e: self._update_status())
        self.text.bind("<ButtonRelease>", lambda e: self._update_status())

    # ---------- menus ----------
    def _build_menus(self) -> None:
        menubar = tk.Menu(self)

        # File menu
        file_menu = tk.Menu(menubar, tearoff=False)
        file_menu.add_command(label="New", accelerator="Ctrl+N", command=self.action_new)
        file_menu.add_command(label="Open…", accelerator="Ctrl+O", command=self.action_open)
        file_menu.add_command(label="Save", accelerator="Ctrl+S", command=self.action_save)
        file_menu.add_command(label="Save As…", accelerator="Ctrl+Shift+S", command=self.action_save_as)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", accelerator="Ctrl+Q", command=self.action_exit)
        menubar.add_cascade(label="File", menu=file_menu)

        # Edit menu (kept from Session 9 for completeness)
        edit_menu = tk.Menu(menubar, tearoff=False)
        edit_menu.add_command(label="Undo", accelerator="Ctrl+Z", command=lambda: self.text.event_generate("<<Undo>>"))
        edit_menu.add_command(label="Redo", accelerator="Ctrl+Y", command=lambda: self.text.event_generate("<<Redo>>"))
        edit_menu.add_separator()
        edit_menu.add_command(label="Cut", accelerator="Ctrl+X", command=lambda: self.text.event_generate("<<Cut>>"))
        edit_menu.add_command(label="Copy", accelerator="Ctrl+C", command=lambda: self.text.event_generate("<<Copy>>"))
        edit_menu.add_command(label="Paste", accelerator="Ctrl+V", command=lambda: self.text.event_generate("<<Paste>>"))
        menubar.add_cascade(label="Edit", menu=edit_menu)

        # Format menu (new for Session 10)
        format_menu = tk.Menu(menubar, tearoff=False)
        format_menu.add_command(label="Text Color…", command=self.action_text_color)
        format_menu.add_command(label="Font Size…", command=self.action_font_size)
        # (Optional) could add "Font Family…" later — see TODO below
        menubar.add_cascade(label="Format", menu=format_menu)

        self.config(menu=menubar)

    # ---------- shortcuts ----------
    def _bind_shortcuts(self) -> None:
        self.bind_all("<Control-n>", lambda e: self.action_new())
        self.bind_all("<Control-o>", lambda e: self.action_open())
        self.bind_all("<Control-s>", lambda e: self.action_save())
        self.bind_all("<Control-S>", lambda e: self.action_save_as())  # Shift+Ctrl+S
        self.bind_all("<Control-q>", lambda e: self.action_exit())

        # edit shortcuts
        self.bind_all("<Control-z>", lambda e: self.text.event_generate("<<Undo>>"))
        self.bind_all("<Control-y>", lambda e: self.text.event_generate("<<Redo>>"))
        self.bind_all("<Control-x>", lambda e: self.text.event_generate("<<Cut>>"))
        self.bind_all("<Control-c>", lambda e: self.text.event_generate("<<Copy>>"))
        self.bind_all("<Control-v>", lambda e: self.text.event_generate("<<Paste>>"))

    # ---------- status ----------
    def _on_modified(self, _e=None) -> None:
        self.text.edit_modified(False)
        self._update_status()

    def _update_status(self) -> None:
        contents = self.text.get("1.0", "end-1c")
        words = len(contents.split()) if contents.strip() else 0
        chars = len(contents)
        filename = os.path.basename(self.current_path) if self.current_path else "Untitled"
        self.status.set(f"{filename} — {words} words, {chars} chars")
        # TODO(amtoj): add line:column display near the right edge

    # ---------- helpers ----------
    def _confirm_discard_if_needed(self) -> bool:
        """If there’s content and we’re in Untitled, ask before nuking."""
        has_text = bool(self.text.get("1.0", "end-1c").strip())
        if has_text and self.current_path is None:
            return messagebox.askyesno("Discard?", "Discard current contents?")
        return True

    def _read_file(self, path: str) -> str:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()

    def _write_file(self, path: str, data: str) -> None:
        with open(path, "w", encoding="utf-8") as f:
            f.write(data)

    # ---------- file actions (standard dialogs) ----------
    def action_new(self) -> None:
        if not self._confirm_discard_if_needed():
            return
        self.text.delete("1.0", "end")
        self.current_path = None
        self._update_status()

    def action_open(self) -> None:
        path = filedialog.askopenfilename(
            title="Open File",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
        )
        if not path:
            return
        try:
            data = self._read_file(path)
        except Exception as e:
            messagebox.showerror("Open failed", f"Could not open file:\n{e}")
            return
        self.text.delete("1.0", "end")
        self.text.insert("1.0", data)
        self.current_path = path
        self._update_status()

    def action_save(self) -> None:
        if self.current_path is None:
            self.action_save_as()
            return
        try:
            data = self.text.get("1.0", "end-1c")
            self._write_file(self.current_path, data)
            self._update_status()
        except Exception as e:
            messagebox.showerror("Save failed", f"Could not save file:\n{e}")

    def action_save_as(self) -> None:
        path = filedialog.asksaveasfilename(
            title="Save As",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
        )
        if not path:
            return
        self.current_path = path
        self.action_save()

    def action_exit(self) -> None:
        # Minimal exit (you could ask to save here if desired)
        self.destroy()

    # ---------- format actions (standard dialogs) ----------
    def action_text_color(self) -> None:
        """
        Use the standard color chooser to set the text foreground color.
        Returns ( (r,g,b), "#rrggbb" ). We use the hex string.
        """
        rgb_tuple, hex_code = colorchooser.askcolor(title="Choose text color")
        if not hex_code:
            return  # user cancelled
        self.text.configure(fg=hex_code)

    def action_font_size(self) -> None:
        """
        Use a standard simple dialog to ask for a new font size.
        Keep it basic: just an integer between 6 and 72.
        """
        size = simpledialog.askinteger(
            "Font Size",
            "Enter a font size (6–72):",
            minvalue=6,
            maxvalue=72,
            parent=self,
        )
        if not size:
            return
        # update the tkfont.Font used by the Text widget
        self.text_font.configure(size=size)


def main() -> None:
    app = EditorWithDialogs()
    app.mainloop()


if __name__ == "__main__":
    main()
