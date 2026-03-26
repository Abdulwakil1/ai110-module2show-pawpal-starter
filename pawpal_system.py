from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Task:
    description: str
    time: str
    duration: int
    priority: str
    frequency: str
    is_complete: bool = False

    def mark_complete(self) -> None:
        """Mark this task as complete."""
        self.is_complete = True


@dataclass
class Pet:
    name: str
    species: str
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a new task to this pet."""
        self.tasks.append(task)

    def get_tasks(self) -> list[Task]:
        """Return a copy of this pet's tasks."""
        return list(self.tasks)


class Owner:
    name: str
    pets: list[Pet]

    def __init__(self, name: str) -> None:
        """Initialize an owner with no pets."""
        self.name = name
        self.pets = []

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner."""
        self.pets.append(pet)

    def get_all_tasks(self) -> list[Task]:
        """Return all tasks across all owned pets."""
        all_tasks: list[Task] = []
        for pet in self.pets:
            all_tasks.extend(pet.get_tasks())
        return all_tasks


class Scheduler:
    @staticmethod
    def _time_to_minutes(time_value: str) -> int:
        """Convert an HH:MM time string to total minutes."""
        hours_text, minutes_text = time_value.strip().split(":")
        return int(hours_text) * 60 + int(minutes_text)

    @classmethod
    def _task_window(cls, task: Task) -> tuple[int, int]:
        """Return a task's time window as (start_minute, end_minute)."""
        start_minute = cls._time_to_minutes(task.time)
        end_minute = start_minute + task.duration
        return start_minute, end_minute

    def get_all_tasks(self, owner: Owner) -> list[Task]:
        """Retrieve all tasks from an owner's pets."""
        return owner.get_all_tasks()

    def sort_by_time(self, tasks: list[Task]) -> list[Task]:
        """Return tasks sorted by time in ascending order."""
        return sorted(tasks, key=lambda task: self._time_to_minutes(task.time))

    def filter_tasks(self, tasks: list[Task], status: str) -> list[Task]:
        """Return tasks that match the requested completion status."""
        normalized_status = status.strip().lower()
        if normalized_status in {"complete", "completed", "done", "true"}:
            desired_is_complete = True
        elif normalized_status in {"incomplete", "pending", "open", "false"}:
            desired_is_complete = False
        else:
            raise ValueError("Invalid status. Use 'complete' or 'incomplete'.")
        return [task for task in tasks if task.is_complete == desired_is_complete]

    def detect_conflicts(self, tasks: list[Task]) -> list[tuple[Task, Task]]:
        """Detect overlapping task pairs based on time and duration."""
        conflicts: list[tuple[Task, Task]] = []
        sorted_tasks = self.sort_by_time(tasks)

        for index, current_task in enumerate(sorted_tasks):
            current_start, current_end = self._task_window(current_task)
            for next_task in sorted_tasks[index + 1 :]:
                next_start, next_end = self._task_window(next_task)
                if next_start >= current_end:
                    break
                if current_start < next_end and next_start < current_end:
                    conflicts.append((current_task, next_task))

        return conflicts

    def generate_daily_plan(self, tasks: list[Task]) -> list[Task]:
        """Generate a day plan by ordering tasks chronologically."""
        return self.sort_by_time(tasks)

    def explain_plan(self, tasks: list[Task]) -> str:
        """Return a readable explanation of the daily task plan."""
        ordered_tasks = self.generate_daily_plan(tasks)
        if not ordered_tasks:
            return "No tasks scheduled for today."

        lines: list[str] = ["Daily Plan:"]
        for task in ordered_tasks:
            completion_label = "Done" if task.is_complete else "Pending"
            lines.append(
                f"- {task.time} | {task.description} "
                f"({task.duration} min, {task.priority}, {completion_label})"
            )
        return "\n".join(lines)
