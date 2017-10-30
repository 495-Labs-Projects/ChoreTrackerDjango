from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from django.core.urlresolvers import reverse
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from chores.tests.utilities import *
from chores.tests.pages.child_pages import *
from chores.tests.pages.task_pages import *

import time


class FactoryFunctionalTestCase(StaticLiveServerTestCase):
    factories = Populate()

    # Auxiliary function to add view subdir to URL
    def get_full_url(self, url):
        return self.live_server_url + url

    # Wait page load by element presence
    def wait_page_load(self, el):
        wait = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(el)
            )

# Tedious Way
class TediousChildFunctionalTests(FactoryFunctionalTestCase):
    def setUp(self):
        self.driver = webdriver.Firefox(executable_path="chores/tests/drivers/geckodriver.exe")
        self.driver.implicitly_wait(3)
        self.factories.populate_children()

    def tearDown(self):
        self.driver.quit()
    
    def test_child_list(self):
        driver = self.driver
        self.driver.get(self.get_full_url(reverse("chores:child_list")))

        self.assertIn("Chore Tracker", driver.title)
        heading = driver.find_element_by_css_selector("h1")
        self.assertIn("Children", heading.text)

        children = driver.find_elements_by_css_selector("#child-list li")
        self.assertEqual(len(children), Child.objects.count()) 

    def test_child_detail(self):
        driver = self.driver
        self.driver.get(self.get_full_url(reverse("chores:child_detail", args=(self.factories.alex.id,))))

        name = driver.find_element_by_id("child-name")
        self.assertEqual(self.factories.alex.name(), name.text)

    def test_create_new_child(self):
        driver = self.driver
        self.driver.get(self.get_full_url(reverse("chores:child_new")))

        first_name_input = driver.find_element_by_id("id_first_name")
        first_name_input.send_keys("John")

        last_name_input = driver.find_element_by_id("id_last_name")
        last_name_input.send_keys("Smith")

        first_name_input.submit()

        self.wait_page_load((By.ID, "child-name"))

        name = driver.find_element_by_id("child-name")
        self.assertEqual("John Smith", name.text) 


class BaseFunctionalTests(FactoryFunctionalTestCase):
    def setUp(self):
        self.driver = webdriver.Firefox(executable_path="chores/tests/drivers/geckodriver.exe")
        self.driver.implicitly_wait(3)
        self.driver.get(self.get_full_url(reverse("chores:child_list")))
        self.child_list_page = ChildListPage(self.driver) 

    def tearDown(self):
        self.driver.refresh()
        self.driver.quit()

    def test_navbar(self):
        self.assertEqual(self.child_list_page.get_tasks_nav().text, "Tasks")
        task_list_page = self.child_list_page.goto_tasks_nav()
        self.assertEqual(task_list_page.get_chores_nav().text, "Chores")
        chore_list_page = task_list_page.goto_chores_nav()
        self.assertEqual(chore_list_page.get_children_nav().text, "Children")
        child_list_page = chore_list_page.goto_children_nav()


