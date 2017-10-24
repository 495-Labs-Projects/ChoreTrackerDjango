from chores.tests.factories import *
from django.utils import timezone

class Populate():

  def populate_children(self):
    self.alex = ChildFactory.create()
    self.mark = ChildFactory.create(first_name="Mark")
    self.rachel = ChildFactory.create(first_name="Rachel", active=False)

  def populate_tasks(self):
    self.dishes = TaskFactory.create()
    self.wood = TaskFactory.create(name="Stack wood", active=False)
    self.sweep = TaskFactory.create(name="Sweep floor")
    self.shovel = TaskFactory.create(name="Shovel driveway", points=3)
    self.mow = TaskFactory.create(name="Mow grass", points=2)

  def populate_chores(self):
    self.populate_children()
    self.populate_tasks()

    self.ac1 = ChoreFactory.create(child=self.alex, task=self.dishes)
    self.mc1 = ChoreFactory.create(child=self.mark, task=self.sweep)
    self.ac2 = ChoreFactory.create(child=self.alex, task=self.sweep, due_on=date.today() + datetime.timedelta(days=2))
    self.mc2 = ChoreFactory.create(child=self.mark, task=self.dishes, due_on=date.today() + datetime.timedelta(days=2))
    self.ac3 = ChoreFactory.create(child=self.alex, task=self.shovel, due_on=date.today() - datetime.timedelta(days=2), completed=True)
    self.ac4 = ChoreFactory.create(child=self.alex, task=self.dishes, due_on=date.today(), completed=True)
    self.mc3 = ChoreFactory.create(child=self.mark, task=self.sweep, due_on=date.today(), completed=True)