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

    # Given a web element to click and the expected page_class that will load, 
    # this method will click the element and return an instance of the expected page_class
    def goto_page(self, click_element, page_class):
        click_element.click()
        page = page_class(self.driver)
        page.check_page_element()
        return page

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

    # Returns the navbar's web element
    def get_navbar(self):
        return self.driver.find_element(*self.navbar_element)

    # Returns the web element for the Children link in the navbar
    def get_children_nav(self):
        return self.driver.find_element(*self.children_nav)

    # Returns the web element for the Tasks link in the navbar
    def get_tasks_nav(self):
        return self.driver.find_element(*self.tasks_nav)

    # Returns the web element for the Chores link in the navbar
    def get_chores_nav(self):
        return self.driver.find_element(*self.chores_nav)

    # Click on the children navbar link and returns back the expected page
    def goto_children_nav(self, page_class=BasePage):
        return self.goto_page(self.get_children_nav(), page_class)

    # Click on the tasks navbar link and returns back the expected page
    def goto_tasks_nav(self, page_class=BasePage):
        return self.goto_page(self.get_tasks_nav(), page_class)

    # Click on the chores navbar link and returns back the expected page
    def goto_chores_nav(self, page_class=BasePage):
        return self.goto_page(self.get_chores_nav(), page_class)

    # Returns the web element for the footer
    def get_footer(self):
        return self.driver.find_element(*self.footer_element)

    # Returns the web element for the messages (mostly for success messages)
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

    # Returns the web element of the heading
    def get_heading(self):
        return self.driver.find_element(*self.heading)

    # Returns the web element containing the full list
    def get_list(self):
        return self.driver.find_element(*self.list)

    # Returns the list of web elements containing all list items
    def get_list_elements(self):
        return self.get_list().find_elements(*(By.TAG_NAME, "li"))

    # Given a list item, it will return the web element that links to the details page for the item
    def get_item_detail(self, list_item):
        return list_item.find_element(*self.detail)

    # Given a list item, it will return the web element that links to the edit page for the item
    def get_item_edit(self, list_item):
        return list_item.find_element(*self.edit)

    # Given a list item, it will return the web element deletes the item
    def get_item_delete(self, list_item):
        return list_item.find_element(*self.delete)

    # Returns the web element that contains the link to the new form
    def get_new(self):
        return self.driver.find_element(*self.new)

    # Given a list_item and the expected page_class, it will try and delete the item
    # This method will be used by the sub classes to delete items
    def delete_list_item(self, list_item, page_class):
        self.get_item_delete(list_item).click()
        alert = self.driver.switch_to_alert()
        alert.accept()
        list_page = page_class(self.driver)
        list_page.check_page_element()
        return list_page

# The base Detail Page class that represents a basic detail view of object.
# The following are its fields (not including the inheritted fields)
#   details => the web element that contains all the details of the object
#   back_to_list => the web element that contains the link that goes back to the list view 
class DetailPage(ChoreTrackerPage):
    def __init__(self, driver):
        super().__init__(driver)
        self.heading = (By.ID, "name")
        self.details = (By.ID, "details")
        self.back_to_list = (By.ID, "back-to-list")

    # Returns the web element of the heading
    def get_heading(self):
        return self.driver.find_element(*self.heading)

    # Returns the web element of the details for the specific item
    def get_details(self):
        return self.driver.find_element(*self.details)

    # Returns the web element containing the link to go back to the list page
    def get_back_to_list(self):
        return self.driver.find_element(*self.back_to_list)

# The base Form Page class that represents a basic form view of object. The form page is the same for both new and edit pages.
# The following are its fields (not including the inheritted fields). All pages that inherit this class should have
# additional fields describing each input (either to get, set, and fill out the form)
#   form => the web element describing the form itself
#   errors => the web elements that describe the errors (either field specific or not)
class FormPage(ChoreTrackerPage):
    def __init__(self, driver):
        super().__init__(driver)
        self.page_element = (By.TAG_NAME, "form")
        self.heading = (By.TAG_NAME, "h1")
        self.form = (By.TAG_NAME, "form")
        self.errors = (By.CLASS_NAME, "errorlist")

    # Returns the web element of the heading
    def get_heading(self):
        return self.driver.find_element(*self.heading)

    # Returns the web element of the form
    def get_form(self):
        return self.driver.find_element(*self.form)

    # Returns the web elements of all the errors
    def get_errors(self):
        return self.driver.find_elements(*self.errors)

    # Returns a list of all the error messages' texts
    def get_errors_list(self):
        errors_list = []
        for error in self.get_errors():
            error_messages = error.find_elements(By.TAG_NAME, "li")
            errors_list.extend([msg.text for msg in error_messages])
        return errors_list

    # Submits the form after you fill it out. Give expected page_class depending on whether or not the form is valid
    # For example, you would expect it to return a DetailPage if the form sucessfully submits/saves
    # You would expect it to return the same FormPage with errors if the form isn't valid
    def submit_form(self, page_class=DetailPage):
        self.get_form().submit()
        detail_page = page_class(self.driver)
        detail_page.check_page_element()
        return detail_page
