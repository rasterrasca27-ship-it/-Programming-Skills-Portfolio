import os
import tkinter as tk
from tkinter import ttk, messagebox

DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "studentMarks.txt")


class Student:
    def __init__(self, code, name, c1, c2, c3, exam):
        self.code = int(code)
        self.name = str(name).strip()
        self.c1, self.c2, self.c3, self.exam = int(c1), int(c2), int(c3), int(exam)

        if not (1000 <= self.code <= 9999):
            raise ValueError("Code must be between 1000 and 9999.")
        if not self.name or any(ch in self.name for ch in ",\n\r"):
            raise ValueError("Name cannot be empty or contain commas/newlines.")
        if not all(0 <= m <= 20 for m in (self.c1, self.c2, self.c3)):
            raise ValueError("Coursework marks must be between 0 and 20.")
        if not (0 <= self.exam <= 100):
            raise ValueError("Exam mark must be between 0 and 100.")

    @property
    def coursework(self): return self.c1 + self.c2 + self.c3

    @property
    def overall(self): return self.coursework + self.exam

    @property
    def percentage(self): return (self.overall / 160) * 100

    @property
    def grade(self):
        p = self.percentage
        return "A" if p >= 70 else "B" if p >= 60 else "C" if p >= 50 else "D" if p >= 40 else "F"

    def to_line(self):
        return f"{self.code},{self.name},{self.c1},{self.c2},{self.c3},{self.exam}"

    def summary(self):
        return (f"Student: {self.name} ({self.code}) | Coursework: {self.coursework}/60 | "
                f"Exam: {self.exam}/100 | Overall: {self.overall}/160 ({self.percentage:.1f}%) | Grade: {self.grade}")


class StudentFormDialog(tk.Toplevel):
    """Single reusable form for both Adding and Updating a student."""
    def __init__(self, parent, title, student=None):
        super().__init__(parent)
        self.title(title)
        self.resizable(False, False)
        self.result = None
        self.transient(parent)
        self.grab_set()

        fields = [("Code (1000-9999):", student.code if student else ""),
                  ("Name:", student.name if student else ""),
                  ("Coursework 1 (0-20):", student.c1 if student else ""),
                  ("Coursework 2 (0-20):", student.c2 if student else ""),
                  ("Coursework 3 (0-20):", student.c3 if student else ""),
                  ("Exam (0-100):", student.exam if student else "")]

        self.vars = []
        frm = ttk.Frame(self, padding=12)
        frm.pack()
        for r, (label, val) in enumerate(fields):
            ttk.Label(frm, text=label).grid(row=r, column=0, sticky="w", pady=3)
            var = tk.StringVar(value=str(val))
            ttk.Entry(frm, textvariable=var, width=24).grid(row=r, column=1, pady=3)
            self.vars.append(var)

        btns = ttk.Frame(frm)
        btns.grid(row=len(fields), columnspan=2, pady=(10, 0))
        ttk.Button(btns, text="Save", command=self.on_save).pack(side="left", padx=5)
        ttk.Button(btns, text="Cancel", command=self.destroy).pack(side="left", padx=5)
        self.wait_window()

    def on_save(self):
        try:
            self.result = Student(*[v.get().strip() for v in self.vars])
            self.destroy()
        except ValueError as e:
            messagebox.showerror("Invalid Input", str(e), parent=self)


class StudentManagerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Student Manager")
        self.geometry("850x500")
        self.students = self.load_data()
        if self.students is None:
            self.destroy()
            return
        self.build_ui()
        self.refresh_table()

    def load_data(self):
        if not os.path.exists(DATA_FILE):
            self.save_data([])
            return []
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                lines = [l.strip() for l in f if l.strip()]
            count = int(lines[0])
            students = [Student(*line.split(",")) for line in lines[1:]]
            if count != len(students):
                raise ValueError(f"Header says {count} students, found {len(students)}.")
            return students
        except Exception as e:
            messagebox.showerror("File Error", f"Could not load studentMarks.txt:\n{e}")
            return None

    def save_data(self, students=None):
        data = self.students if students is None else students
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            f.write(f"{len(data)}\n" + "\n".join(s.to_line() for s in data) + ("\n" if data else ""))

    def build_ui(self):
        # Menu bar
        menubar = tk.Menu(self)
        view_m = tk.Menu(menubar, tearoff=0)
        view_m.add_command(label="View All Summary", command=self.view_all)
        view_m.add_command(label="Highest Overall Mark", command=lambda: self.show_extreme(max))
        view_m.add_command(label="Lowest Overall Mark", command=lambda: self.show_extreme(min))
        menubar.add_cascade(label="View", menu=view_m)

        sort_m = tk.Menu(menubar, tearoff=0)
        sort_m.add_command(label="Sort Ascending", command=lambda: self.sort_by_mark(False))
        sort_m.add_command(label="Sort Descending", command=lambda: self.sort_by_mark(True))
        menubar.add_cascade(label="Sort", menu=sort_m)

        edit_m = tk.Menu(menubar, tearoff=0)
        edit_m.add_command(label="Add Student", command=self.add_student)
        edit_m.add_command(label="Update Selected", command=self.update_student)
        edit_m.add_command(label="Delete Selected", command=self.delete_student)
        menubar.add_cascade(label="Edit", menu=edit_m)
        self.config(menu=menubar)

        # Top Search Bar
        top = ttk.Frame(self, padding=(8, 6))
        top.pack(fill="x")
        ttk.Label(top, text="Find (Code or Name):").pack(side="left")
        self.search_var = tk.StringVar()
        ttk.Entry(top, textvariable=self.search_var, width=25).pack(side="left", padx=6)
        ttk.Button(top, text="Search", command=self.search_student).pack(side="left")
        ttk.Button(top, text="Show All", command=self.refresh_table).pack(side="left", padx=4)

        # Table
        cols = ("Name", "Code", "Coursework /60", "Exam /100", "Overall /160", "Percentage", "Grade")
        self.tree = ttk.Treeview(self, columns=cols, show="headings", height=13)
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=150 if c == "Name" else 95, anchor="w" if c == "Name" else "center")
        self.tree.pack(fill="both", expand=True, padx=8)
        self.tree.tag_configure("A", background="#d6f5d6")
        self.tree.tag_configure("F", background="#f8d7da")
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

        # Details Box & Status Bar
        self.details = tk.Text(self, height=6, state="disabled", font=("Consolas", 10))
        self.details.pack(fill="x", padx=8, pady=6)
        self.status = tk.StringVar()
        ttk.Label(self, textvariable=self.status, relief="sunken", padding=4).pack(fill="x", side="bottom")

    def refresh_table(self, subset=None):
        records = self.students if subset is None else subset
        self.tree.delete(*self.tree.get_children())
        for s in records:
            vals = (s.name, s.code, f"{s.coursework}/60", f"{s.exam}/100", f"{s.overall}/160", f"{s.percentage:.1f}%", s.grade)
            self.tree.insert("", "end", iid=str(s.code), values=vals, tags=(s.grade,))
        avg = sum(s.percentage for s in self.students) / len(self.students) if self.students else 0
        self.status.set(f"Total Students: {len(self.students)}   |   Class Average: {avg:.1f}%")

    def set_details(self, text):
        self.details.config(state="normal")
        self.details.delete("1.0", "end")
        self.details.insert("1.0", text)
        self.details.config(state="disabled")

    def get_selected_student(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showinfo("Select Student", "Click a student in the table first.")
            return None
        code = int(sel[0])
        return next((s for s in self.students if s.code == code), None)

    def on_select(self, _event):
        s = self.get_selected_student()
        if s:
            self.set_details(s.summary())

    def search_student(self):
        q = self.search_var.get().strip().lower()
        if not q:
            return self.refresh_table()
        matches = [s for s in self.students if q in s.name.lower() or q == str(s.code)]
        self.refresh_table(matches)
        self.set_details(matches[0].summary() if matches else "No matching student found.")

    def view_all(self):
        self.refresh_table()
        if not self.students:
            return self.set_details("No records available.")
        avg = sum(s.percentage for s in self.students) / len(self.students)
        report = "\n".join(s.summary() for s in self.students)
        self.set_details(f"{report}\n{'-'*60}\nTotal: {len(self.students)} | Average: {avg:.1f}%")

    def show_extreme(self, func):
        if self.students:
            self.set_details(func(self.students, key=lambda s: s.overall).summary())

    def sort_by_mark(self, descending):
        self.students.sort(key=lambda s: s.overall, reverse=descending)
        self.view_all()

    def add_student(self):
        dlg = StudentFormDialog(self, "Add Student")
        if dlg.result:
            if any(s.code == dlg.result.code for s in self.students):
                return messagebox.showerror("Duplicate", f"Code {dlg.result.code} already exists.")
            self.students.append(dlg.result)
            self.save_data()
            self.refresh_table()

    def update_student(self):
        student = self.get_selected_student()
        if not student:
            return
        dlg = StudentFormDialog(self, "Update Student", student)
        if dlg.result:
            if dlg.result.code != student.code and any(s.code == dlg.result.code for s in self.students):
                return messagebox.showerror("Duplicate", f"Code {dlg.result.code} already exists.")
            idx = self.students.index(student)
            self.students[idx] = dlg.result
            self.save_data()
            self.refresh_table()
            self.set_details(dlg.result.summary())

    def delete_student(self):
        student = self.get_selected_student()
        if student and messagebox.askyesno("Confirm", f"Delete {student.name} ({student.code})?"):
            self.students.remove(student)
            self.save_data()
            self.refresh_table()
            self.set_details("")


if __name__ == "__main__":
    StudentManagerApp().mainloop()