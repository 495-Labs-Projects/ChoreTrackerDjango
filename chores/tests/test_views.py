from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.utils import timezone

from chores.models import *
from chores.forms import *
from chores.views import *
from chores.tests.test_models import FactoryTestCase

class ChildViewTests(FactoryTestCase):

    def setUp(self):
        self.populate_children()

    def test_list_view_with_no_children(self):
        Child.objects.all().delete()

        response = self.client.get(reverse('chores:child_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No children are available.")
        self.assertQuerysetEqual(response.context['children'], [])

    def test_list_view_with_children(self):
        response = self.client.get(reverse('chores:child_list'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(list(response.context['children']), 
            [repr(self.factories.alex), repr(self.factories.mark), repr(self.factories.rachel)])

    def test_new_child_view(self):
        response = self.client.get(reverse('chores:child_new'))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], ChildForm)
        self.assertContains(response, "Create Child")

    def test_create_child_view(self):
        num_children = Child.objects.count()
        response = self.client.post(reverse('chores:child_new'),
            {'first_name': 'Connor', 'last_name': 'Hanley', 'active': True}) 
        self.assertEqual(Child.objects.count(), num_children + 1)
        self.assertRedirects(response, reverse('chores:child_detail', args=(num_children+1,)))

    def test_create_bad_child_view(self):
        num_children = Child.objects.count()
        response = self.client.post(reverse('chores:child_new'),
            {'first_name': '', 'last_name': '', 'active': False}) 
        self.assertEqual(Child.objects.count(), num_children)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], ChildForm)

    def test_edit_child_view(self):
        response = self.client.get(reverse('chores:child_edit', args=(self.factories.alex.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], ChildForm)
        self.assertContains(response, "Update Child")

    def test_update_child_view(self):
        response = self.client.post(reverse('chores:child_edit', args=(self.factories.alex.id,)),
            {'first_name': 'Batman', 'last_name': 'Heimann', 'active': True})
        self.factories.alex.refresh_from_db()
        self.assertEqual(self.factories.alex.first_name, 'Batman')
        self.assertRedirects(response, reverse('chores:child_detail', args=(self.factories.alex.id,)))

    def test_update_bad_child_view(self):
        response = self.client.post(reverse('chores:child_edit', args=(self.factories.alex.id,)),
            {'first_name': '', 'last_name': '', 'active': False})
        self.factories.alex.refresh_from_db()
        self.assertEqual(self.factories.alex.first_name, 'Alex')
        self.assertEqual(self.factories.alex.last_name, 'Heimann')
        self.assertEqual(self.factories.alex.active, True)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], ChildForm)

    def test_delete_child_view(self):
        num_children = Child.objects.count()
        response = self.client.post(reverse('chores:child_delete', args=(self.factories.alex.id,)))
        self.assertEqual(Child.objects.count(), num_children - 1)
        self.assertRedirects(response, reverse('chores:child_list'))


class TaskViewTests(FactoryTestCase):

    def setUp(self):
        self.factories.populate_tasks()

    def test_list_view_with_no_tasks(self):
        Task.objects.all().delete()

        response = self.client.get(reverse('chores:task_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No tasks are available.")
        self.assertQuerysetEqual(response.context['tasks'], [])

    def test_list_view_with_tasks(self):
        response = self.client.get(reverse('chores:task_list'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(list(response.context['tasks']), 
            [repr(self.factories.mow), repr(self.factories.shovel), repr(self.factories.wood), repr(self.factories.sweep), repr(self.factories.dishes)])

    def test_new_task_view(self):
        response = self.client.get(reverse('chores:task_new'))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], TaskForm)
        self.assertContains(response, "Create Task")

    def test_create_task_view(self):
        num_tasks = Task.objects.count()
        response = self.client.post(reverse('chores:task_new'),
            {'name': 'Pet the cat', 'points': 5, 'active': True}) 
        self.assertEqual(Task.objects.count(), num_tasks + 1)
        self.assertRedirects(response, reverse('chores:task_detail', args=(num_tasks+1,)))

    def test_create_bad_task_view(self):
        num_tasks = Task.objects.count()
        response = self.client.post(reverse('chores:task_new'),
            {'name': 'Pet the cat', 'points': -1, 'active': True}) 
        self.assertEqual(Task.objects.count(), num_tasks)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], TaskForm)

    def test_edit_task_view(self):
        response = self.client.get(reverse('chores:task_edit', args=(self.factories.dishes.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], TaskForm)
        self.assertContains(response, "Update Task")

    def test_update_task_view(self):
        response = self.client.post(reverse('chores:task_edit', args=(self.factories.dishes.id,)),
            {'name': 'Pet the cat', 'points': 1, 'active': True})
        self.factories.dishes.refresh_from_db()
        self.assertEqual(self.factories.dishes.name, 'Pet the cat')
        self.assertRedirects(response, reverse('chores:task_detail', args=(self.factories.dishes.id,)))

    def test_update_bad_task_view(self):
        response = self.client.post(reverse('chores:task_edit', args=(self.factories.dishes.id,)),
            {'name': 'Pet the cat', 'points': -1, 'active': True})
        self.factories.dishes.refresh_from_db()
        self.assertEqual(self.factories.a1.name, 'Wash dishes')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], TaskForm)

    def test_delete_task_view(self):
        num_tasks = Task.objects.count()
        response = self.client.post(reverse('chores:task_delete', args=(self.factories.dishes.id,)))
        self.assertEqual(Task.objects.count(), num_tasks - 1)
        self.assertRedirects(response, reverse('chores:task_list'))


