"""
CIS 216 – Assignment 8 (GUI Text Editor)
Author: Amtoj Singh

Simple text editor with:
- New / Open / Save / Save As
- Vertical *and* horizontal scrollbars
- Word & character counts in a status bar
- Optional word wrap toggle
- Light error handling with message boxes

Non-Wikiversity references:
- Tkinter: https://docs.python.org/3/library/tkinter.html
- tkinter.filedialog: https://docs.python.org/3/library/dialog.html#module-tkinter.filedialog
- Text widget: https://tkdocs.com/shipman/text.html  (nice practical guide)

Notes:
- Horizontal scrolling only works if wrap is disabled (wrap='none').
- I default to wrap='none' to satisfy the “include vertical and horizontal scrollbars” requirement.
"""

from __future__ import annotations
import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox


class SimpleEditor(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Simple Text Editor – CIS216")
        self.geometry("800x520")

        # current file path (None if new/unsaved)
        self.current_path: str | None = None
        self._setup_ui()
        self._bind_events()

    # ---------- UI ----------
    def _setup_ui(self) -> None:
        # Top-level grid
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        # Menu
        self._build_menu()

        # Toolbar (wrap toggle)
        toolbar = ttk.Frame(self, padding=(8, 4))
        toolbar.grid(row=0, column=0, sticky="ew")
        self.word_wrap = tk.BooleanVar(value=False)  # keep wrap off by default
        ttk.Checkbutton(
            toolbar, text="Word Wrap", variable=self.word_wrap, command=self._toggle_wrap
        ).pack(side="left")

        # Text area + scrollbars in a frame
        text_frame = ttk.Frame(self)
        text_frame.grid(row=1, column=0, sticky="nsew")
        text_frame.columnconfigure(0, weight=1)
        text_frame.rowconfigure(0, weight=1)

        # Text widget
        # wrap='none' allows H-scrollbar to work; see _toggle_wrap for switching
        self.text = tk.Text(
            text_frame,
            wrap="none",
            undo=True,
            font=("Consolas", 12),
        )
        self.text.grid(row=0, column=0, sticky="nsew")

        # Scrollbars (vertical + horizontal)
        yscroll = ttk.Scrollbar(text_frame, orient="vertical", command=self.text.yview)
        xscroll = ttk.Scrollbar(text_frame, orient="horizontal", command=self.text.xview)
        yscroll.grid(row=0, column=1, sticky="ns")
        xscroll.grid(row=1, column=0, sticky="ew")

        # Connect scrollbars to the Text widget
        self.text.configure(yscrollcommand=yscroll.set, xscrollcommand=xscroll.set)

        # Status bar
        self.status = tk.StringVar(value="Ready")
        status_bar = ttk.Label(self, textvariable=self.status, anchor="w", padding=(8, 2))
        status_bar.grid(row=2, column=0, sticky="ew")

    def _build_menu(self) -> None:
        menubar = tk.Menu(self)

        file_menu = tk.Menu(menubar, tearoff=False)
        file_menu.add_command(label="New", accelerator="Ctrl+N", command=self.new_file)
        file_menu.add_command(label="Open…", accelerator="Ctrl+O", command=self.open_file)
        file_menu.add_command(label="Save", accelerator="Ctrl+S", command=self.save)
        file_menu.add_command(label="Save As…", accelerator="Ctrl+Shift+S", command=self.save_as)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.destroy)
        menubar.add_cascade(label="File", menu=file_menu)

        edit_menu = tk.Menu(menubar, tearoff=False)
        edit_menu.add_command(label="Undo", accelerator="Ctrl+Z", command=lambda: self.text.event_generate("<<Undo>>"))
        edit_menu.add_command(label="Redo", accelerator="Ctrl+Y", command=lambda: self.text.event_generate("<<Redo>>"))
        edit_menu.add_separator()
        edit_menu.add_command(label="Cut", accelerator="Ctrl+X", command=lambda: self.text.event_generate("<<Cut>>"))
        edit_menu.add_command(label="Copy", accelerator="Ctrl+C", command=lambda: self.text.event_generate("<<Copy>>"))
        edit_menu.add_command(label="Paste", accelerator="Ctrl+V", command=lambda: self.text.event_generate("<<Paste>>"))
        menubar.add_cascade(label="Edit", menu=edit_menu)

        self.config(menu=menubar)

    # ---------- events & helpers ----------
    def _bind_events(self) -> None:
        # Keyboard shortcuts
        self.bind_all("<Control-n>", lambda e: self.new_file())
        self.bind_all("<Control-o>", lambda e: self.open_file())
        self.bind_all("<Control-s>", lambda e: self.save())
        self.bind_all("<Control-S>", lambda e: self.save_as())  # Shift+Ctrl+S
        self.bind_all("<Control-y>", lambda e: self.text.event_generate("<<Redo>>"))
        self.bind_all("<Control-z>", lambda e: self.text.event_generate("<<Undo>>"))

        # Update status as user types or moves
        self.text.bind("<<Modified>>", self._on_modified)
        self.text.bind("<KeyRelease>", lambda e: self._update_status())
        self.text.bind("<ButtonRelease>", lambda e: self._update_status())

    def _toggle_wrap(self) -> None:
        # NOTE: horizontal scrolling only works when wrap is 'none'.
        # That’s why the checkbox flips wrap between 'word' and 'none'.
        self.text.configure(wrap="word" if self.word_wrap.get() else "none")

    def _on_modified(self, event=None) -> None:
        # Reset modified flag and update counts
        self.text.edit_modified(False)
        self._update_status()

    def _update_status(self) -> None:
        contents = self.text.get("1.0", "end-1c")
        chars = len(contents)
        words = len(contents.split()) if contents.strip() else 0
        # tiny UX choice: show "Untitled" until the first save, so the status isn’t blank
        filename = os.path.basename(self.current_path) if self.current_path else "Untitled"
        self.status.set(f"{filename} — {words} words, {chars} chars")
        # TODO(amtoj): add line/column indicator later

    # ---------- file actions ----------
    def confirm_discard(self) -> bool:
        # Simple heuristic: if text is modified, ask. Tk Text has an internal modified flag,
        # but we’re recomputing status anyway—this is a straightforward prompt.
        contents = self.text.get("1.0", "end-1c")
        if contents and self.current_path is None:
            return messagebox.askyesno("Discard?", "Discard current contents?")
        return True

    def new_file(self) -> None:
        if not self.confirm_discard():
            return
        self.text.delete("1.0", "end")
        self.current_path = None
        self._update_status()

    def open_file(self) -> None:
        if not self.confirm_discard():
            return
        path = filedialog.askopenfilename(
            title="Open file",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if not path:
            return
        try:
            # using utf-8 by default — good enough for class; real apps might detect encoding
            with open(path, "r", encoding="utf-8") as f:
                data = f.read()
        except Exception as e:
            messagebox.showerror("Open failed", f"Could not open file:\n{e}")
            return
        self.text.delete("1.0", "end")
        self.text.insert("1.0", data)
        self.current_path = path
        self._update_status()

    def save(self) -> None:
        if self.current_path is None:
            self.save_as()
            return
        try:
            data = self.text.get("1.0", "end-1c")
            with open(self.current_path, "w", encoding="utf-8") as f:
                f.write(data)
            self._update_status()
        except Exception as e:
            messagebox.showerror("Save failed", f"Could not save file:\n{e}")

    def save_as(self) -> None:
        path = filedialog.asksaveasfilename(
            title="Save As",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if not path:
            return
        self.current_path = path
        self.save()


def main() -> None:
    app = SimpleEditor()
    app.mainloop()


if __name__ == "__main__":
    main()
