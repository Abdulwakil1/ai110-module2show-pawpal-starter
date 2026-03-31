classDiagram
class Owner {
+name: str
+pets: list~Pet~ +**init**(name: str)
+add_pet(pet: Pet)
+get_all_tasks() list~Task~
}

    class Pet {
        +name: str
        +species: str
        +tasks: list~Task~
        +add_task(task: Task)
        +get_tasks() list~Task~
    }

    class Task {
        +description: str
        +time: str
        +duration: int
        +priority: str
        +frequency: str
        +is_complete: bool
        +mark_complete() Task | None
    }

    class Scheduler {
        -_time_to_minutes(time_value: str) int
        -_task_window(task: Task) tuple~int, int~
        +get_all_tasks(owner: Owner) list~Task~
        +filter_by_pet(owner: Owner, pet_name: str) list~Task~
        +sort_by_time(tasks: list~Task~) list~Task~
        +filter_tasks(tasks: list~Task~, status: str) list~Task~
        +detect_conflicts(tasks: list~Task~) list~tuple~Task, Task~~
        +generate_daily_plan(tasks: list~Task~) list~Task~
        +explain_plan(tasks: list~Task~) str
    }

    Owner "1" o-- "0..*" Pet : has
    Pet "1" o-- "0..*" Task : has
    Scheduler ..> Owner : uses
    Scheduler ..> Task : analyzes
