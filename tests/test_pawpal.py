"""Quick tests for PawPal+ core classes.

Covers:
1. Task completion behavior
2. Task addition to a pet
"""

import pytest
import main as pawpal_main

from pawpal_system import Owner, Pet, Scheduler, Task


def test_task_completion() -> None:
	"""Verify that mark_complete() updates the task's status."""
	task = Task(
		description="Feed dog",
		time="08:00",
		duration=10,
		priority="High",
		frequency="Daily",
	)

	assert task.is_complete is False

	next_task = task.mark_complete()

	assert task.is_complete is True
	assert next_task is not None


def test_task_completion_is_idempotent() -> None:
	"""Verify repeated completion calls keep task completed."""
	task = Task(
		description="Check water",
		time="07:30",
		duration=5,
		priority="Low",
		frequency="Daily",
	)

	task.mark_complete()
	task.mark_complete()

	assert task.is_complete is True


def test_add_task_to_pet() -> None:
	"""Verify that adding a task updates a pet's task list."""
	pet = Pet(name="Buddy", species="Dog")
	initial_tasks = pet.get_tasks()

	assert initial_tasks == []

	new_task = Task(
		description="Walk dog",
		time="09:00",
		duration=30,
		priority="Medium",
		frequency="Daily",
	)

	pet.add_task(new_task)
	tasks_after_add = pet.get_tasks()

	assert len(tasks_after_add) == len(initial_tasks) + 1
	assert tasks_after_add[0] is new_task


def test_get_tasks_returns_copy_not_internal_list() -> None:
	"""Verify callers cannot mutate pet.tasks through get_tasks() output."""
	pet = Pet(name="Luna", species="Cat")
	task = Task(
		description="Brush fur",
		time="10:00",
		duration=10,
		priority="Low",
		frequency="Weekly",
	)
	pet.add_task(task)

	tasks_view = pet.get_tasks()
	tasks_view.clear()

	assert len(tasks_view) == 0
	assert len(pet.get_tasks()) == 1
	assert pet.get_tasks()[0] is task


@pytest.mark.parametrize(
	"description,time,duration,priority,frequency",
	[
		("Feed cat", "06:45", 5, "High", "Daily"),
		("Evening walk", "18:30", 25, "Medium", "Daily"),
	],
)
def test_add_multiple_tasks_to_pet(
	description: str,
	time: str,
	duration: int,
	priority: str,
	frequency: str,
) -> None:
	"""Verify each added task appears in the pet task list."""
	pet = Pet(name="Milo", species="Dog")
	task = Task(
		description=description,
		time=time,
		duration=duration,
		priority=priority,
		frequency=frequency,
	)

	pet.add_task(task)

	assert task in pet.get_tasks()


def test_filter_by_pet_returns_matching_tasks_and_empty_when_missing() -> None:
	"""Verify Scheduler.filter_by_pet returns tasks for matching pet only."""
	owner = Owner("Amina")
	dog = Pet(name="Buddy", species="Dog")
	cat = Pet(name="Luna", species="Cat")

	dog_task = Task(
		description="Morning walk",
		time="08:00",
		duration=30,
		priority="High",
		frequency="Daily",
	)
	cat_task = Task(
		description="Litter cleaning",
		time="09:00",
		duration=15,
		priority="Medium",
		frequency="Daily",
	)

	dog.add_task(dog_task)
	cat.add_task(cat_task)
	owner.add_pet(dog)
	owner.add_pet(cat)

	scheduler = Scheduler()

	buddy_tasks = scheduler.filter_by_pet(owner, "Buddy")
	assert buddy_tasks == [dog_task]

	missing_pet_tasks = scheduler.filter_by_pet(owner, "Mochi")
	assert missing_pet_tasks == []


def test_filter_by_pet_is_case_insensitive() -> None:
	"""Verify Scheduler.filter_by_pet matches pet names ignoring case."""
	owner = Owner("Amina")
	dog = Pet(name="Buddy", species="Dog")
	dog_task = Task(
		description="Morning walk",
		time="08:00",
		duration=30,
		priority="High",
		frequency="Daily",
	)
	dog.add_task(dog_task)
	owner.add_pet(dog)

	scheduler = Scheduler()

	buddy_tasks_lowercase = scheduler.filter_by_pet(owner, "buddy")
	assert buddy_tasks_lowercase == [dog_task]


def test_mark_complete_daily_returns_new_task() -> None:
	"""Verify mark_complete() returns a new Task with same properties for Daily frequency."""
	task = Task(
		description="Morning walk",
		time="08:00",
		duration=30,
		priority="High",
		frequency="Daily",
	)

	assert task.is_complete is False

	next_task = task.mark_complete()

	assert task.is_complete is True
	assert next_task is not None
	assert next_task.description == "Morning walk"
	assert next_task.time == "08:00"
	assert next_task.duration == 30
	assert next_task.priority == "High"
	assert next_task.frequency == "Daily"
	assert next_task.is_complete is False
	assert next_task is not task


