from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from django.core.urlresolvers import reverse
from chores.tests.test_functionals.test_base_functionals import FactoryFunctionalTestCase

from chores.tests.utilities import *
from chores.tests.pages.task_pages import *

driverType = "geckodriver"

class TaskFunctionalTests(FactoryFunctionalTestCase):
    def setUp(self):
        self.driver = webdriver.Firefox(executable_path="chores/tests/drivers/"+driverType)
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
        detail_page = new_task_page.submit_form(TaskDetailPage)
        self.assertEqual(detail_page.get_heading().text, "Wash Bathroom")
        self.assertEqual(detail_page.get_messages().text, "Successfully created Wash Bathroom!")

    def test_create_new_bad_task(self):
        new_task_page = self.task_list_page.goto_task_new()
        self.assertEqual(new_task_page.get_heading().text, "New Task")
        new_task_page.fill_out_form("Wash Bathroom", -15, True)
        form_page = new_task_page.submit_form(TaskFormPage)
        self.assertIn("Ensure this value is greater than or equal to 0.", form_page.get_errors_list())

    def test_edit_task(self):
        tasks = self.task_list_page.get_list_elements()
        self.assertEqual(self.task_list_page.get_item_detail(tasks[0]).text, self.factories.mow.name)
        edit_page = self.task_list_page.goto_task_edit(tasks[0])
        self.assertEqual(edit_page.get_heading().text, "Edit Task")
        edit_page.fill_out_form(name="Make Bed")
        detail_page = edit_page.submit_form(TaskDetailPage)
        self.assertEqual(detail_page.get_heading().text, "Make Bed")
        self.assertEqual(detail_page.get_messages().text, "Successfully updated Make Bed!")

    def test_delete_task(self):
        tasks = self.task_list_page.get_list_elements()
        tasks_length = len(tasks)
        task_list_page = self.task_list_page.delete_task(tasks[0])
        new_tasks = task_list_page.get_list_elements()
        self.assertEqual(len(new_tasks), tasks_length - 1)
