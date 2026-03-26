classDiagram
class Owner {
+name: str
+pets: list~Pet~
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
        +mark_complete()
    }

    class Scheduler {
        +get_all_tasks(owner: Owner) list~Task~
        +sort_by_time(tasks: list~Task~) list~Task~
        +filter_tasks(tasks: list~Task~, status: str) list~Task~
        +detect_conflicts(tasks: list~Task~) list~Task~
        +generate_daily_plan(tasks: list~Task~) list~Task~
        +explain_plan(tasks: list~Task~) str
    }

    Owner "1" o-- "*" Pet : has
    Pet "1" o-- "*" Task : has
    Scheduler ..> Owner : retrieves tasks from
