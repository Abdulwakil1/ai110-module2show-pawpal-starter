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
	conflicts = scheduler.detect_conflicts(sorted_tasks)
	daily_plan = scheduler.generate_daily_plan(sorted_tasks)
	explanation = scheduler.explain_plan(daily_plan)

	print("Today's Schedule")
	print("-" * 40)
	for task in daily_plan:
		print(f"- {format_task(task)}")

	print("\nDetected Conflicts")
	print("-" * 40)
	if conflicts:
		for first_task, second_task in conflicts:
			first_pet_name = find_pet_name_for_task(owner, first_task)
			second_pet_name = find_pet_name_for_task(owner, second_task)
			print(
				f"- [{first_pet_name}] {first_task.description} ({first_task.time}) overlaps with "
				f"[{second_pet_name}] {second_task.description} ({second_task.time})"
			)
	else:
		print("No conflicts detected.")

	print("\nPlan Explanation")
	print("-" * 40)
	print(explanation)


if __name__ == "__main__":
	main()
