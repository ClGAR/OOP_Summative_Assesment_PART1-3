from task import Task
from task_manager import TaskManager


manager = TaskManager()


def add_task():
    print("\n=== ADD TASK ===")

    subject = input("Subject: ").strip()
    title = input("Task Title: ").strip()

    if not subject or not title:
        print("Subject and task title are required.")
        return

    try:
        days = int(input("Days Remaining: "))
        hours = float(input("Estimated Hours Needed: "))
        progress = int(input("Progress (0-100): "))

    except ValueError:
        print("Please enter valid numbers.")
        return

    if days < 0 or hours < 0:
        print("Days and hours cannot be negative.")
        return

    priority = input(
        "Priority (Low/Medium/High): "
    )

    if priority.lower() not in [
        "low",
        "medium",
        "high"
    ]:
        print("Invalid priority.")
        return

    if progress < 0 or progress > 100:
        print(
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

    manager.add_task(task)

    print("\nTask successfully added.")
    print(
        "Risk Level:",
        task.calculate_risk()
    )


def view_tasks():
    manager.view_tasks()


def view_by_risk():
    if not manager.tasks:
        print("No tasks available.")
        return

    manager.sort_by_risk()

    print("\n=== TASKS BY RISK ===")

    manager.view_tasks()


def update_task():
    manager.view_tasks()

    if not manager.tasks:
        return

    try:
        task_number = int(
            input(
                "\nEnter task number: "
            )
        )

        progress = int(
            input(
                "New progress (0-100): "
            )
        )

    except ValueError:
        print("Invalid input.")
        return

    if progress < 0 or progress > 100:
        print(
            "Progress must be between 0 and 100."
        )
        return

    manager.update_progress(
        task_number - 1,
        progress
    )


def complete_task():
    manager.view_tasks()

    if not manager.tasks:
        return

    try:
        task_number = int(
            input(
                "\nEnter task number "
                "to complete: "
            )
        )

    except ValueError:
        print("Invalid input.")
        return

    manager.mark_complete(
        task_number - 1
    )


def delete_task():
    manager.view_tasks()

    if not manager.tasks:
        return

    try:
        task_number = int(
            input(
                "\nEnter task number "
                "to delete: "
            )
        )

    except ValueError:
        print("Invalid input.")
        return

    manager.delete_task(
        task_number - 1
    )


def main():
    while True:
        print("\n========================")
        print("       TASKTRIAGE")
        print("========================")

        print("1. Add Task")
        print("2. View Tasks")
        print("3. View Tasks by Risk")
        print("4. Update Progress")
        print("5. Mark Task Complete")
        print("6. Delete Task")
        print("7. Exit")

        choice = input(
            "\nSelect option: "
        )

        if choice == "1":
            add_task()

        elif choice == "2":
            view_tasks()

        elif choice == "3":
            view_by_risk()

        elif choice == "4":
            update_task()

        elif choice == "5":
            complete_task()

        elif choice == "6":
            delete_task()

        elif choice == "7":
            print(
                "\nThank you for using "
                "TaskTriage."
            )

            break

        else:
            print("Invalid option.")


if __name__ == "__main__":
    main()