def test_mark_complete_weekly_returns_none() -> None:
	"""Verify mark_complete() returns None for non-Daily frequency."""
	task = Task(
		description="Groom dog",
		time="10:00",
		duration=45,
		priority="Medium",
		frequency="Weekly",
	)

	assert task.is_complete is False

	next_task = task.mark_complete()

	assert task.is_complete is True
	assert next_task is None


def test_main_prints_conflicts_section_with_overlap(capsys: pytest.CaptureFixture[str]) -> None:
	"""Verify main() prints the conflicts section and overlap details."""
	pawpal_main.main()
	captured = capsys.readouterr().out

	assert "Conflicts" in captured
	assert (
		"Morning walk (08:00) conflicts with Breakfast feeding (08:15)"
		in captured
	)


def test_main_prints_no_conflicts_message_when_none_found(
	monkeypatch: pytest.MonkeyPatch,
	capsys: pytest.CaptureFixture[str],
) -> None:
	"""Verify main() prints fallback text when no conflicts are detected."""
	monkeypatch.setattr(Scheduler, "detect_conflicts", lambda self, tasks: [])

	pawpal_main.main()
	captured = capsys.readouterr().out

	assert "Conflicts" in captured
	assert "No conflicts detected" in captured


"""Additional scheduler behavior tests:
- sorting (time and priority),
- conflict detection (overlap vs back-to-back),
- pet filtering (including case-insensitive matching),
- empty-input handling.
"""


def test_sort_by_time_orders_tasks_chronologically() -> None:
	"""Verify tasks added out of order are sorted by time."""
	scheduler = Scheduler()
	tasks = [
		Task("Evening walk", "18:00", 20, "Medium", "Daily"),
		Task("Morning feed", "07:30", 10, "High", "Daily"),
		Task("Lunch check", "12:00", 5, "Low", "Daily"),
	]

	sorted_tasks = scheduler.sort_by_time(tasks)

	assert [task.time for task in sorted_tasks] == ["07:30", "12:00", "18:00"]


def test_sort_by_time_same_time_orders_by_priority() -> None:
	"""Verify same-time tasks are sorted high -> medium -> low priority."""
	scheduler = Scheduler()
	tasks = [
		Task("Low priority task", "09:00", 10, "Low", "Daily"),
		Task("High priority task", "09:00", 10, "High", "Daily"),
		Task("Medium priority task", "09:00", 10, "Medium", "Daily"),
	]

	sorted_tasks = scheduler.sort_by_time(tasks)

	assert [task.priority for task in sorted_tasks] == ["High", "Medium", "Low"]


def test_detect_conflicts_finds_overlapping_tasks() -> None:
	"""Verify overlapping task windows are detected as conflicts."""
	scheduler = Scheduler()
	task1 = Task("Walk", "08:00", 30, "High", "Daily")   # 08:00-08:30
	task2 = Task("Feed", "08:15", 10, "Medium", "Daily") # 08:15-08:25
	task3 = Task("Brush", "09:00", 10, "Low", "Daily")   # 09:00-09:10

	conflicts = scheduler.detect_conflicts([task1, task2, task3])

	assert (task1, task2) in conflicts
	assert len(conflicts) == 1


def test_detect_conflicts_back_to_back_not_conflict() -> None:
	"""Verify back-to-back tasks are not treated as conflicts."""
	scheduler = Scheduler()
	task1 = Task("Morning walk", "08:00", 30, "High", "Daily")  # 08:00-08:30
	task2 = Task("Breakfast", "08:30", 15, "Medium", "Daily")   # 08:30-08:45

	conflicts = scheduler.detect_conflicts([task1, task2])

	assert conflicts == []


def test_filter_by_pet_returns_only_specified_pet_tasks_case_insensitive() -> None:
	"""Verify filter_by_pet returns only matching pet tasks and ignores case."""
	owner = Owner("Amina")
	dog = Pet(name="Buddy", species="Dog")
	cat = Pet(name="Luna", species="Cat")

	dog_task_1 = Task("Morning walk", "08:00", 30, "High", "Daily")
	dog_task_2 = Task("Evening walk", "18:00", 25, "Medium", "Daily")
	cat_task = Task("Litter cleaning", "09:00", 15, "Low", "Daily")

	dog.add_task(dog_task_1)
	dog.add_task(dog_task_2)
	cat.add_task(cat_task)

	owner.add_pet(dog)
	owner.add_pet(cat)

	scheduler = Scheduler()
	result = scheduler.filter_by_pet(owner, "bUdDy")

	assert result == [dog_task_1, dog_task_2]
	assert cat_task not in result


def test_scheduler_methods_handle_empty_task_lists() -> None:
	"""Verify scheduler methods gracefully handle empty task lists."""
	scheduler = Scheduler()

	assert scheduler.sort_by_time([]) == []
	assert scheduler.detect_conflicts([]) == []
	assert scheduler.generate_daily_plan([]) == []
	assert scheduler.filter_tasks([], "complete") == []
	assert scheduler.filter_tasks([], "incomplete") == []
	assert scheduler.explain_plan([]) == "No tasks scheduled for today."
