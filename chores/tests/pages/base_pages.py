from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time

# The Base Page class that represents the most fundamental fields of a page.
# The following are its fields
#   driver => the web driver that allows the page to interact with the actual page
#   page_element => the defining element that represents the page (used to tell if the page has shown up or not)
#   timeout => the timeout limit for any page load or waits (like waiting for a form to submit)
class BasePage(object):
    def __init__(self, driver):
        self.driver = driver
        self.page_element = (By.TAG_NAME, "body")
        self.timeout = 5

    # Returns the page's html title as a string
    def get_title(self):
        return self.driver.title

    # Check whether or not the page has shown up using the page_element
    # This will wait until the timeout time for the page_element to show up and will fail if not.
    # This is generally run when navigating between pages and submitting forms.
    def check_page_element(self, specific_element=None):
        element = specific_element if specific_element else self.page_element
        time.sleep(0.1)
        WebDriverWait(self.driver, self.timeout).until(
                EC.presence_of_element_located(element)
            )

# The base ChoreTracker Page class that represents a basic page in the ChoreTracker App.
# The following are its fields (not including the inheritted fields)
#   page_element => just for specificity, this is defined by the navbar since all ChoreTracker pages should have the navbar
#   navbar_element => the navbar webelement
#   footer_element => the footer webelement
#   messages_element => the messages webelement (used for displayed success messsages or notifications)
class ChoreTrackerPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.page_element = (By.ID, "navbar")
        self.navbar_element = (By.ID, "navbar")
        self.footer_element = (By.ID, "footer")
        self.messages_element = (By.ID, "messages")
        self.children_nav = (By.ID, "children-nav")
        self.tasks_nav = (By.ID, "tasks-nav")
        self.chores_nav = (By.ID, "chores-nav")

    def get_navbar(self):
        return self.driver.find_element(*self.navbar_element)

    def get_children_nav(self):
        return self.driver.find_element(*self.children_nav)

    def get_tasks_nav(self):
        return self.driver.find_element(*self.tasks_nav)

    def get_chores_nav(self):
        return self.driver.find_element(*self.chores_nav)

    def goto_children_nav(self):
        self.get_children_nav().click()
        child_list_page = ChoreTrackerPage(self.driver)
        child_list_page.check_page_element((By.ID, "child-list"))
        return child_list_page

    def goto_tasks_nav(self):
        self.get_tasks_nav().click()
        task_list_page = ChoreTrackerPage(self.driver)
        task_list_page.check_page_element((By.ID, "task-list"))
        return task_list_page

    def goto_chores_nav(self):
        self.get_chores_nav().click()
        chore_list_page = ChoreTrackerPage(self.driver)
        chore_list_page.check_page_element((By.ID, "chore-list"))
        return chore_list_page

    def get_footer(self):
        return self.driver.find_element(*self.footer_element)

    def get_messages(self):
        return self.driver.find_element(*self.messages_element)

# The base List Page class that represents a basic index view of each model. Each model should have one of these
# The following are its fields (not including the inheritted fields)
#   heading => the main heading of the list page (for a tasks it is generally the task name)
#   list => the list web element that represents the list of model objects (generally the <ul> or <ol> tags)
#   new => the create new model button that links you to a new form page
#   detail => within a list item element, it represents the link to the detail page of that model object
#   edit => within a list item element, it represents the link to the edit page of that model object
#   delete => within a list item element, it represents the delete button for that model object
class ListPage(ChoreTrackerPage):
    def __init__(self, driver):
        super().__init__(driver)
        self.heading = (By.TAG_NAME, "h1")
        self.list = (By.ID, "list")
        self.new = (By.ID, "new")
        self.detail = (By.CLASS_NAME, "detail")
        self.edit = (By.CLASS_NAME, "edit")
        self.delete = (By.CLASS_NAME, "delete")

    def get_heading(self):
        return self.driver.find_element(*self.heading)

    def get_list(self):
        return self.driver.find_element(*self.list)

    def get_list_elements(self):
        return self.get_list().find_elements(*(By.TAG_NAME, "li"))

    def get_item_detail(self, list_item):
        return list_item.find_element(*self.detail)

    def get_item_edit(self, list_item):
        return list_item.find_element(*self.edit)

    def get_item_delete(self, list_item):
        return list_item.find_element(*self.delete)

    def get_new(self):
        return self.driver.find_element(*self.new)

# The base Detail Page class that represents 
class DetailPage(ChoreTrackerPage):
    def __init__(self, driver):
        super().__init__(driver)
        self.heading = (By.ID, "name")
        self.details = (By.ID, "details")
        self.back_to_list = (By.ID, "back-to-list")

    def get_heading(self):
        return self.driver.find_element(*self.heading)

    def get_details(self):
        return self.driver.find_element(*self.details)

    def get_back_to_list(self):
        return self.driver.find_element(*self.back_to_list)

class FormPage(ChoreTrackerPage):
    def __init__(self, driver):
        super().__init__(driver)
        self.page_element = (By.TAG_NAME, "form")
        self.heading = (By.TAG_NAME, "h1")
        self.form = (By.TAG_NAME, "form")
        self.errors = (By.CLASS_NAME, "errorlist")

    def get_heading(self):
        return self.driver.find_element(*self.heading)

    def get_form(self):
        return self.driver.find_element(*self.form)

    def get_errors(self):
        return self.driver.find_elements(*self.errors)

    def get_errors_list(self):
        errors_list = []
        for error in self.get_errors():
            error_messages = error.find_elements(By.TAG_NAME, "li")
            errors_list.extend([msg.text for msg in error_messages])
        return errors_list
