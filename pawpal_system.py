from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Task:
    """Represent a care task for a pet."""

    description: str
    time: str
    duration: int
    priority: str
    frequency: str
    is_complete: bool = False

    def mark_complete(self) -> Task | None:
        """Mark this task as complete and return a new recurring task if Daily.
        
        If frequency is 'Daily', returns a new Task instance with the same
        description, duration, priority, and frequency, with is_complete=False.
        Otherwise returns None.
        """
        self.is_complete = True
        if self.frequency.strip().lower() == "daily":
            return Task(
                description=self.description,
                time=self.time,
                duration=self.duration,
                priority=self.priority,
                frequency=self.frequency,
            )
        return None


@dataclass
class Pet:
    """Represent a pet and its assigned tasks."""

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
    """Represent a pet owner and their pets."""

    name: str
    pets: list[Pet]

    def __init__(self, name: str) -> None:
        """Initialize an owner with a name and no pets."""
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
    """Organize, analyze, and explain pet care tasks."""

    @staticmethod
    def _time_to_minutes(time_value: str) -> int:
        """Convert an HH:MM time string to total minutes."""
        hours_text, minutes_text = time_value.strip().split(":")
        return int(hours_text) * 60 + int(minutes_text)

    @classmethod
    def _task_window(cls, task: Task) -> tuple[int, int]:
        """Return a task time window as start and end minutes."""
        start_minute = cls._time_to_minutes(task.time)
        end_minute = start_minute + task.duration
        return start_minute, end_minute

    def get_all_tasks(self, owner: Owner) -> list[Task]:
        """Retrieve all tasks from an owner's pets."""
        return owner.get_all_tasks()

    def filter_by_pet(self, owner: Owner, pet_name: str) -> list[Task]:
        """Return tasks assigned to the pet with the given name."""
        normalized_pet_name = pet_name.strip().lower()
        for pet in owner.pets:
            if pet.name.strip().lower() == normalized_pet_name:
                return pet.get_tasks()
        return []

    def sort_by_time(self, tasks: list[Task]) -> list[Task]:
        """Return tasks sorted by start time, priority, and duration."""
        priority_ranking = {"high": 0, "medium": 1, "low": 2}
        return sorted(
            tasks,
            key=lambda task: (
                self._time_to_minutes(task.time),
                priority_ranking.get(task.priority.lower(), 3),
                task.duration,
            ),
        )

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
        """Return task pairs that overlap in scheduled time."""
        conflicts: list[tuple[Task, Task]] = []
        sorted_tasks = self.sort_by_time(tasks)

        for index, current_task in enumerate(sorted_tasks):
            current_start, current_end = self._task_window(current_task)
            for next_task in sorted_tasks[index + 1 :]:
                next_start, next_end = self._task_window(next_task)
                if next_start >= current_end:
                    break
                # A conflict means the two task time windows overlap.
                overlap_detected = current_start < next_end and next_start < current_end
                if overlap_detected:
                    conflicts.append((current_task, next_task))

        return conflicts

    def generate_daily_plan(self, tasks: list[Task]) -> list[Task]:
        """Return a daily plan ordered by task start time."""
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
