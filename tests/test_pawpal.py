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
