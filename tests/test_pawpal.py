"""Quick tests for PawPal+ core classes.

Covers:
1. Task completion behavior
2. Task addition to a pet
"""

import pytest

from pawpal_system import Pet, Task


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

	task.mark_complete()

	assert task.is_complete is True


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
