from django.core.exceptions import ValidationError
from django.utils import timezone

from chores.models import *
from chores.tests.utilities import *


class TaskTests(FactoryTestCase):

	def setUp(self):
		self.factories.populate_tasks()

	def test_validate_name(self):
		with self.assertRaises(ValidationError):
				bad_task = TaskFactory.create(name="")
				bad_task.full_clean()

	# def test_validate_points(self):
	# 	with self.assertRaises(ValidationError):
	# 			bad_task = TaskFactory.create(points=-1)
	# 			bad_task.full_clean()

	def test_alphabetical(self):
		self.assertEqual(list(map(lambda task: task.name, Task.objects.alphabetical())), ["Mow grass", "Shovel driveway", "Stack wood", "Sweep floor", "Wash dishes"])

	def test_active(self):
		self.assertEqual(list(map(lambda task: task.name, Task.objects.active().alphabetical())), ["Mow grass", "Shovel driveway", "Sweep floor", "Wash dishes"])