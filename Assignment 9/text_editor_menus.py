"""
CIS 216 – Assignment 9 (Menus & Events)
Author: Amtoj Singh

Goal:
  Extend the Session 8 text editor with:
    - File menu: New, Exit
    - Edit menu: Cut, Copy, Paste
    - Right-click context menu for Edit actions
  Keep it simple and readable so the event wiring is easy to follow.

Non-Wikiversity references (syntax/how-to):
  - Tkinter docs: https://docs.python.org/3/library/tkinter.html
  - Tk Text widget: https://tkdocs.com/shipman/text.html
"""

from __future__ import annotations
import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox


class EditorWithMenus(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("CIS216 – Text Editor (Menus & Events)")
        self.geometry("860x560")
        self.current_path: str | None = None

        self._build_layout()
        self._build_menu_bar()
        self._build_context_menu()
        self._bind_shortcuts()
        self._update_status()

    # ---------- UI Layout ----------
    def _build_layout(self) -> None:
        # top-level grid
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # editor frame
        frame = ttk.Frame(self, padding=(8, 6))
        frame.grid(row=0, column=0, sticky="nsew")
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(0, weight=1)

        # text area
        # NOTE: wrap='none' so the horizontal scrollbar actually does something
        self.text = tk.Text(frame, wrap="none", undo=True, font=("Consolas", 12))
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

        # update status when edited
        self.text.bind("<<Modified>>", self._on_modified)
        self.text.bind("<KeyRelease>", lambda e: self._update_status())
        self.text.bind("<ButtonRelease>", lambda e: self._update_status())

        # right-click context menu
        # Windows/Linux = <Button-3>, macOS often supports Control-Click fallback
        self.text.bind("<Button-3>", self._show_context_menu)              # win/linux
        self.text.bind("<Control-Button-1>", self._show_context_menu)      # mac fallback

    # ---------- Menus ----------
    def _build_menu_bar(self) -> None:
        menubar = tk.Menu(self)

        # File
        file_menu = tk.Menu(menubar, tearoff=False)
        file_menu.add_command(label="New", accelerator="Ctrl+N", command=self.action_new)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", accelerator="Ctrl+Q", command=self.action_exit)
        menubar.add_cascade(label="File", menu=file_menu)

        # Edit
        edit_menu = tk.Menu(menubar, tearoff=False)
        edit_menu.add_command(label="Cut", accelerator="Ctrl+X", command=self.action_cut)
        edit_menu.add_command(label="Copy", accelerator="Ctrl+C", command=self.action_copy)
        edit_menu.add_command(label="Paste", accelerator="Ctrl+V", command=self.action_paste)
        menubar.add_cascade(label="Edit", menu=edit_menu)

        self.config(menu=menubar)

    def _build_context_menu(self) -> None:
        self.context = tk.Menu(self, tearoff=False)
        self.context.add_command(label="Cut", command=self.action_cut)
        self.context.add_command(label="Copy", command=self.action_copy)
        self.context.add_command(label="Paste", command=self.action_paste)

    def _show_context_menu(self, event: tk.Event) -> None:
        # post the popup where the cursor is
        try:
            self.context.tk_popup(event.x_root, event.y_root)
        finally:
            self.context.grab_release()

    # ---------- Shortcuts ----------
    def _bind_shortcuts(self) -> None:
        # File actions
        self.bind_all("<Control-n>", lambda e: self.action_new())
        self.bind_all("<Control-q>", lambda e: self.action_exit())

        # Edit actions (use Text virtual events under the hood)
        self.bind_all("<Control-x>", lambda e: self.action_cut())
        self.bind_all("<Control-c>", lambda e: self.action_copy())
        self.bind_all("<Control-v>", lambda e: self.action_paste())

        # Optional: common editing keys pass through to Text anyway,
        # but we can wire Undo/Redo if desired:
        self.bind_all("<Control-z>", lambda e: self.text.event_generate("<<Undo>>"))
        self.bind_all("<Control-y>", lambda e: self.text.event_generate("<<Redo>>"))

    # ---------- Status & Editing ----------
    def _on_modified(self, _event=None) -> None:
        # Reset modified flag so it fires again next time
        self.text.edit_modified(False)
        self._update_status()

    def _update_status(self) -> None:
        contents = self.text.get("1.0", "end-1c")
        words = len(contents.split()) if contents.strip() else 0
        chars = len(contents)
        filename = os.path.basename(self.current_path) if self.current_path else "Untitled"
        # tiny UX choice: show "Untitled" until saved, keep counts visible
        self.status.set(f"{filename} — {words} words, {chars} chars")
        # TODO(amtoj): consider adding line:column info later

    # ---------- File actions ----------
    def _confirm_discard_if_needed(self) -> bool:
        # If there is text and no path yet, ask before nuking it
        has_text = bool(self.text.get("1.0", "end-1c").strip())
        if has_text and self.current_path is None:
            return messagebox.askyesno("Discard?", "Discard current contents?")
        return True

    def action_new(self) -> None:
        if not self._confirm_discard_if_needed():
            return
        self.text.delete("1.0", "end")
        self.current_path = None
        self._update_status()

    def action_exit(self) -> None:
        # Basic exit; if you want a "Save before exit?" flow, wire it here
        self.destroy()

    # ---------- Edit actions ----------
    # Using Text virtual events to avoid re-implementing clipboard logic
    def action_cut(self) -> None:
        self.text.event_generate("<<Cut>>")

    def action_copy(self) -> None:
        self.text.event_generate("<<Copy>>")

    def action_paste(self) -> None:
        self.text.event_generate("<<Paste>>")


def main() -> None:
    app = EditorWithMenus()
    app.mainloop()


if __name__ == "__main__":
    main()
