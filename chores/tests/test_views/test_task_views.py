from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.utils import timezone

from chores.models import *
from chores.forms import *
from chores.views import *
from chores.tests.test_models import FactoryTestCase

class TaskViewTests(FactoryTestCase):

    def setUp(self):
        self.factories.populate_tasks()

    def test_list_view_with_no_tasks(self):
        Task.objects.all().delete()

        response = self.client.get(reverse('chores:task_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No tasks are available.")
        self.assertQuerysetEqual(response.context['tasks'], [])

    # Not really necessary since we are partially testing alphabetical here, but just to be safe
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
        self.assertEqual(self.factories.dishes.name, 'Wash dishes')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], TaskForm)

    def test_delete_task_view(self):
        num_tasks = Task.objects.count()
        response = self.client.post(reverse('chores:task_delete', args=(self.factories.dishes.id,)))
        self.assertEqual(Task.objects.count(), num_tasks - 1)
        self.assertRedirects(response, reverse('chores:task_list'))

