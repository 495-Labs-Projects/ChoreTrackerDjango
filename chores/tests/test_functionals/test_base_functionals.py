from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from django.core.urlresolvers import reverse
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from chores.tests.utilities import *
from chores.tests.pages.child_pages import *
from chores.tests.pages.task_pages import *
from chores.tests.pages.chore_pages import *

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
        task_list_page = self.child_list_page.goto_tasks_nav(TaskListPage)
        self.assertEqual(task_list_page.get_chores_nav().text, "Chores")
        chore_list_page = task_list_page.goto_chores_nav(ChoreListPage)
        self.assertEqual(chore_list_page.get_children_nav().text, "Children")
        child_list_page = chore_list_page.goto_children_nav(ChildListPage)