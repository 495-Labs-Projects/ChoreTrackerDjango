from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from django.core.urlresolvers import reverse
from chores.tests.test_functionals.test_base_functionals import FactoryFunctionalTestCase

from chores.tests.utilities import *
from chores.tests.pages.child_pages import *


# Tedious Way
class TediousChildFunctionalTests(FactoryFunctionalTestCase):
    def setUp(self):
        self.driver = webdriver.Firefox(executable_path="chores/tests/drivers/geckodriver.exe")
        self.driver.implicitly_wait(3)
        self.factories.populate_children()

    def tearDown(self):
        self.driver.refresh()
        self.driver.quit()
    
    def test_child_list(self):
        # Go to the Children List page
        url = self.get_full_url(reverse("chores:child_list"))
        self.driver.get(url)

        # Check that the page's title is right
        self.assertIn("Chore Tracker", self.driver.title)

        # Check that the page heading is right
        heading = self.driver.find_element_by_tag_name("h1")
        self.assertIn("Children", heading.text)

        # Check that the number of children listed is equal to the number of children in the database
        children = self.driver.find_elements_by_css_selector("#child-list li")
        self.assertEqual(len(children), Child.objects.count()) 

    def test_child_detail(self):
        # Go to Alex's detail page
        url = self.get_full_url(reverse("chores:child_detail", args=(self.factories.alex.id,)))
        self.driver.get(url)

        # Check that the child's name is correct
        name = self.driver.find_element_by_id("child-name")
        self.assertEqual(self.factories.alex.name(), name.text)

    def test_create_new_child(self):
        url = self.get_full_url(reverse("chores:child_new"))
        self.driver.get(url)

        first_name_input = self.driver.find_element_by_id("id_first_name")
        first_name_input.send_keys("John")

        last_name_input = self.driver.find_element_by_id("id_last_name")
        last_name_input.send_keys("Smith")

        self.driver.find_element_by_tag_name("form").submit()

        self.wait_page_load((By.ID, "child-name"))

        name = self.driver.find_element_by_id("child-name")
        self.assertEqual("John Smith", name.text) 


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
        detail_page = new_child_page.submit_form(ChildDetailPage)
        self.assertEqual(detail_page.get_heading().text, "John Smith")
        self.assertEqual(detail_page.get_messages().text, "Successfully created John Smith!")

    def test_edit_child(self):
        children = self.child_list_page.get_list_elements()
        self.assertEqual(self.child_list_page.get_item_detail(children[0]).text, self.factories.alex.name())
        edit_page = self.child_list_page.goto_child_edit(children[0])
        self.assertEqual(edit_page.get_heading().text, "Edit Child")
        edit_page.fill_out_form(first_name="Bob")
        detail_page = edit_page.submit_form(ChildDetailPage)
        self.assertEqual(detail_page.get_heading().text, "Bob Heimann")
        self.assertEqual(detail_page.get_messages().text, "Successfully updated Bob Heimann!")

    def test_delete_child(self):
        children = self.child_list_page.get_list_elements()
        children_length = len(children)
        child_list_page = self.child_list_page.delete_child(children[0])
        new_children = child_list_page.get_list_elements()
        self.assertEqual(len(new_children), children_length - 1)