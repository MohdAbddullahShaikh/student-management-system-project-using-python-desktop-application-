"""
main.py - Student Management System
A full-featured desktop application built with Tkinter and MySQL.

Run:  python main.py
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date

from database import Database
from student import Student


# ═══════════════════════════════════════════════════════════════════════════════
# Colour & font palette
# ═══════════════════════════════════════════════════════════════════════════════

PALETTE = {
    "bg_dark":      "#1a1f2e",   # main window background
    "bg_card":      "#242938",   # form / table card
    "bg_input":     "#2e3347",   # entry field background
    "accent":       "#4f8ef7",   # primary blue accent
    "accent_hover": "#3a7aeb",
    "danger":       "#e05c5c",
    "danger_hover": "#c94444",
    "success":      "#4caf7d",
    "warning":      "#f0a045",
    "text_primary": "#e8ecf5",
    "text_muted":   "#8b92a8",
    "border":       "#363d54",
    "header_bg":    "#1e2436",
    "row_even":     "#242938",
    "row_odd":      "#2a2f42",
    "select_bg":    "#2d4a8a",
}

FONT_TITLE  = ("Segoe UI", 20, "bold")
FONT_HEADER = ("Segoe UI", 11, "bold")
FONT_LABEL  = ("Segoe UI", 10)
FONT_ENTRY  = ("Segoe UI", 10)
FONT_BTN    = ("Segoe UI", 10, "bold")
FONT_SMALL  = ("Segoe UI", 9)


# ═══════════════════════════════════════════════════════════════════════════════
# Helper widgets
# ═══════════════════════════════════════════════════════════════════════════════

def make_button(parent, text, command, color, hover_color, width=16):
    """Create a styled flat button with hover effect."""
    btn = tk.Button(
        parent, text=text, command=command,
        bg=color, fg=PALETTE["text_primary"],
        font=FONT_BTN, relief="flat", bd=0,
        activebackground=hover_color,
        activeforeground=PALETTE["text_primary"],
        cursor="hand2", width=width, pady=7,
    )
    btn.bind("<Enter>", lambda e: btn.config(bg=hover_color))
    btn.bind("<Leave>", lambda e: btn.config(bg=color))
    return btn


def make_label(parent, text, **kw):
    return tk.Label(
        parent, text=text, bg=PALETTE["bg_card"],
        fg=PALETTE["text_muted"], font=FONT_LABEL, **kw
    )


def make_entry(parent, textvariable=None, width=30):
    return tk.Entry(
        parent, textvariable=textvariable, width=width,
        bg=PALETTE["bg_input"], fg=PALETTE["text_primary"],
        insertbackground=PALETTE["text_primary"],
        font=FONT_ENTRY, relief="flat", bd=0,
        highlightthickness=1,
        highlightbackground=PALETTE["border"],
        highlightcolor=PALETTE["accent"],
    )


# ═══════════════════════════════════════════════════════════════════════════════
# Main Application Class
# ═══════════════════════════════════════════════════════════════════════════════

class StudentManagementApp:
    """Root Tkinter application for the Student Management System."""

    def __init__(self, root: tk.Tk):
        self.root = root
        self._setup_window()

        # Database
        self.db = Database()
        try:
            self.db.setup_database()
        except Exception as e:
            messagebox.showerror(
                "Database Error",
                f"Could not connect to MySQL.\n\n{e}\n\n"
                "Please check your credentials in database.py and ensure "
                "MySQL is running.",
            )
            self.root.destroy()
            return

        # Tkinter variables for form fields
        self._init_vars()

        # Build UI
        self._build_ui()

        # Load initial data
        self.view_students()

    # ─────────────────────────────────────────────
    # Window & variable setup
    # ─────────────────────────────────────────────

    def _setup_window(self):
        self.root.title("Student Management System")
        self.root.geometry("1340x750")
        self.root.minsize(1100, 650)
        self.root.configure(bg=PALETTE["bg_dark"])
        self.root.option_add("*tearOff", False)
        # Centre on screen
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth()  - 1340) // 2
        y = (self.root.winfo_screenheight() -  750) // 2
        self.root.geometry(f"1340x750+{x}+{y}")

    def _init_vars(self):
        self.var_id      = tk.StringVar()
        self.var_name    = tk.StringVar()
        self.var_age     = tk.StringVar()
        self.var_gender  = tk.StringVar()
        self.var_course  = tk.StringVar()
        self.var_email   = tk.StringVar()
        self.var_phone   = tk.StringVar()
        self.var_address = tk.StringVar()
        self.var_date    = tk.StringVar(value=str(date.today()))
        self.var_search  = tk.StringVar()
        self.search_by   = tk.StringVar(value="Name")

    # ─────────────────────────────────────────────
    # UI construction
    # ─────────────────────────────────────────────

    def _build_ui(self):
        """Assemble the full layout."""
        # ── Title bar ────────────────────────────
        title_bar = tk.Frame(self.root, bg=PALETTE["bg_dark"], pady=0)
        title_bar.pack(fill="x", padx=20, pady=(15, 8))

        tk.Label(
            title_bar,
            text="🎓  Student Management System",
            bg=PALETTE["bg_dark"], fg=PALETTE["text_primary"],
            font=FONT_TITLE,
        ).pack(side="left")

        tk.Label(
            title_bar,
            text="MySQL  •  Tkinter  •  Python",
            bg=PALETTE["bg_dark"], fg=PALETTE["text_muted"],
            font=FONT_SMALL,
        ).pack(side="right", padx=5)

        # Thin accent divider
        tk.Frame(self.root, bg=PALETTE["accent"], height=2).pack(fill="x", padx=20, pady=(0, 12))

        # ── Main content (form | table) ──────────
        content = tk.Frame(self.root, bg=PALETTE["bg_dark"])
        content.pack(fill="both", expand=True, padx=20, pady=(0, 15))

        self._build_form(content)
        self._build_table_panel(content)

    # ── Left panel: input form ────────────────────────────────────────────────

    def _build_form(self, parent):
        form_frame = tk.Frame(
            parent, bg=PALETTE["bg_card"],
            highlightthickness=1, highlightbackground=PALETTE["border"],
        )
        form_frame.pack(side="left", fill="y", padx=(0, 12), ipadx=12, ipady=12)

        # Section header
        tk.Label(
            form_frame, text="Student Details",
            bg=PALETTE["bg_card"], fg=PALETTE["accent"],
            font=FONT_HEADER,
        ).grid(row=0, column=0, columnspan=2, sticky="w", padx=16, pady=(12, 10))

        tk.Frame(form_frame, bg=PALETTE["border"], height=1).grid(
            row=1, column=0, columnspan=2, sticky="ew", padx=16, pady=(0, 10)
        )

        fields = [
            ("Student ID",      self.var_id,      "entry",    None),
            ("Full Name *",     self.var_name,    "entry",    None),
            ("Age *",           self.var_age,     "entry",    None),
            ("Gender",          self.var_gender,  "combo",    Student.GENDERS),
            ("Course",          self.var_course,  "combo",    Student.COURSES),
            ("Email",           self.var_email,   "entry",    None),
            ("Phone",           self.var_phone,   "entry",    None),
            ("Address",         self.var_address, "entry",    None),
            ("Admission Date",  self.var_date,    "entry",    None),
        ]

        self.entry_id = None  # keep reference to disable it

        for idx, (label, var, widget_type, options) in enumerate(fields):
            row = idx + 2
            make_label(form_frame, label).grid(
                row=row, column=0, sticky="w", padx=(16, 6), pady=5
            )

            if widget_type == "entry":
                w = make_entry(form_frame, textvariable=var, width=28)
                if label == "Student ID":
                    w.config(state="disabled",
                             disabledforeground=PALETTE["text_muted"],
                             disabledbackground=PALETTE["bg_input"])
                    self.entry_id = w
            else:  # combo
                style_name = "Dark.TCombobox"
                w = ttk.Combobox(
                    form_frame, textvariable=var,
                    values=options, width=26,
                    font=FONT_ENTRY, state="readonly",
                )
                self._style_combobox(w)

            w.grid(row=row, column=1, sticky="ew", padx=(0, 16), pady=5)

        form_frame.columnconfigure(1, weight=1)

        # ── Action buttons ────────────────────────
        tk.Frame(form_frame, bg=PALETTE["border"], height=1).grid(
            row=len(fields) + 2, column=0, columnspan=2,
            sticky="ew", padx=16, pady=(14, 10)
        )

        btn_frame = tk.Frame(form_frame, bg=PALETTE["bg_card"])
        btn_frame.grid(row=len(fields) + 3, column=0, columnspan=2, pady=4, padx=10)

        buttons = [
            ("➕  Add Student",    self.add_student,    PALETTE["accent"],  PALETTE["accent_hover"]),
            ("✏️  Update",          self.update_student, PALETTE["warning"], "#d4893a"),
            ("🗑️  Delete",          self.delete_student, PALETTE["danger"],  PALETTE["danger_hover"]),
            ("🔄  Clear Form",      self.clear_fields,   PALETTE["bg_input"],PALETTE["border"]),
        ]

        for col, (text, cmd, color, hover) in enumerate(buttons[:2]):
            make_button(btn_frame, text, cmd, color, hover, width=17).grid(
                row=0, column=col, padx=4, pady=4
            )
        for col, (text, cmd, color, hover) in enumerate(buttons[2:]):
            make_button(btn_frame, text, cmd, color, hover, width=17).grid(
                row=1, column=col, padx=4, pady=4
            )

        # Exit button at the very bottom
        make_button(
            form_frame, "✖  Exit Application",
            self._on_exit, PALETTE["bg_input"], PALETTE["border"], width=36
        ).grid(
            row=len(fields) + 4, column=0, columnspan=2,
            padx=16, pady=(6, 14), sticky="ew"
        )

    def _style_combobox(self, cb):
        """Apply dark styling to a Combobox."""
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "TCombobox",
            fieldbackground=PALETTE["bg_input"],
            background=PALETTE["bg_input"],
            foreground=PALETTE["text_primary"],
            selectbackground=PALETTE["accent"],
            selectforeground=PALETTE["text_primary"],
            arrowcolor=PALETTE["text_muted"],
            bordercolor=PALETTE["border"],
            lightcolor=PALETTE["bg_input"],
            darkcolor=PALETTE["bg_input"],
        )
        cb.option_add("*TCombobox*Listbox.background", PALETTE["bg_card"])
        cb.option_add("*TCombobox*Listbox.foreground", PALETTE["text_primary"])
        cb.option_add("*TCombobox*Listbox.selectBackground", PALETTE["accent"])
        cb.option_add("*TCombobox*Listbox.selectForeground", PALETTE["text_primary"])

    # ── Right panel: search + treeview ───────────────────────────────────────

    def _build_table_panel(self, parent):
        right = tk.Frame(parent, bg=PALETTE["bg_dark"])
        right.pack(side="left", fill="both", expand=True)

        # Search bar
        search_card = tk.Frame(
            right, bg=PALETTE["bg_card"],
            highlightthickness=1, highlightbackground=PALETTE["border"],
        )
        search_card.pack(fill="x", pady=(0, 10), ipady=8)

        tk.Label(
            search_card, text="Search Students",
            bg=PALETTE["bg_card"], fg=PALETTE["accent"],
            font=FONT_HEADER,
        ).pack(side="left", padx=(16, 12))

        tk.Label(search_card, text="By:", bg=PALETTE["bg_card"],
                 fg=PALETTE["text_muted"], font=FONT_LABEL).pack(side="left")

        for opt in ("Name", "ID"):
            tk.Radiobutton(
                search_card, text=opt, variable=self.search_by, value=opt,
                bg=PALETTE["bg_card"], fg=PALETTE["text_primary"],
                activebackground=PALETTE["bg_card"],
                activeforeground=PALETTE["text_primary"],
                selectcolor=PALETTE["bg_input"],
                font=FONT_LABEL, cursor="hand2",
            ).pack(side="left", padx=4)

        search_entry = make_entry(search_card, textvariable=self.var_search, width=30)
        search_entry.pack(side="left", padx=8)
        search_entry.bind("<Return>", lambda e: self.search_student())

        make_button(search_card, "🔍  Search", self.search_student,
                    PALETTE["accent"], PALETTE["accent_hover"], width=12).pack(side="left", padx=4)
        make_button(search_card, "Show All", self.view_students,
                    PALETTE["bg_input"], PALETTE["border"], width=10).pack(side="left", padx=4)

        # Status label (record count)
        self.status_var = tk.StringVar(value="")
        tk.Label(
            search_card, textvariable=self.status_var,
            bg=PALETTE["bg_card"], fg=PALETTE["text_muted"],
            font=FONT_SMALL,
        ).pack(side="right", padx=16)

        # Treeview card
        table_card = tk.Frame(
            right, bg=PALETTE["bg_card"],
            highlightthickness=1, highlightbackground=PALETTE["border"],
        )
        table_card.pack(fill="both", expand=True)

        self._build_treeview(table_card)

    def _build_treeview(self, parent):
        columns = ("ID", "Name", "Age", "Gender", "Course",
                   "Email", "Phone", "Address", "Admission Date")
        col_widths = (55, 150, 45, 70, 150, 180, 100, 140, 110)

        # Style the Treeview
        style = ttk.Style()
        style.configure(
            "Dark.Treeview",
            background=PALETTE["row_even"],
            foreground=PALETTE["text_primary"],
            fieldbackground=PALETTE["row_even"],
            rowheight=28,
            font=FONT_SMALL,
            borderwidth=0,
        )
        style.configure(
            "Dark.Treeview.Heading",
            background=PALETTE["header_bg"],
            foreground=PALETTE["accent"],
            font=("Segoe UI", 10, "bold"),
            relief="flat",
        )
        style.map(
            "Dark.Treeview",
            background=[("selected", PALETTE["select_bg"])],
            foreground=[("selected", PALETTE["text_primary"])],
        )
        style.map(
            "Dark.Treeview.Heading",
            background=[("active", PALETTE["bg_card"])],
        )

        # Scrollbars
        vsb = ttk.Scrollbar(parent, orient="vertical")
        hsb = ttk.Scrollbar(parent, orient="horizontal")

        self.tree = ttk.Treeview(
            parent,
            columns=columns,
            show="headings",
            yscrollcommand=vsb.set,
            xscrollcommand=hsb.set,
            style="Dark.Treeview",
        )
        vsb.config(command=self.tree.yview)
        hsb.config(command=self.tree.xview)

        for col, width in zip(columns, col_widths):
            self.tree.heading(col, text=col,
                              command=lambda c=col: self._sort_column(c, False))
            self.tree.column(col, width=width, minwidth=40, anchor="center")

        # Alternating row colours
        self.tree.tag_configure("evenrow", background=PALETTE["row_even"])
        self.tree.tag_configure("oddrow",  background=PALETTE["row_odd"])

        vsb.pack(side="right", fill="y")
        hsb.pack(side="bottom", fill="x")
        self.tree.pack(fill="both", expand=True, padx=2, pady=2)

        # Bind row selection → populate form
        self.tree.bind("<<TreeviewSelect>>", self._on_row_select)
        self.tree.bind("<Double-1>", self._on_row_select)

    # ─────────────────────────────────────────────
    # CRUD operations
    # ─────────────────────────────────────────────

    def add_student(self):
        """Validate form and insert a new student into the database."""
        ok, msg = Student.validate(
            self.var_name.get(), self.var_age.get(),
            self.var_email.get(), self.var_phone.get()
        )
        if not ok:
            messagebox.showwarning("Validation Error", msg, parent=self.root)
            return

        try:
            adm_date = Student.parse_date(self.var_date.get())
        except ValueError as e:
            messagebox.showwarning("Validation Error", str(e), parent=self.root)
            return

        try:
            new_id = self.db.add_student(
                name=self.var_name.get().strip(),
                age=int(self.var_age.get()),
                gender=self.var_gender.get(),
                course=self.var_course.get(),
                email=self.var_email.get().strip(),
                phone=self.var_phone.get().strip(),
                address=self.var_address.get().strip(),
                admission_date=adm_date,
            )
            messagebox.showinfo(
                "Success",
                f"Student added successfully!\nStudent ID: {new_id}",
                parent=self.root,
            )
            self.clear_fields()
            self.view_students()
        except RuntimeError as e:
            messagebox.showerror("Database Error", str(e), parent=self.root)

    def view_students(self):
        """Load all students into the Treeview."""
        try:
            rows = self.db.view_students()
            self._populate_tree(rows)
        except RuntimeError as e:
            messagebox.showerror("Database Error", str(e), parent=self.root)

    def update_student(self):
        """Update the currently selected student record."""
        if not self.var_id.get():
            messagebox.showwarning(
                "No Selection",
                "Please select a student from the table first.",
                parent=self.root,
            )
            return

        ok, msg = Student.validate(
            self.var_name.get(), self.var_age.get(),
            self.var_email.get(), self.var_phone.get()
        )
        if not ok:
            messagebox.showwarning("Validation Error", msg, parent=self.root)
            return

        try:
            adm_date = Student.parse_date(self.var_date.get())
        except ValueError as e:
            messagebox.showwarning("Validation Error", str(e), parent=self.root)
            return

        confirm = messagebox.askyesno(
            "Confirm Update",
            f"Update record for Student ID {self.var_id.get()}?",
            parent=self.root,
        )
        if not confirm:
            return

        try:
            affected = self.db.update_student(
                student_id=int(self.var_id.get()),
                name=self.var_name.get().strip(),
                age=int(self.var_age.get()),
                gender=self.var_gender.get(),
                course=self.var_course.get(),
                email=self.var_email.get().strip(),
                phone=self.var_phone.get().strip(),
                address=self.var_address.get().strip(),
                admission_date=adm_date,
            )
            if affected:
                messagebox.showinfo("Success", "Student updated successfully!", parent=self.root)
                self.clear_fields()
                self.view_students()
            else:
                messagebox.showwarning("Not Found", "No matching student found.", parent=self.root)
        except RuntimeError as e:
            messagebox.showerror("Database Error", str(e), parent=self.root)

    def delete_student(self):
        """Delete the selected student after confirmation."""
        if not self.var_id.get():
            messagebox.showwarning(
                "No Selection",
                "Please select a student from the table first.",
                parent=self.root,
            )
            return

        name = self.var_name.get() or f"ID {self.var_id.get()}"
        confirm = messagebox.askyesno(
            "Confirm Delete",
            f"Permanently delete student: {name}?\n\nThis cannot be undone.",
            icon="warning",
            parent=self.root,
        )
        if not confirm:
            return

        try:
            affected = self.db.delete_student(int(self.var_id.get()))
            if affected:
                messagebox.showinfo("Deleted", f"Student '{name}' deleted.", parent=self.root)
                self.clear_fields()
                self.view_students()
            else:
                messagebox.showwarning("Not Found", "No matching student found.", parent=self.root)
        except RuntimeError as e:
            messagebox.showerror("Database Error", str(e), parent=self.root)

    def search_student(self):
        """Search students by ID or Name and display results."""
        query = self.var_search.get().strip()
        if not query:
            messagebox.showwarning(
                "Empty Search", "Enter a name or ID to search.", parent=self.root
            )
            return

        try:
            if self.search_by.get() == "ID":
                if not query.isdigit():
                    messagebox.showwarning(
                        "Invalid ID", "Student ID must be a number.", parent=self.root
                    )
                    return
                rows = self.db.search_by_id(int(query))
            else:
                rows = self.db.search_by_name(query)

            self._populate_tree(rows)

            if not rows:
                messagebox.showinfo(
                    "No Results",
                    f"No students found matching '{query}'.",
                    parent=self.root,
                )
        except RuntimeError as e:
            messagebox.showerror("Database Error", str(e), parent=self.root)

    def clear_fields(self):
        """Reset all form fields to their defaults."""
        self.var_id.set("")
        self.var_name.set("")
        self.var_age.set("")
        self.var_gender.set("")
        self.var_course.set("")
        self.var_email.set("")
        self.var_phone.set("")
        self.var_address.set("")
        self.var_date.set(str(date.today()))
        self.var_search.set("")

    # ─────────────────────────────────────────────
    # Helpers
    # ─────────────────────────────────────────────

    def _populate_tree(self, rows):
        """Clear the Treeview and insert rows with alternating colours."""
        # Remove old rows
        for item in self.tree.get_children():
            self.tree.delete(item)

        for i, row in enumerate(rows):
            tag = "evenrow" if i % 2 == 0 else "oddrow"
            self.tree.insert("", "end", values=row, tags=(tag,))

        count = len(rows)
        self.status_var.set(f"{count} record{'s' if count != 1 else ''} found")

    def _on_row_select(self, event=None):
        """Populate form fields when a Treeview row is clicked."""
        selected = self.tree.selection()
        if not selected:
            return
        values = self.tree.item(selected[0], "values")
        if not values:
            return

        fields = [
            self.var_id, self.var_name, self.var_age, self.var_gender,
            self.var_course, self.var_email, self.var_phone,
            self.var_address, self.var_date,
        ]
        for var, val in zip(fields, values):
            var.set(val)

    def _sort_column(self, col, reverse):
        """Sort Treeview by the clicked column header."""
        data = [
            (self.tree.set(item, col), item)
            for item in self.tree.get_children("")
        ]
        try:
            data.sort(key=lambda x: int(x[0]) if x[0].isdigit() else x[0].lower(),
                      reverse=reverse)
        except Exception:
            data.sort(reverse=reverse)

        for idx, (_, item) in enumerate(data):
            self.tree.move(item, "", idx)
            tag = "evenrow" if idx % 2 == 0 else "oddrow"
            self.tree.item(item, tags=(tag,))

        self.tree.heading(col, command=lambda: self._sort_column(col, not reverse))

    def _on_exit(self):
        """Cleanly close the application."""
        if messagebox.askyesno("Exit", "Exit Student Management System?", parent=self.root):
            self.db.disconnect()
            self.root.destroy()


# ═══════════════════════════════════════════════════════════════════════════════
# Entry point
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    root = tk.Tk()
    app = StudentManagementApp(root)
    root.protocol("WM_DELETE_WINDOW", app._on_exit)
    root.mainloop()
