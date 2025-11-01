"""
CIS 216 – Assignment 11 (Custom Dialog Boxes)
Author: Amtoj Singh

Extends prior editor with:
  - Help > About…  -> custom Toplevel dialog (modal)
  - Format > Font… -> custom Toplevel dialog (choose family + size with live preview)
  - Keeps standard File actions (New/Open/Save/Save As) from earlier sessions for completeness

Non-Wikiversity references:
  - Tkinter Toplevel / modal patterns: https://tkdocs.com/tutorial/windows.html
  - Fonts API (tkinter.font): https://docs.python.org/3/library/tkinter.font.html
  - filedialog/colorchooser/simpledialog docs for context: https://docs.python.org/3/library/dialog.html

Notes:
  - Using a shared tkfont.Font so changes apply immediately to the Text widget.
  - Horizontal scrolling needs wrap='none' to show the H-scrollbar actually doing work.
"""

from __future__ import annotations
import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, colorchooser
from tkinter import font as tkfont

from about_dialog import AboutDialog
from font_dialog import FontDialog


APP_NAME = "CIS216 Editor"
APP_VERSION = "1.3"
APP_AUTHOR = "Amtoj Singh"
APP_EMAIL = "sa48190@mail.harpercollege.edu"  # course email (ok to show in About)


class EditorWithCustomDialogs(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title(f"{APP_NAME} (Custom Dialogs)")
        self.geometry("900x600")

        self.current_path: str | None = None
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

        self.text = tk.Text(frame, wrap="none", undo=True, font=self.text_font)
        self.text.grid(row=0, column=0, sticky="nsew")

        yscroll = ttk.Scrollbar(frame, orient="vertical", command=self.text.yview)
        xscroll = ttk.Scrollbar(frame, orient="horizontal", command=self.text.xview)
        yscroll.grid(row=0, column=1, sticky="ns")
        xscroll.grid(row=1, column=0, sticky="ew")
        self.text.configure(yscrollcommand=yscroll.set, xscrollcommand=xscroll.set)

        self.status = tk.StringVar(value="Ready")
        ttk.Label(self, textvariable=self.status, anchor="w", padding=(8, 2)).grid(row=1, column=0, sticky="ew")

        # Status updates
        self.text.bind("<<Modified>>", self._on_modified)
        self.text.bind("<KeyRelease>", lambda e: self._update_status())
        self.text.bind("<ButtonRelease>", lambda e: self._update_status())

    # ---------- menus ----------
    def _build_menus(self) -> None:
        menubar = tk.Menu(self)

        # File
        file_menu = tk.Menu(menubar, tearoff=False)
        file_menu.add_command(label="New", accelerator="Ctrl+N", command=self.action_new)
        file_menu.add_command(label="Open…", accelerator="Ctrl+O", command=self.action_open)
        file_menu.add_command(label="Save", accelerator="Ctrl+S", command=self.action_save)
        file_menu.add_command(label="Save As…", accelerator="Ctrl+Shift+S", command=self.action_save_as)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", accelerator="Ctrl+Q", command=self.action_exit)
        menubar.add_cascade(label="File", menu=file_menu)

        # Edit
        edit_menu = tk.Menu(menubar, tearoff=False)
        edit_menu.add_command(label="Undo", accelerator="Ctrl+Z", command=lambda: self.text.event_generate("<<Undo>>"))
        edit_menu.add_command(label="Redo", accelerator="Ctrl+Y", command=lambda: self.text.event_generate("<<Redo>>"))
        edit_menu.add_separator()
        edit_menu.add_command(label="Cut", accelerator="Ctrl+X", command=lambda: self.text.event_generate("<<Cut>>"))
        edit_menu.add_command(label="Copy", accelerator="Ctrl+C", command=lambda: self.text.event_generate("<<Copy>>"))
        edit_menu.add_command(label="Paste", accelerator="Ctrl+V", command=lambda: self.text.event_generate("<<Paste>>"))
        menubar.add_cascade(label="Edit", menu=edit_menu)

        # Format
        fmt_menu = tk.Menu(menubar, tearoff=False)
        fmt_menu.add_command(label="Text Color…", command=self.action_text_color)  # keeps standard color dialog
        fmt_menu.add_command(label="Font…", command=self.action_font_custom)       # custom font dialog (this session)
        menubar.add_cascade(label="Format", menu=fmt_menu)

        # Help
        help_menu = tk.Menu(menubar, tearoff=False)
        help_menu.add_command(label="About…", command=self.action_about_custom)
        menubar.add_cascade(label="Help", menu=help_menu)

        self.config(menu=menubar)

    # ---------- shortcuts ----------
    def _bind_shortcuts(self) -> None:
        self.bind_all("<Control-n>", lambda e: self.action_new())
        self.bind_all("<Control-o>", lambda e: self.action_open())
        self.bind_all("<Control-s>", lambda e: self.action_save())
        self.bind_all("<Control-S>", lambda e: self.action_save_as())
        self.bind_all("<Control-q>", lambda e: self.action_exit())

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
        fname = os.path.basename(self.current_path) if self.current_path else "Untitled"
        self.status.set(f"{fname} — {words} words, {chars} chars")
        # TODO(amtoj): line:col indicator near the right edge

    # ---------- file helpers ----------
    def _read_file(self, path: str) -> str:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()

    def _write_file(self, path: str, data: str) -> None:
        with open(path, "w", encoding="utf-8") as f:
            f.write(data)

    # ---------- file actions ----------
    def action_new(self) -> None:
        has_text = bool(self.text.get("1.0", "end-1c").strip())
        if has_text and self.current_path is None:
            if not messagebox.askyesno("Discard?", "Discard current contents?"):
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
        # (Optional future improvement: prompt to save if modified)
        self.destroy()

    # ---------- custom dialogs ----------
    def action_about_custom(self) -> None:
        AboutDialog(self, app_name=APP_NAME, version=APP_VERSION, author=APP_AUTHOR, email=APP_EMAIL)

    def action_font_custom(self) -> None:
        """
        Show custom font dialog. On OK, apply new family/size to the shared tkfont.Font,
        which updates the Text widget immediately.
        """
        current_family = self.text_font.cget("family")
        current_size = int(self.text_font.cget("size"))
        dlg = FontDialog(self, initial_family=current_family, initial_size=current_size)
        if dlg.result:
            fam = dlg.result["family"]
            size = dlg.result["size"]
            self.text_font.configure(family=fam, size=size)

    def action_text_color(self) -> None:
        # Keep color chooser from previous session for convenience
        _rgb, hex_code = colorchooser.askcolor(title="Choose text color")
        if hex_code:
            self.text.configure(fg=hex_code)


def main() -> None:
    app = EditorWithCustomDialogs()
    app.mainloop()


if __name__ == "__main__":
    main()
