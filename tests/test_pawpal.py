from pawpal_system import Pet, Task


def test_task_completion_marks_task_as_completed() -> None:
	task = Task(
		task_id="task-1",
		pet_id="pet-1",
		description="Morning walk",
		duration_minutes=20,
		priority="high",
	)

	assert task.completed is False

	task.mark_complete()

	assert task.completed is True


def test_task_addition_increases_pet_task_count() -> None:
	pet = Pet(
		pet_id="pet-1",
		name="Mochi",
		species="dog",
		breed="Shiba Inu",
		weight_kg=10.5,
	)

	starting_count = len(pet.tasks)

	task = Task(
		task_id="task-2",
		pet_id=pet.pet_id,
		description="Evening feeding",
		duration_minutes=10,
		priority="medium",
	)
	pet.add_task(task)

	assert len(pet.tasks) == starting_count + 1
