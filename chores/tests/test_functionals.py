from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from django.core.urlresolvers import reverse
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from chores.tests.utilities import *
from chores.tests.pages import *


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

# firefox create selenium tests extension

# Tedious Way
# class ChildFunctionalTests(FactoryFunctionalTestCase):
#     def setUp(self):
#         self.driver = webdriver.Firefox(executable_path="chores/tests/drivers/geckodriver.exe")
#         self.driver.implicitly_wait(3)
#         self.factories.populate_children()

#     def tearDown(self):
#         self.driver.quit()
    
#     def test_child_list(self):
#         driver = self.driver
#         self.driver.get(self.get_full_url(reverse("chores:child_list")))

#         self.assertIn("Chore Tracker", driver.title)
#         heading = driver.find_element_by_css_selector("h1")
#         self.assertIn("Children", heading.text)

#         children = driver.find_elements_by_css_selector("#child-list li")
#         self.assertEqual(len(children), Child.objects.count()) 

#     def test_child_detail(self):
#         driver = self.driver
#         self.driver.get(self.get_full_url(reverse("chores:child_detail", args=(self.factories.alex.id,))))

#         name = driver.find_element_by_id("child-name")
#         self.assertEqual(self.factories.alex.name(), name.text)

#     def test_create_new_child(self):
#         driver = self.driver
#         self.driver.get(self.get_full_url(reverse("chores:child_new")))

#         first_name_input = driver.find_element_by_id("id_first_name")
#         first_name_input.send_keys("John")

#         last_name_input = driver.find_element_by_id("id_last_name")
#         last_name_input.send_keys("Smith")

#         first_name_input.submit()

#         self.wait_page_load((By.ID, "child-name"))

#         name = driver.find_element_by_id("child-name")
#         self.assertEqual("John Smith", name.text) 


class BetterChildFunctionalTests(FactoryFunctionalTestCase):
    def setUp(self):
        self.driver = webdriver.Firefox(executable_path="chores/tests/drivers/geckodriver.exe")
        self.driver.implicitly_wait(3)
        self.factories.populate_children()
        self.driver.get(self.get_full_url(reverse("chores:child_list")))
        self.child_list_page = ChildListPage(self.driver)

    def tearDown(self):
        self.driver.quit()

    def test_child_list(self):
        self.assertEquals(self.child_list_page.get_title(), "Chore Tracker")
        self.assertEquals(self.child_list_page.get_heading().text, "Children")
        self.assertEquals(len(self.child_list_page.get_list_elements()), len(Child.objects.all()))

    def test_child_detail(self):
        children = self.child_list_page.get_list_elements()
        detail_page = self.child_list_page.goto_child_detail(children[0])
        self.assertEquals(detail_page.get_heading().text, self.factories.alex.name())

    def test_create_new_child(self):
        new_child_page = self.child_list_page.goto_child_new()
        new_child_page.fill_out_form("John", "Smith", True)
        detail_page = new_child_page.submit_form()
        self.assertEquals(detail_page.get_heading().text, "John Smith")
        self.assertEquals(detail_page.get_messages().text, "Successfully created John Smith!")



