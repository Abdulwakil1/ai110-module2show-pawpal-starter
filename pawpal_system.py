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
        pass


@dataclass
class Pet:
    name: str
    species: str
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        pass

    def get_tasks(self) -> list[Task]:
        pass


class Owner:
    name: str
    pets: list[Pet]

    def __init__(self, name: str) -> None:
        self.name = name
        self.pets = []

    def add_pet(self, pet: Pet) -> None:
        pass

    def get_all_tasks(self) -> list[Task]:
        pass


class Scheduler:
    def get_all_tasks(self, owner: Owner) -> list[Task]:
        pass

    def sort_by_time(self, tasks: list[Task]) -> list[Task]:
        pass

    def filter_tasks(self, tasks: list[Task], status: str) -> list[Task]:
        pass

    def detect_conflicts(self, tasks: list[Task]) -> list[Task]:
        pass

    def generate_daily_plan(self, tasks: list[Task]) -> list[Task]:
        pass

    def explain_plan(self, tasks: list[Task]) -> str:
        pass
