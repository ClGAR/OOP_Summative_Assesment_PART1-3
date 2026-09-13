import json
import os

from task import Task


class TaskManager:
    def __init__(self):
        self.tasks = []

        folder = os.path.dirname(
            os.path.abspath(__file__)
        )

        self.filename = os.path.join(
            folder,
            "task.json"
        )

        self.old_filename = os.path.join(
            folder,
            "tasks.json"
        )

        self.load_tasks()

    def add_task(self, task):
        self.tasks.append(task)
        self.save_tasks()

    def view_tasks(self):
        if not self.tasks:
            print("\nNo tasks available.")
            return

        for number, task in enumerate(self.tasks, start=1):
            print("\nTask Number:", number)
            task.display()

    def delete_task(self, index):
        if 0 <= index < len(self.tasks):
            deleted = self.tasks.pop(index)

            print("\nDeleted:", deleted.title)

            self.save_tasks()
        else:
            print("Invalid task number.")

    def update_progress(self, index, progress):
        if progress < 0 or progress > 100:
            print(
                "Progress must be between 0 and 100."
            )
            return False

        if 0 <= index < len(self.tasks):
            self.tasks[index].progress = progress

            self.save_tasks()

            print("Task progress updated.")
            return True

        print("Invalid task number.")
        return False

    def mark_complete(self, index):
        if 0 <= index < len(self.tasks):
            self.tasks[index].progress = 100

            self.save_tasks()

            print("Task marked as completed.")
        else:
            print("Invalid task number.")

    def sort_by_risk(self):
        self.tasks.sort(
            key=lambda task: task.calculate_score(),
            reverse=True
        )

    def save_tasks(self):
        data = []

        for task in self.tasks:
            data.append(task.to_dict())

        try:
            with open(self.filename, "w") as file:
                json.dump(data, file, indent=4)
        except OSError as error:
            print("Could not save tasks:", error)

    def load_tasks(self):
        self.tasks = []

        loaded = self._read_task_file(self.filename)

        if loaded is None:
            loaded = self._read_task_file(
                self.old_filename
            )

        if not loaded:
            return

        for task_data in loaded:
            try:
                task = Task.from_dict(task_data)
                self.tasks.append(task)
            except (KeyError, TypeError, ValueError):
                continue

    def _read_task_file(self, path):
        if not os.path.exists(path):
            return None

        try:
            with open(path, "r") as file:
                content = file.read().strip()

            if not content:
                return []

            data = json.loads(content)

            if isinstance(data, list):
                return data

        except (OSError, json.JSONDecodeError):
            return []

        return []