class ChoreViewTests(FactoryTestCase):

    def setUp(self):
        self.factories.populate_chores()

    def test_list_view_with_no_chores(self):
        Chore.objects.all().delete()

        response = self.client.get(reverse('chores:chore_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No chores are available.")
        self.assertQuerysetEqual(response.context['chores'], [])

    def test_list_view_with_chores(self):
        response = self.client.get(reverse('chores:chore_list'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(list(response.context['chores']), 
            [repr(self.factories.ac3),repr(self.factories.mc1),repr(self.factories.ac2),repr(self.factories.mc3),repr(self.factories.ac1),repr(self.factories.mc2),repr(self.factories.ac4)])

    def test_new_chore_view(self):
        response = self.client.get(reverse('chores:chore_new'))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], ChoreForm)
        self.assertContains(response, "Create Chore")

    def test_create_chore_view(self):
        num_chores = Chore.objects.count()
        response = self.client.post(reverse('chores:chore_new'),
            {'child': self.factories.alex.id, 'task': self.factories.shovel.id, 'due_on': timezone.now() + timezone.timedelta(days=3), 'completed': False}) 
        self.assertEqual(Chore.objects.count(), num_chores + 1)
        self.assertRedirects(response, reverse('chores:chore_detail', args=(num_chores+1,)))

    def test_create_bad_chore_view(self):
        num_chores = Chore.objects.count()
        response = self.client.post(reverse('chores:chore_new'),
            {'child': self.factories.alex.id, 'task': 500, 'due_on': timezone.now() + timezone.timedelta(days=3), 'completed': False}) 
        self.assertEqual(Chore.objects.count(), num_chores)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], ChoreForm)

    def test_edit_chore_view(self):
        response = self.client.get(reverse('chores:chore_edit', args=(self.factories.ac1.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], ChoreForm)
        self.assertContains(response, "Update Chore")

    def test_update_chore_view(self):
        response = self.client.post(reverse('chores:chore_edit', args=(self.factories.ac1.id,)),
            {'child': self.factories.alex.id, 'task': self.factories.dishes.id, 'due_on': timezone.now() + timezone.timedelta(days=3), 'completed': False})
        self.factories.ac1.refresh_from_db()
        self.assertEqual(self.factories.ac1.due_on, timezone.now() + timezone.timedelta(days=3))
        self.assertRedirects(response, reverse('chores:chore_detail', args=(self.factories.ac1.id,)))

    def test_update_bad_chore_view(self):
        response = self.client.post(reverse('chores:chore_edit', args=(self.factories.ac1.id,)),
            {'child': self.factories.alex.id, 'task': 500, 'due_on': timezone.now() + timezone.timedelta(days=3), 'completed': False})
        self.factories.ac1.refresh_from_db()
        self.assertEqual(self.factories.ac1.due_on, timezone.now() + timezone.timedelta(days=1))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], ChoreForm)

    def test_delete_chore_view(self):
        num_chores = Chore.objects.count()
        response = self.client.post(reverse('chores:chore_delete', args=(self.factories.ac1.id,)))
        self.assertEqual(Chore.objects.count(), num_chores - 1)
        self.assertRedirects(response, reverse('chores:chore_list'))
