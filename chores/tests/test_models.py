from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils import timezone

from chores.models import *
from chores.tests.utilities import *

class FactoryTestCase(TestCase):
	factories = Populate()

class ChildTests(FactoryTestCase):

	def setUp(self):
		# Set up all factories since we'll need in certain context regarding point totals
		self.factories.populate_chores()

	# In Django, the default is that blank=False, so we don't need to test this
	# def test_validations(self):
	# 	bad_child1 = ChildFactory.create(first_name="")
	# 	self.assertRaises(ValidationError, bad_child1.full_clean)

	# 	bad_child2 = ChildFactory.create(last_name="")
	# 	self.assertRaises(ValidationError, bad_child2.full_clean)

	def test_name(self):
		self.assertEqual("Alex Heimann", self.factories.alex.name())
		self.assertEqual("Mark Heimann", self.factories.mark.name())
		self.assertEqual("Rachel Heimann", self.factories.rachel.name())

	def test_points_earned(self):
		self.assertEqual(4, self.factories.alex.points_earned())
		self.assertEqual(1, self.factories.mark.points_earned())
		self.assertEqual(0, self.factories.rachel.points_earned())

	def test_alphabetical(self):
		self.assertEqual(list(map(lambda child: child.first_name, Child.objects.alphabetical())), ["Alex", "Mark", "Rachel"])

	def test_active(self):
		self.assertEqual(list(map(lambda child: child.first_name, Child.objects.active().alphabetical())), ["Alex", "Mark"])

class TaskTests(FactoryTestCase):

	def setUp(self):
		self.factories.populate_tasks()

	# In Django, the default is that blank=False, so we don't need to test this
	# def test_validate_name(self):
	# 	bad_task1 = TaskFactory.create(name="")
	# 	self.assertRaises(ValidationError, bad_task1.full_clean)

	def test_alphabetical(self):
		self.assertEqual(list(map(lambda task: task.name, Task.objects.alphabetical())), ["Mow grass", "Shovel driveway", "Stack wood", "Sweep floor", "Wash dishes"])

	def test_active(self):
		self.assertEqual(list(map(lambda task: task.name, Task.objects.active().alphabetical())), ["Mow grass", "Shovel driveway", "Sweep floor", "Wash dishes"])

class ChoreTests(FactoryTestCase):

	def setUp(self):
		self.factories.populate_chores()

	def test_by_task(self):
		self.assertEqual(list(map(lambda chore: chore.task.name, Chore.objects.by_task())), ["Shovel driveway","Sweep floor","Sweep floor","Sweep floor", "Wash dishes","Wash dishes","Wash dishes"])

	def test_chronological(self):
		self.assertEqual(list(map(lambda chore: chore.task.name, Chore.objects.chronological())), ["Shovel driveway","Sweep floor","Wash dishes","Sweep floor","Wash dishes","Sweep floor","Wash dishes"])

	def test_pending(self):
		self.assertEqual(4, len(Chore.objects.pending()))

	def test_done(self):
		self.assertEqual(3, len(Chore.objects.done()))

	def test_upcoming(self):
		self.assertEqual(6, len(Chore.objects.upcoming()))

	def test_past(self):
		self.assertEqual(1, len(Chore.objects.past()))

	def test_status_completed(self):
		self.assertEqual("Completed", self.factories.ac3.status())

	def test_status_pending(self):
		self.assertEqual("Pending", self.factories.mc1.status())
    
