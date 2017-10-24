from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from django.core.urlresolvers import reverse
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from chores.tests.utilities import *


class FactoryFunctionalTestCase(StaticLiveServerTestCase):
    factories = Populate()

    # Auxiliary function to add view subdir to URL
    def get_full_url(self, url):
        return self.live_server_url + url

    # Wait page load by element id presence
    def wait_page_load(self, id):
        wait = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, id))
            )

class ChildFunctionalTests(FactoryFunctionalTestCase):
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

        self.wait_page_load("child-name")

        name = driver.find_element_by_id("child-name")
        self.assertEqual("John Smith", name.text) 

