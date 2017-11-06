from django.core.exceptions import ValidationError
from django.utils import timezone

from chores.models import *
from chores.tests.utilities import *


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