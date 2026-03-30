from datetime import date, time

from pawpal_system import Owner, Pet, Scheduler, Task


def build_demo_data() -> tuple[Owner, Scheduler]:
	owner = Owner(
		owner_id="owner-1",
		name="Jordan",
		time_available_min_per_day=90,
		preferences={
			"blocked_task_types": [],
		},
	)

	dog = Pet(
		pet_id="pet-1",
		name="Mochi",
		species="dog",
		breed="Shiba Inu",
		weight_kg=11.2,
		diet_plan="High-protein kibble",
	)

	cat = Pet(
		pet_id="pet-2",
		name="Luna",
		species="cat",
		breed="Domestic Short Hair",
		weight_kg=4.6,
		diet_plan="Wet food AM/PM",
	)

	dog.add_task(
		Task(
			task_id="t-1",
			pet_id=dog.pet_id,
			description="Morning walk",
			duration_minutes=25,
			priority="high",
			frequency="daily",
			due_time=time(8, 0),
			task_type="walk",
		)
	)

	dog.add_task(
		Task(
			task_id="t-2",
			pet_id=dog.pet_id,
			description="Dinner feeding",
			duration_minutes=10,
			priority="high",
			frequency="daily",
			due_time=time(18, 0),
			task_type="feeding",
		)
	)

	dog.add_task(
		Task(
			task_id="t-5",
			pet_id=dog.pet_id,
			description="Midday potty break",
			duration_minutes=15,
			priority="medium",
			frequency="daily",
			due_time=time(12, 30),
			task_type="walk",
		)
	)

	cat.add_task(
		Task(
			task_id="t-3",
			pet_id=cat.pet_id,
			description="Play and enrichment",
			duration_minutes=20,
			priority="medium",
			frequency="daily",
			due_time=time(12, 30),
			task_type="enrichment",
		)
	)

	cat.add_task(
		Task(
			task_id="t-4",
			pet_id=cat.pet_id,
			description="Medication",
			duration_minutes=5,
			priority="high",
			frequency="daily",
			due_time=time(21, 0),
			task_type="medication",
		)
	)

	owner.add_pet(dog)
	owner.add_pet(cat)

	scheduler = Scheduler()
	return owner, scheduler


def print_schedule(owner: Owner, scheduler: Scheduler) -> None:
	today = date.today()
	# Mark one task complete so filtering by completion has visible output in terminal.
	scheduler.mark_task_complete(owner, "t-2", completed_on=today)
	plan = scheduler.build_daily_plan(owner, today)
	pet_name_by_id = {pet.pet_id: pet.name for pet in owner.pets}
	planned_minutes = sum(task.duration_minutes for task in plan)
	completed_count = sum(1 for task in plan if task.completed)
	pending_count = len(plan) - completed_count

	print("TODAY'S SCHEDULE")
	print("=" * 60)
	print(f"Owner: {owner.name}")
	print(f"Date: {today.isoformat()}")
	print(f"Time Budget: {owner.get_available_time(today)} min")
	print(f"Planned: {planned_minutes} min ({len(plan)} tasks)")
	print("=" * 60)
	print()

	if not plan:
		print("No tasks selected for today.")
		return

	print(f"{'#':<3} {'Time':<6} {'Pri':<5} {'Pet':<8} {'Task':<24} {'Dur':<5} {'Status':<9}")
	for idx, task in enumerate(plan, start=1):
		due_text = task.due_time.strftime("%H:%M") if task.due_time else "--:--"
		priority_text = task.priority.upper()[:5]
		pet_name = pet_name_by_id.get(task.pet_id, task.pet_id)
		description = task.description[:24]
		status_text = "done" if task.completed else "pending"
		print(
			f"{idx:<3} {due_text:<6} {priority_text:<5} {pet_name:<8} "
			f"{description:<24} {str(task.duration_minutes) + 'm':<5} {status_text:<9}"
		)

	print()
	print("-" * 60)
	print(f"Summary: {pending_count} pending, {completed_count} completed")
	print("-" * 60)
	print()
	print("WHY THIS PLAN")
	explanations = scheduler.explain_plan().splitlines()
	for line in explanations:
		print(f"- {line.replace('Included: ', '')}")

	print()
	print("CONFLICT WARNINGS")
	print("-" * 60)
	conflicts = scheduler.detect_time_conflicts(plan)
	conflict_warnings = scheduler.get_conflict_warnings(plan, pet_name_by_id)
	print(f"Conflict count: {len(conflicts)}")
	for conflict in conflicts:
		due_text = conflict["due_time"].strftime("%H:%M")
		pets_text = ", ".join(pet_name_by_id.get(pet_id, pet_id) for pet_id in conflict["pet_ids"])
		tasks_text = ", ".join(conflict["task_ids"])
		print(f"  -> {due_text} | pets: {pets_text} | task_ids: {tasks_text}")
	if conflict_warnings:
		for warning in conflict_warnings:
			print(warning)
	else:
		print("No time conflicts detected.")

	print()
	print("FILTERED VIEWS")
	print("-" * 60)

	mochi_tasks = scheduler.filter_tasks(plan, owner.pets, pet_name="Mochi")
	completed_tasks = scheduler.filter_tasks(plan, owner.pets, completed=True)
	pending_tasks = scheduler.filter_tasks(plan, owner.pets, completed=False)

	print(f"Tasks for Mochi: {len(mochi_tasks)}")
	for task in mochi_tasks:
		due_text = task.due_time.strftime("%H:%M") if task.due_time else "--:--"
		print(f"  {due_text} - {task.description}")

	print(f"Completed tasks: {len(completed_tasks)}")
	for task in completed_tasks:
		due_text = task.due_time.strftime("%H:%M") if task.due_time else "--:--"
		pet_name = pet_name_by_id.get(task.pet_id, task.pet_id)
		print(f"  {due_text} - {pet_name}: {task.description}")

	print(f"Pending tasks: {len(pending_tasks)}")
	for task in pending_tasks:
		due_text = task.due_time.strftime("%H:%M") if task.due_time else "--:--"
		pet_name = pet_name_by_id.get(task.pet_id, task.pet_id)
		print(f"  {due_text} - {pet_name}: {task.description}")


if __name__ == "__main__":
	demo_owner, demo_scheduler = build_demo_data()
	print_schedule(demo_owner, demo_scheduler)
