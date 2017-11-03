from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.utils import timezone

from chores.models import *
from chores.forms import *
from chores.views import *
from chores.tests.test_models import FactoryTestCase

class ChildViewTests(FactoryTestCase):

    def setUp(self):
        self.factories.populate_children()

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
