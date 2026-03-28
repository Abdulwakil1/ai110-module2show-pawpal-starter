from pawpal_system import Owner, Pet, Scheduler, Task


def format_task(task: Task) -> str:
	status_label = "Done" if task.is_complete else "Pending"
	return (
		f"[{task.time}] {task.description} "
		f"({task.duration} min, Priority: {task.priority}, {status_label})"
	)


def find_pet_name_for_task(owner: Owner, target_task: Task) -> str:
	for pet in owner.pets:
		for pet_task in pet.tasks:
			if pet_task is target_task:
				return pet.name
	return "Unknown"


def main() -> None:
	owner = Owner("Amina")

	dog = Pet(name="Buddy", species="Dog")
	cat = Pet(name="Luna", species="Cat")

	dog.add_task(
		Task(
			description="Evening walk",
			time="18:00",
			duration=25,
			priority="Medium",
			frequency="Daily",
		)
	)
	dog.add_task(
		Task(
			description="Morning walk",
			time="08:00",
			duration=30,
			priority="High",
			frequency="Daily",
		)
	)
	dog.add_task(
		Task(
			description="Breakfast feeding",
			time="08:15",
			duration=10,
			priority="Medium",
			frequency="Daily",
		)
	)
	cat.add_task(
		Task(
			description="Dinner feeding",
			time="19:00",
			duration=10,
			priority="Medium",
			frequency="Daily",
		)
	)
	cat.add_task(
		Task(
			description="Litter box cleaning",
			time="09:00",
			duration=15,
			priority="Low",
			frequency="Daily",
		)
	)

	owner.add_pet(dog)
	owner.add_pet(cat)

	scheduler = Scheduler()

	all_tasks = scheduler.get_all_tasks(owner)
	sorted_tasks = scheduler.sort_by_time(all_tasks)

	print("Sorted Tasks")
	print("-" * 40)
	for task in sorted_tasks:
		print(f"- {format_task(task)}")

	conflicts = scheduler.detect_conflicts(all_tasks)

	print("\nConflicts")
	print("-" * 40)
	if conflicts:
		for task1, task2 in conflicts:
			print(
				f"{task1.description} ({task1.time}) "
				f"conflicts with {task2.description} ({task2.time})"
			)
	else:
		print("No conflicts detected")

	target_pet_name = "Buddy"
	pet_tasks = scheduler.filter_by_pet(owner, target_pet_name)
	sorted_pet_tasks = scheduler.sort_by_time(pet_tasks)

	print(f"\nTasks for {target_pet_name}")
	print("-" * 40)
	if sorted_pet_tasks:
		for task in sorted_pet_tasks:
			print(f"- {format_task(task)}")
	else:
		print("No tasks found for this pet.")


if __name__ == "__main__":
	main()
