class Task:
    def __init__(
        self,
        subject,
        title,
        days_remaining,
        estimated_hours,
        priority,
        progress
    ):
        self.subject = subject
        self.title = title
        self.days_remaining = days_remaining
        self.estimated_hours = estimated_hours
        self.priority = priority
        self.progress = progress

    def calculate_score(self):
        if self.progress >= 100:
            return 0

        score = 0

        # Deadline
        if self.days_remaining <= 1:
            score += 4
        elif self.days_remaining <= 3:
            score += 3
        elif self.days_remaining <= 7:
            score += 2
        else:
            score += 1

        # Estimated workload
        if self.estimated_hours >= 8:
            score += 4
        elif self.estimated_hours >= 5:
            score += 3
        elif self.estimated_hours >= 2:
            score += 2
        else:
            score += 1

        # Priority
        if self.priority.lower() == "high":
            score += 3
        elif self.priority.lower() == "medium":
            score += 2
        else:
            score += 1

        # Progress
        if self.progress <= 25:
            score += 3
        elif self.progress <= 60:
            score += 2
        else:
            score += 1

        return score

    def calculate_risk(self):
        if self.progress >= 100:
            return "COMPLETED"

        score = self.calculate_score()

        if score >= 10:
            return "CRITICAL"
        elif score >= 7:
            return "HIGH"
        elif score >= 4:
            return "MODERATE"
        else:
            return "LOW"

    def display(self):
        print("\n-------------------------")
        print("Subject:", self.subject)
        print("Task:", self.title)
        print("Days Remaining:", self.days_remaining)
        print("Estimated Hours:", self.estimated_hours)
        print("Priority:", self.priority)
        print("Progress:", self.progress, "%")
        print("Risk Score:", self.calculate_score())
        print("Risk Level:", self.calculate_risk())
        print("-------------------------")

    def to_dict(self):
        return {
            "subject": self.subject,
            "title": self.title,
            "days_remaining": self.days_remaining,
            "estimated_hours": self.estimated_hours,
            "priority": self.priority,
            "progress": self.progress
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["subject"],
            data["title"],
            data["days_remaining"],
            data["estimated_hours"],
            data["priority"],
            data["progress"]
        )