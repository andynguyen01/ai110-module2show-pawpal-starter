"""Core implementation for the PawPal pet-care planning system."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime, time, timedelta
from typing import Any, Dict, List, Optional


@dataclass
class Task:
	"""A single care activity for a pet."""

	task_id: str
	pet_id: str
	description: str
	duration_minutes: int
	priority: str
	frequency: str = "daily"
	due_time: Optional[time] = None
	completed: bool = False
	task_type: str = "general"
	reason: str = ""
	scheduled_for: Optional[date] = None

	VALID_PRIORITIES = {"low", "medium", "high"}
	VALID_FREQUENCIES = {"once", "daily", "weekly"}

	def __post_init__(self) -> None:
		"""Normalize and validate task fields after initialization."""
		self.priority = self.priority.lower().strip()
		self.frequency = self.frequency.lower().strip()
		if self.priority not in self.VALID_PRIORITIES:
			raise ValueError(f"Invalid priority: {self.priority}")
		if self.frequency not in self.VALID_FREQUENCIES:
			raise ValueError(f"Invalid frequency: {self.frequency}")
		if self.duration_minutes <= 0:
			raise ValueError("duration_minutes must be positive")

	def is_due_on(self, day: date) -> bool:
		"""Return True if task should appear in plan for this date."""
		if self.completed and self.frequency == "once":
			return False
		if self.frequency == "daily":
			return True
		if self.frequency == "weekly":
			if self.scheduled_for is None:
				return False
			return day.weekday() == self.scheduled_for.weekday()
		# once
		if self.scheduled_for is None:
			return True
		return self.scheduled_for == day

	def mark_completed(self) -> None:
		"""Mark this task as completed."""
		self.completed = True

	def mark_complete(self) -> None:
		"""Compatibility alias for mark_completed."""
		self.mark_completed()

	def mark_incomplete(self) -> None:
		"""Mark this task as not completed."""
		self.completed = False

	def calculate_urgency(self, current_time: time) -> int:
		"""Higher number means more urgent."""
		urgency = 0
		if self.priority == "high":
			urgency += 60
		elif self.priority == "medium":
			urgency += 35
		else:
			urgency += 15

		if self.due_time is not None:
			now_minutes = current_time.hour * 60 + current_time.minute
			due_minutes = self.due_time.hour * 60 + self.due_time.minute
			if now_minutes >= due_minutes:
				urgency += 50
			else:
				mins_left = due_minutes - now_minutes
				urgency += max(0, 40 - mins_left // 10)

		if not self.completed:
			urgency += 10

		return urgency

	def explain_why(self) -> str:
		"""Return a short explanation for why the task was selected."""
		due_text = self.due_time.strftime("%H:%M") if self.due_time else "any time"
		return (
			f"{self.description} for pet {self.pet_id} was selected because "
			f"it is {self.priority} priority, {self.frequency}, and due around {due_text}."
		)


@dataclass
class Pet:
	"""Stores pet profile and its care tasks."""

	pet_id: str
	name: str
	species: str
	breed: str
	weight_kg: float
	diet_plan: str = ""
	medications: List[str] = field(default_factory=list)
	care_notes: Dict[str, Any] = field(default_factory=dict)
	tasks: List[Task] = field(default_factory=list)

	def add_task(self, task: Task) -> None:
		"""Add a task to this pet after validating ownership."""
		if task.pet_id != self.pet_id:
			raise ValueError("task.pet_id must match pet.pet_id")
		self.tasks.append(task)

	def remove_task(self, task_id: str) -> bool:
		"""Remove a task by id and return True if removed."""
		for i, task in enumerate(self.tasks):
			if task.task_id == task_id:
				del self.tasks[i]
				return True
		return False

	def get_tasks_for_day(self, day: date) -> List[Task]:
		"""Return tasks that are due on the provided day."""
		return [task for task in self.tasks if task.is_due_on(day)]

	def get_pending_tasks_for_day(self, day: date) -> List[Task]:
		"""Return due tasks for the day that are not completed."""
		return [task for task in self.get_tasks_for_day(day) if not task.completed]

	def update_health(self, weight_kg: float, notes: Optional[Dict[str, Any]] = None) -> None:
		"""Update this pet's weight and optionally merge care notes."""
		self.weight_kg = weight_kg
		if notes:
			self.care_notes.update(notes)