class ChildFunctionalTests(FactoryFunctionalTestCase):
    def setUp(self):
        self.driver = webdriver.Firefox(executable_path="chores/tests/drivers/geckodriver.exe")
        self.driver.implicitly_wait(3)
        self.factories.populate_children()
        self.driver.get(self.get_full_url(reverse("chores:child_list")))
        self.child_list_page = ChildListPage(self.driver)

    def tearDown(self):
        self.driver.refresh()
        self.driver.quit()

    def test_child_list(self):
        self.assertEqual(self.child_list_page.get_title(), "Chore Tracker")
        self.assertEqual(self.child_list_page.get_heading().text, "Children")
        self.assertEqual(len(self.child_list_page.get_list_elements()), len(Child.objects.all()))

    def test_child_detail(self):
        children = self.child_list_page.get_list_elements()
        detail_page = self.child_list_page.goto_child_detail(children[0])
        self.assertEqual(detail_page.get_heading().text, self.factories.alex.name())

    def test_create_new_child(self):
        new_child_page = self.child_list_page.goto_child_new()
        self.assertEqual(new_child_page.get_heading().text, "New Child")
        new_child_page.fill_out_form("John", "Smith", True)
        detail_page = new_child_page.submit_form()
        self.assertEqual(detail_page.get_heading().text, "John Smith")
        self.assertEqual(detail_page.get_messages().text, "Successfully created John Smith!")

    def test_edit_child(self):
        children = self.child_list_page.get_list_elements()
        self.assertEqual(self.child_list_page.get_item_detail(children[0]).text, self.factories.alex.name())
        edit_page = self.child_list_page.goto_child_edit(children[0])
        self.assertEqual(edit_page.get_heading().text, "Edit Child")
        edit_page.fill_out_form(first_name="Bob")
        detail_page = edit_page.submit_form()
        self.assertEqual(detail_page.get_heading().text, "Bob Heimann")
        self.assertEqual(detail_page.get_messages().text, "Successfully updated Bob Heimann!")

    def test_delete_child(self):
        children = self.child_list_page.get_list_elements()
        children_length = len(children)
        child_list_page = self.child_list_page.delete_child(children[0])
        new_children = child_list_page.get_list_elements()
        self.assertEqual(len(new_children), children_length - 1)


class TaskFunctionalTests(FactoryFunctionalTestCase):
    def setUp(self):
        self.driver = webdriver.Firefox(executable_path="chores/tests/drivers/geckodriver.exe")
        self.driver.implicitly_wait(3)
        self.factories.populate_tasks()
        self.driver.get(self.get_full_url(reverse("chores:task_list")))
        self.task_list_page = TaskListPage(self.driver)

    def tearDown(self):
        self.driver.refresh()
        self.driver.quit()

    def test_task_list(self):
        self.assertEqual(self.task_list_page.get_title(), "Chore Tracker")
        self.assertEqual(self.task_list_page.get_heading().text, "Tasks")
        self.assertEqual(len(self.task_list_page.get_list_elements()), len(Task.objects.all()))

    def test_task_detail(self):
        tasks = self.task_list_page.get_list_elements()
        detail_page = self.task_list_page.goto_task_detail(tasks[0])
        self.assertEqual(detail_page.get_heading().text, self.factories.mow.name)

    def test_create_new_task(self):
        new_task_page = self.task_list_page.goto_task_new()
        self.assertEqual(new_task_page.get_heading().text, "New Task")
        new_task_page.fill_out_form("Wash Bathroom", 15, True)
        detail_page = new_task_page.submit_form()
        self.assertEqual(detail_page.get_heading().text, "Wash Bathroom")
        self.assertEqual(detail_page.get_messages().text, "Successfully created Wash Bathroom!")

    def test_create_new_bad_task(self):
        new_task_page = self.task_list_page.goto_task_new()
        self.assertEqual(new_task_page.get_heading().text, "New Task")
        new_task_page.fill_out_form("Wash Bathroom", -15, True)
        form_page = new_task_page.submit_bad_form()
        self.assertIn("-15 is less than 0, needs to be non-negative", form_page.get_errors_list())

    def test_edit_task(self):
        tasks = self.task_list_page.get_list_elements()
        self.assertEqual(self.task_list_page.get_item_detail(tasks[0]).text, self.factories.mow.name)
        edit_page = self.task_list_page.goto_task_edit(tasks[0])
        self.assertEqual(edit_page.get_heading().text, "Edit Task")
        edit_page.fill_out_form(name="Make Bed")
        detail_page = edit_page.submit_form()
        self.assertEqual(detail_page.get_heading().text, "Make Bed")
        self.assertEqual(detail_page.get_messages().text, "Successfully updated Make Bed!")

    def test_delete_task(self):
        tasks = self.task_list_page.get_list_elements()
        tasks_length = len(tasks)
        task_list_page = self.task_list_page.delete_task(tasks[0])
        new_tasks = task_list_page.get_list_elements()
        self.assertEqual(len(new_tasks), tasks_length - 1)





