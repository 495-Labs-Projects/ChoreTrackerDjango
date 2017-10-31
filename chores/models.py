from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from functools import reduce

# Child, Task, and Chore Models

class Child(models.Model):
  # Child fields
  first_name = models.CharField(max_length=255)
  last_name = models.CharField(max_length=255)
  active = models.BooleanField(default=True)

  # Scopes/Manager
  class QuerySet(models.QuerySet):
    def alphabetical(self):
      return self.order_by("last_name", "first_name")

    def active(self):
      return self.filter(active=True)

  objects = QuerySet.as_manager()

  # Methods
  def name(self):
    return self.first_name + " " + self.last_name

  def points_earned(self):
    return reduce(lambda a,b: a+b, map(lambda chore: chore.task.points, self.chore_set.done()), 0)

  # For debugging
  def __str__(self):
    return self.first_name + " " + self.last_name

class Task(models.Model):
  # Task fields
  name = models.CharField(max_length=255)
  points = models.PositiveIntegerField()
  active = models.BooleanField(default=True)

  # Scopes/Manager
  class QuerySet(models.QuerySet):
    def alphabetical(self):
      return self.order_by("name")

    def active(self):
      return self.filter(active=True)

  objects = QuerySet.as_manager()

  # For debugging
  def __str__(self):
    return self.name

class Chore(models.Model):
  # Task fields
  child = models.ForeignKey(Child)
  task = models.ForeignKey(Task)
  due_on = models.DateField()
  completed = models.BooleanField(default=False)

  # Scopes/Manager
  class QuerySet(models.QuerySet):
    def chronological(self):
      return self.order_by("due_on", "task__name")

    def done(self):
      return self.filter(completed=True)

    def pending(self):
      return self.filter(completed=False)

    def by_task(self):
      return self.order_by("task__name")

    def upcoming(self):
      return self.filter(due_on__gte=timezone.now())

    def past(self):
      return self.filter(due_on__lt=timezone.now())

  objects = QuerySet.as_manager()

  # Methods
  def status(self):
    return "Completed" if self.completed else "Pending"

  # For debugging
  def __str__(self):
    return self.task.name

