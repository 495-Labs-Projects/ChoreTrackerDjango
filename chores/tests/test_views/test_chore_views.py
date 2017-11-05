from django.test import RequestFactory
from django.urls import reverse
from django.utils import timezone

from chores.models import *
from chores.forms import *
from chores.views import *
from chores.tests.utilities import *
    

class ChoreViewTests(FactoryTestCase):

    def setUp(self):
        self.factories.populate_chores()

    def test_list_view_with_no_chores(self):
        Chore.objects.all().delete()

        response = self.client.get(reverse('chores:chore_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No chores are available.")
        self.assertQuerysetEqual(response.context['chores'], [])

    # Not really necessary since we are partially testing chronological here, but just to be safe
    def test_list_view_with_chores(self):
        response = self.client.get(reverse('chores:chore_list'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(list(response.context['chores']), 
            [repr(self.factories.ac3),repr(self.factories.mc3),repr(self.factories.ac4),repr(self.factories.mc1),repr(self.factories.ac1),repr(self.factories.ac2),repr(self.factories.mc2)])

    def test_new_chore_view(self):
        response = self.client.get(reverse('chores:chore_new'))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], ChoreForm)
        self.assertContains(response, "Create Chore")

    def test_create_chore_view(self):
        num_chores = Chore.objects.count()
        response = self.client.post(reverse('chores:chore_new'),
            {'child': self.factories.alex.id, 'task': self.factories.shovel.id, 'due_on': timezone.now().date() + timezone.timedelta(days=3), 'completed': False}) 
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
            {'child': self.factories.alex.id, 'task': self.factories.dishes.id, 'due_on': timezone.now().date() + timezone.timedelta(days=3), 'completed': False})
        self.factories.ac1.refresh_from_db()
        self.assertEqual(self.factories.ac1.due_on, timezone.now().date() + timezone.timedelta(days=3))
        self.assertRedirects(response, reverse('chores:chore_detail', args=(self.factories.ac1.id,)))

    def test_update_bad_chore_view(self):
        response = self.client.post(reverse('chores:chore_edit', args=(self.factories.ac1.id,)),
            {'child': self.factories.alex.id, 'task': 500, 'due_on': timezone.now() + timezone.timedelta(days=3), 'completed': False})
        self.factories.ac1.refresh_from_db()
        self.assertEqual(self.factories.ac1.due_on, timezone.now().date() + timezone.timedelta(days=1))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], ChoreForm)

    def test_delete_chore_view(self):
        num_chores = Chore.objects.count()
        response = self.client.post(reverse('chores:chore_delete', args=(self.factories.ac1.id,)))
        self.assertEqual(Chore.objects.count(), num_chores - 1)
        self.assertRedirects(response, reverse('chores:chore_list'))
        