class Owner:
	"""Manages pets and provides task access for scheduling."""

	def __init__(
		self,
		owner_id: str,
		name: str,
		time_available_min_per_day: int,
		preferences: Optional[Dict[str, Any]] = None,
		notification_method: str = "app",
		pets: Optional[List[Pet]] = None,
	) -> None:
		"""Initialize an owner with profile, preferences, and pets."""
		self.owner_id = owner_id
		self.name = name
		self.time_available_min_per_day = time_available_min_per_day
		self.preferences = preferences if preferences is not None else {}
		self.notification_method = notification_method
		self.pets: List[Pet] = pets if pets is not None else []

	def add_pet(self, pet: Pet) -> None:
		"""Add a pet to the owner's managed pet list."""
		self.pets.append(pet)

	def remove_pet(self, pet_id: str) -> bool:
		"""Remove a pet by id and return True if removed."""
		for i, pet in enumerate(self.pets):
			if pet.pet_id == pet_id:
				del self.pets[i]
				return True
		return False

	def set_preferences(self, preferences: Dict[str, Any]) -> None:
		"""Replace owner preferences with the provided mapping."""
		self.preferences = preferences

	def get_available_time(self, day: date) -> int:
		"""Allow per-day overrides in preferences via 'time_overrides'."""
		overrides = self.preferences.get("time_overrides", {})
		return int(overrides.get(day.isoformat(), self.time_available_min_per_day))

	def get_all_tasks(self, day: Optional[date] = None) -> List[Task]:
		"""Return all pet tasks, optionally filtered to a specific day."""
		all_tasks: List[Task] = []
		for pet in self.pets:
			if day is None:
				all_tasks.extend(pet.tasks)
			else:
				all_tasks.extend(pet.get_tasks_for_day(day))
		return all_tasks

	def complete_task(self, task_id: str) -> bool:
		"""Mark a task completed by id and return success status."""
		for task in self.get_all_tasks():
			if task.task_id == task_id:
				task.mark_completed()
				return True
		return False


class Scheduler:
	"""The planning brain that builds a feasible daily plan."""

	def __init__(self, constraints: Optional[Dict[str, Any]] = None) -> None:
		"""Initialize scheduler state and optional planning constraints."""
		self.constraints = constraints if constraints is not None else {}
		self.daily_plan: List[Task] = []
		self._task_index: Dict[str, Task] = {}
		self._last_explanations: List[str] = []

	def collect_tasks(self, pets: List[Pet], day: date) -> List[Task]:
		"""Collect pending tasks due on the given day from all pets."""
		collected: List[Task] = []
		for pet in pets:
			collected.extend(pet.get_pending_tasks_for_day(day))
		return collected

	def rank_tasks(self, tasks: List[Task], current_time: Optional[time] = None) -> List[Task]:
		"""Sort tasks by urgency, then duration, then description."""
		if current_time is None:
			current_time = datetime.now().time()

		return sorted(
			tasks,
			key=lambda task: (
				task.calculate_urgency(current_time),
				-task.duration_minutes,
				task.description.lower(),
			),
			reverse=True,
		)

	def apply_owner_constraints(self, owner: Owner, tasks: List[Task], day: date) -> List[Task]:
		"""Filter ranked tasks to fit owner limits and preferences."""
		available_minutes = owner.get_available_time(day)
		blocked_types = set(owner.preferences.get("blocked_task_types", []))
		preferred_species = owner.preferences.get("preferred_species")

		selected: List[Task] = []
		used_minutes = 0

		pet_by_id = {pet.pet_id: pet for pet in owner.pets}

		for task in tasks:
			if task.task_type in blocked_types:
				continue
			pet = pet_by_id.get(task.pet_id)
			if preferred_species and pet and pet.species != preferred_species:
				continue
			if used_minutes + task.duration_minutes > available_minutes:
				continue
			selected.append(task)
			used_minutes += task.duration_minutes

		return selected

	def build_daily_plan(self, owner: Owner, day: date, current_time: Optional[time] = None) -> List[Task]:
		"""Build and store the selected daily plan for the owner."""
		candidate_tasks = self.collect_tasks(owner.pets, day)
		ranked_tasks = self.rank_tasks(candidate_tasks, current_time=current_time)
		self.daily_plan = self.apply_owner_constraints(owner, ranked_tasks, day)

		self._task_index = {task.task_id: task for task in self.daily_plan}
		self._last_explanations = [
			f"Included: {task.explain_why()}"
			for task in self.daily_plan
		]

		for task in self.daily_plan:
			task.scheduled_for = day

		return self.daily_plan

	def reschedule_unfinished_tasks(self, owner: Owner, source_day: date, target_day: Optional[date] = None) -> int:
		"""Move unfinished once/weekly tasks to a target day."""
		if target_day is None:
			target_day = source_day + timedelta(days=1)

		rescheduled_count = 0
		for task in owner.get_all_tasks(source_day):
			if not task.completed and task.frequency in {"once", "weekly"}:
				task.scheduled_for = target_day
				rescheduled_count += 1

		return rescheduled_count

	def get_task_by_id(self, task_id: str) -> Optional[Task]:
		"""Return a task from the current plan index by id."""
		return self._task_index.get(task_id)

	def explain_plan(self) -> str:
		"""Return human-readable explanations for the current daily plan."""
		if not self.daily_plan:
			return "No tasks were selected for today."
		return "\n".join(self._last_explanations)


# Backward-compatible alias for earlier class naming.
Pets = Pet
