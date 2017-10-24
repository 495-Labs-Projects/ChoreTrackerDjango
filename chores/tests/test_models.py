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

	# We do not specifically test one to many relationships here
	# def test_relationships

	def test_validations(self):
    bad_child1 = ChildFactory.create(first_name="")
    self.assertRaises(ValidationError, bad_child1.full_clean)

    bad_child2 = ChildFactory.create(last_name="")
    self.assertRaises(ValidationError, bad_child2.full_clean)

  def test_name(self):
  	self.assertEqual("Alex Heimann", self.factories.alex.name())
  	self.assertEqual("Mark Heimann", self.factories.mark.name())
  	self.assertEqual("Rachel Heimann", self.factories.rachel.name())

  def test_points_earned(self):
  	self.assertEqual(4, self.factories.alex.points_earned())
  	self.assertEqual(1, self.factories.mark.points_earned())
  	self.assertEqual(0, self.factories.rachel.points_earned())

  def test_alphabetical(self):
  	self.assertEqual(map(lambda child: child.first_name, Child.objects.alphabetical()), ["Alex", "Mark", "Rachel"])

  def test_active(self):
  	self.assertEqual(map(lambda child: child.first_name, Child.objects.active.alphabetical()), ["Alex", "Mark"])

class TaskTests(FactoryTestCase):

	def setUp(self):
		self.factories.populate_tasks()

	def test_validate_name(self):
		bad_task1 = TaskFactory.create(name="")
    self.assertRaises(ValidationError, bad_task1.full_clean)

  




