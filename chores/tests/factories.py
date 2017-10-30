import factory
from chores.models import *
from django.utils import timezone

class ChildFactory(factory.django.DjangoModelFactory):
  class Meta:
    model = Child

  first_name = "Alex"
  last_name = "Heimann"
  active = True

class TaskFactory(factory.django.DjangoModelFactory):
  class Meta:
    model = Task

  name = "Wash dishes"
  points = 1
  active = True

class ChoreFactory(factory.django.DjangoModelFactory):
  class Meta:
    model = Chore

  # Sub Factories are used for One to Many relationships
  child = factory.SubFactory(ChildFactory)
  task = factory.SubFactory(TaskFactory)

  due_on = timezone.now() + timezone.timedelta(days=1)
  completed = False