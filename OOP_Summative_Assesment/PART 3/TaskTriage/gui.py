import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

from task import Task
from task_manager import TaskManager


class TaskTriageGUI:
    def __init__(self, root):
        self.root = root
        self.manager = TaskManager()

        self.root.title("TaskTriage")
        self.root.geometry("1150x720")
        self.root.minsize(1000, 650)
        self.root.configure(bg="#F4F6F8")

        self.setup_styles()
        self.build_header()
        self.build_summary()
        self.build_main_content()
        self.build_actions()
        self.build_status_bar()

        self.refresh_table()

    # =========================================================
    # STYLES
    # =========================================================

    def setup_styles(self):
        style = ttk.Style()

        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure(
            "Treeview",
            background="white",
            fieldbackground="white",
            rowheight=34,
            font=("Segoe UI", 10),
            borderwidth=0
        )

        style.configure(
            "Treeview.Heading",
            font=("Segoe UI", 10, "bold"),
            background="#E9EEF5",
            foreground="#1E293B",
            padding=8
        )

        style.map(
            "Treeview",
            background=[("selected", "#DCEBFF")],
            foreground=[("selected", "#0F172A")]
        )

        style.configure(
            "Primary.TButton",
            font=("Segoe UI", 10, "bold"),
            padding=(14, 8)
        )

        style.configure(
            "Secondary.TButton",
            font=("Segoe UI", 10),
            padding=(12, 7)
        )

    # =========================================================
    # HEADER
    # =========================================================

    def build_header(self):
        header = tk.Frame(
            self.root,
            bg="#172554",
            height=95
        )

        header.pack(
            fill="x"
        )

        header.pack_propagate(False)

        text_frame = tk.Frame(
            header,
            bg="#172554"
        )

        text_frame.pack(
            side="left",
            padx=35,
            pady=18
        )

        tk.Label(
            text_frame,
            text="TaskTriage",
            font=("Segoe UI", 25, "bold"),
            fg="white",
            bg="#172554"
        ).pack(
            anchor="w"
        )

        tk.Label(
            text_frame,
            text="Academic Deadline Risk & Workload Planner",
            font=("Segoe UI", 10),
            fg="#BFDBFE",
            bg="#172554"
        ).pack(
            anchor="w"
        )

    # =========================================================
    # SUMMARY CARDS
    # =========================================================

    def build_summary(self):
        summary = tk.Frame(
            self.root,
            bg="#F4F6F8"
        )

        summary.pack(
            fill="x",
            padx=28,
            pady=(20, 10)
        )

        self.total_value = self.create_summary_card(
            summary,
            "TOTAL TASKS"
        )

        self.critical_value = self.create_summary_card(
            summary,
            "CRITICAL"
        )

        self.high_value = self.create_summary_card(
            summary,
            "HIGH RISK"
        )

        self.completed_value = self.create_summary_card(
            summary,
            "COMPLETED"
        )

    def create_summary_card(self, parent, title):
        card = tk.Frame(
            parent,
            bg="white",
            highlightbackground="#DDE3EA",
            highlightthickness=1
        )

        card.pack(
            side="left",
            expand=True,
            fill="x",
            padx=6
        )

        tk.Label(
            card,
            text=title,
            font=("Segoe UI", 9, "bold"),
            fg="#64748B",
            bg="white"
        ).pack(
            anchor="w",
            padx=18,
            pady=(13, 2)
        )

        value = tk.Label(
            card,
            text="0",
            font=("Segoe UI", 22, "bold"),
            fg="#0F172A",
            bg="white"
        )

        value.pack(
            anchor="w",
            padx=18,
            pady=(0, 12)
        )

        return value

    # =========================================================
    # MAIN CONTENT
    # =========================================================

    def build_main_content(self):
        content = tk.Frame(
            self.root,
            bg="#F4F6F8"
        )

        content.pack(
            fill="both",
            expand=True,
            padx=28,
            pady=10
        )

        content.columnconfigure(
            0,
            weight=0
        )

        content.columnconfigure(
            1,
            weight=1
        )

        content.rowconfigure(
            0,
            weight=1
        )

        self.build_form(content)
        self.build_table(content)

    # =========================================================
    # ADD TASK PANEL
    # =========================================================

    def build_form(self, parent):
        panel = tk.Frame(
            parent,
            bg="white",
            width=310,
            highlightbackground="#DDE3EA",
            highlightthickness=1
        )

        panel.grid(
            row=0,
            column=0,
            sticky="ns",
            padx=(0, 15)
        )

        panel.grid_propagate(False)

        tk.Label(
            panel,
            text="Add New Task",
            font=("Segoe UI", 15, "bold"),
            bg="white",
            fg="#0F172A"
        ).pack(
            anchor="w",
            padx=22,
            pady=(20, 4)
        )

        tk.Label(
            panel,
            text="Enter the academic task details.",
            font=("Segoe UI", 9),
            bg="white",
            fg="#64748B"
        ).pack(
            anchor="w",
            padx=22,
            pady=(0, 18)
        )

        self.subject_entry = self.create_entry(
            panel,
            "Subject"
        )

        self.title_entry = self.create_entry(
            panel,
            "Task Name"
        )

        self.days_entry = self.create_entry(
            panel,
            "Days Remaining"
        )

        self.hours_entry = self.create_entry(
            panel,
            "Estimated Hours"
        )

        self.create_label(
            panel,
            "Priority"
        )

        self.priority_box = ttk.Combobox(
            panel,
            values=[
                "Low",
                "Medium",
                "High"
            ],
            state="readonly",
            font=("Segoe UI", 10)
        )

        self.priority_box.pack(
            fill="x",
            padx=22,
            pady=(0, 12)
        )

        self.priority_box.set("Medium")

        self.progress_entry = self.create_entry(
            panel,
            "Progress %"
        )

        self.progress_entry.insert(
            0,
            "0"
        )

        ttk.Button(
            panel,
            text="＋  Add Task",
            style="Primary.TButton",
            command=self.add_task
        ).pack(
            fill="x",
            padx=22,
            pady=(15, 10)
        )

        ttk.Button(
            panel,
            text="Clear Form",
            style="Secondary.TButton",
            command=self.clear_form
        ).pack(
            fill="x",
            padx=22
        )

    def create_label(self, parent, text):
        tk.Label(
            parent,
            text=text,
            font=("Segoe UI", 9, "bold"),
            bg="white",
            fg="#475569"
        ).pack(
            anchor="w",
            padx=22,
            pady=(5, 4)
        )

    def create_entry(self, parent, label):
        self.create_label(
            parent,
            label
        )

        entry = ttk.Entry(
            parent,
            font=("Segoe UI", 10)
        )

        entry.pack(
            fill="x",
            padx=22,
            pady=(0, 9),
            ipady=4
        )

        return entry

    # =========================================================
    # TASK TABLE
    # =========================================================

    def build_table(self, parent):
        table_panel = tk.Frame(
            parent,
            bg="white",
            highlightbackground="#DDE3EA",
            highlightthickness=1
        )

        table_panel.grid(
            row=0,
            column=1,
            sticky="nsew"
        )

        title_area = tk.Frame(
            table_panel,
            bg="white"
        )

        title_area.pack(
            fill="x",
            padx=20,
            pady=(18, 10)
        )

        tk.Label(
            title_area,
            text="Academic Tasks",
            font=("Segoe UI", 15, "bold"),
            fg="#0F172A",
            bg="white"
        ).pack(
            side="left"
        )

        self.task_count_label = tk.Label(
            title_area,
            text="0 tasks",
            font=("Segoe UI", 9),
            fg="#64748B",
            bg="white"
        )

        self.task_count_label.pack(
            side="left",
            padx=10
        )

        table_container = tk.Frame(
            table_panel,
            bg="white"
        )

        table_container.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=(0, 15)
        )

        columns = (
            "subject",
            "task",
            "days",
            "hours",
            "priority",
            "progress",
            "risk"
        )

        self.table = ttk.Treeview(
            table_container,
            columns=columns,
            show="headings",
            selectmode="browse"
        )

        headings = {
            "subject": "Subject",
            "task": "Task",
            "days": "Days Left",
            "hours": "Hours",
            "priority": "Priority",
            "progress": "Progress",
            "risk": "Risk"
        }

        for column in columns:
            self.table.heading(
                column,
                text=headings[column]
            )

        self.table.column(
            "subject",
            width=110,
            anchor="w"
        )

        self.table.column(
            "task",
            width=220,
            anchor="w"
        )

        self.table.column(
            "days",
            width=80,
            anchor="center"
        )

        self.table.column(
            "hours",
            width=80,
            anchor="center"
        )

        self.table.column(
            "priority",
            width=90,
            anchor="center"
        )

        self.table.column(
            "progress",
            width=90,
            anchor="center"
        )

        self.table.column(
            "risk",
            width=100,
            anchor="center"
        )

        scrollbar = ttk.Scrollbar(
            table_container,
            orient="vertical",
            command=self.table.yview
        )

        self.table.configure(
            yscrollcommand=scrollbar.set
        )

        self.table.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        # Risk colors
        self.table.tag_configure(
            "CRITICAL",
            background="#FEE2E2",
            foreground="#991B1B"
        )

        self.table.tag_configure(
            "HIGH",
            background="#FFEDD5",
            foreground="#9A3412"
        )

        self.table.tag_configure(
            "MODERATE",
            background="#FEF9C3",
            foreground="#854D0E"
        )

        self.table.tag_configure(
            "LOW",
            background="#DCFCE7",
            foreground="#166534"
        )

        self.table.tag_configure(
            "COMPLETED",
            background="#E2E8F0",
            foreground="#475569"
        )

    # =========================================================
    # ACTION BUTTONS
    # =========================================================

    def build_actions(self):
        actions = tk.Frame(
            self.root,
            bg="#F4F6F8"
        )

        actions.pack(
            fill="x",
            padx=28,
            pady=(0, 15)
        )

        ttk.Button(
            actions,
            text="Sort by Risk",
            style="Secondary.TButton",
            command=self.sort_tasks
        ).pack(
            side="left",
            padx=(0, 8)
        )

        ttk.Button(
            actions,
            text="Update Progress",
            style="Secondary.TButton",
            command=self.update_progress
        ).pack(
            side="left",
            padx=8
        )

        ttk.Button(
            actions,
            text="✓ Mark Complete",
            style="Secondary.TButton",
            command=self.complete_task
        ).pack(
            side="left",
            padx=8
        )

        ttk.Button(
            actions,
            text="Delete Task",
            style="Secondary.TButton",
            command=self.delete_task
        ).pack(
            side="left",
            padx=8
        )

    # =========================================================
    # STATUS BAR
    # =========================================================

    def build_status_bar(self):
        self.status_label = tk.Label(
            self.root,
            text="Ready",
            anchor="w",
            font=("Segoe UI", 9),
            fg="#64748B",
            bg="#E9EEF5",
            padx=15,
            pady=6
        )

        self.status_label.pack(
            fill="x",
            side="bottom"
        )

    # =========================================================
    # FUNCTIONS
    # =========================================================

    def add_task(self):
        try:
            subject = self.subject_entry.get().strip()
            title = self.title_entry.get().strip()

            if not subject or not title:
                messagebox.showerror(
                    "Missing Information",
                    "Subject and task name are required."
                )
                return

            days = int(
                self.days_entry.get()
            )

            hours = float(
                self.hours_entry.get()
            )

            priority = self.priority_box.get()

            progress = int(
                self.progress_entry.get()
            )

            if days < 0:
                messagebox.showerror(
                    "Invalid Days",
                    "Days remaining cannot be negative."
                )
                return

            if hours < 0:
                messagebox.showerror(
                    "Invalid Hours",
                    "Estimated hours cannot be negative."
                )
                return

            if progress < 0 or progress > 100:
                messagebox.showerror(
                    "Invalid Progress",
                    "Progress must be between 0 and 100."
                )
                return

            task = Task(
                subject,
                title,
                days,
                hours,
                priority,
                progress
            )

            self.manager.add_task(task)

            self.clear_form()
            self.refresh_table()

            self.status_label.config(
                text=f"Added task: {title}"
            )

        except ValueError:
            messagebox.showerror(
                "Invalid Input",
                "Days, hours, and progress must contain valid numbers."
            )

    def refresh_table(self):
        for row in self.table.get_children():
            self.table.delete(row)

        for task in self.manager.tasks:
            risk = task.calculate_risk()

            self.table.insert(
                "",
                "end",
                values=(
                    task.subject,
                    task.title,
                    task.days_remaining,
                    f"{task.estimated_hours:g}",
                    task.priority,
                    f"{task.progress}%",
                    risk
                ),
                tags=(risk,)
            )

        self.update_summary()

    def update_summary(self):
        total = len(
            self.manager.tasks
        )

        critical = 0
        high = 0
        completed = 0

        for task in self.manager.tasks:
            risk = task.calculate_risk()

            if risk == "CRITICAL":
                critical += 1

            elif risk == "HIGH":
                high += 1

            elif risk == "COMPLETED":
                completed += 1

        self.total_value.config(
            text=str(total)
        )

        self.critical_value.config(
            text=str(critical)
        )

        self.high_value.config(
            text=str(high)
        )

        self.completed_value.config(
            text=str(completed)
        )

        self.task_count_label.config(
            text=f"{total} task"
            if total == 1
            else f"{total} tasks"
        )

    def clear_form(self):
        self.subject_entry.delete(
            0,
            tk.END
        )

        self.title_entry.delete(
            0,
            tk.END
        )

        self.days_entry.delete(
            0,
            tk.END
        )

        self.hours_entry.delete(
            0,
            tk.END
        )

        self.priority_box.set(
            "Medium"
        )

        self.progress_entry.delete(
            0,
            tk.END
        )

        self.progress_entry.insert(
            0,
            "0"
        )

    def get_selected_index(self):
        selected = self.table.selection()

        if not selected:
            messagebox.showwarning(
                "No Task Selected",
                "Select a task from the table first."
            )
            return None

        return self.table.index(
            selected[0]
        )

    def sort_tasks(self):
        self.manager.sort_by_risk()
        self.refresh_table()

        self.status_label.config(
            text="Tasks sorted from highest to lowest risk."
        )

    def update_progress(self):
        index = self.get_selected_index()

        if index is None:
            return

        task = self.manager.tasks[index]

        progress = simpledialog.askinteger(
            "Update Progress",
            f"{task.title}\n\nEnter progress from 0 to 100:",
            minvalue=0,
            maxvalue=100
        )

        if progress is None:
            return

        self.manager.update_progress(
            index,
            progress
        )

        self.refresh_table()

        self.status_label.config(
            text=f"Updated progress for {task.title}."
        )

    def complete_task(self):
        index = self.get_selected_index()

        if index is None:
            return

        task = self.manager.tasks[index]

        confirm = messagebox.askyesno(
            "Complete Task",
            f"Mark '{task.title}' as completed?"
        )

        if not confirm:
            return

        self.manager.mark_complete(
            index
        )

        self.refresh_table()

        self.status_label.config(
            text=f"Completed: {task.title}"
        )

    def delete_task(self):
        index = self.get_selected_index()

        if index is None:
            return

        task = self.manager.tasks[index]

        confirm = messagebox.askyesno(
            "Delete Task",
            f"Delete '{task.title}'?\n\nThis cannot be undone."
        )

        if not confirm:
            return

        self.manager.delete_task(
            index
        )

        self.refresh_table()

        self.status_label.config(
            text=f"Deleted task: {task.title}"
        )


def main():
    if sys.platform.startswith("linux") and not (
        os.environ.get("DISPLAY")
        or os.environ.get("WAYLAND_DISPLAY")
    ):
        print(
            "TaskTriage GUI requires a graphical display, but none is available."
        )
        print(
            "In Codespaces, run this program with: xvfb-run -a python gui.py"
        )
        return

    try:
        root = tk.Tk()
    except tk.TclError as error:
        print(
            "Unable to start the TaskTriage GUI because no usable display is available."
        )
        print(
            "In Codespaces, install Xvfb and run: xvfb-run -a python gui.py"
        )
        print(f"Tkinter details: {error}")
        return

    app = TaskTriageGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()