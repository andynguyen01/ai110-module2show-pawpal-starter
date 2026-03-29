"""Core class skeletons for the PawPal pet-care planning system."""

from typing import Any, Dict, List


class Owner:
	def __init__(
		self,
		owner_id: str,
		name: str,
		time_available_min_per_day: int,
		preferences: Dict[str, Any],
		notification_method: str,
	) -> None:
		self.owner_id = owner_id
		self.name = name
		self.time_available_min_per_day = time_available_min_per_day
		self.preferences = preferences
		self.notification_method = notification_method

	def view_daily_plan(self, date: str) -> None:
		pass

	def complete_task(self, task_id: str) -> None:
		pass

	def set_preferences(self, preferences: Dict[str, Any]) -> None:
		pass

	def get_available_time(self, date: str) -> int:
		pass


class Pets:
	def __init__(
		self,
		pet_id: str,
		name: str,
		species: str,
		breed: str,
		weight_kg: float,
		diet_plan: str,
		medications: List[str],
		walk_need_per_day: int,
		enrichment_need_per_day: int,
		care_notes: Dict[str, Any],
	) -> None:
		self.pet_id = pet_id
		self.name = name
		self.species = species
		self.breed = breed
		self.weight_kg = weight_kg
		self.diet_plan = diet_plan
		self.medications = medications
		self.walk_need_per_day = walk_need_per_day
		self.enrichment_need_per_day = enrichment_need_per_day
		self.care_notes = care_notes

	def get_daily_needs(self) -> List["Task"]:
		pass

	def update_health(self, weight_kg: float, notes: Dict[str, Any]) -> None:
		pass

	def requires_task(self, task_type: str) -> bool:
		pass


class Task:
	def __init__(
		self,
		task_id: str,
		pet_id: str,
		task_type: str,
		duration_min: int,
		priority: int,
		due_window: str,
		recurrence: str,
		status: str,
		reason: str,
	) -> None:
		self.task_id = task_id
		self.pet_id = pet_id
		self.task_type = task_type
		self.duration_min = duration_min
		self.priority = priority
		self.due_window = due_window
		self.recurrence = recurrence
		self.status = status
		self.reason = reason

	def is_due_today(self, date: str) -> bool:
		pass

	def calculate_urgency(self, current_time: str) -> int:
		pass

	def mark_completed(self) -> None:
		pass

	def explain_why(self) -> str:
		pass


class Scheduler:
	def __init__(self, tasks: List[Task], constraints: Dict[str, Any]) -> None:
		self.tasks = tasks
		self.constraints = constraints
		self.daily_plan: List[Task] = []

	def collect_tasks(self, pets: List[Pets]) -> List[Task]:
		pass

	def apply_owner_constraints(self, owner: Owner) -> None:
		pass

	def rank_tasks(self) -> List[Task]:
		pass

	def build_daily_plan(self, date: str) -> List[Task]:
		pass

	def reschedule_unfinished_tasks(self) -> None:
		pass

	def explain_plan(self) -> str:
		pass
