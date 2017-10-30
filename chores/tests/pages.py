from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BasePage(object):
    def __init__(self, driver):
        self.driver = driver
        self.page_element = (By.TAG_NAME, "body")
        self.timeout = 5

    def get_title(self):
        return self.driver.title

    def check_page_element(self):
        WebDriverWait(self.driver, self.timeout).until(
                EC.presence_of_element_located(self.page_element)
            )

    def find_elements_or_one(self, selector, parent=None):
        parent = parent if parent else self.driver
        elements = parent.find_elements(*selector)
        if(len(elements) == 0):
            return parent.find_element(*selector)
        elif(len(elements) == 1):
            return elements[0]
        else:
            return elements

class ManagerPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.page_element = (By.ID, "navbar")
        self.navbar_element = (By.ID, "navbar")
        self.footer_element = (By.ID, "footer")
        self.messages_element = (By.ID, "messages")

    def get_navbar(self):
        return self.driver.find_element(*self.navbar_element)

    def get_footer(self):
        return self.driver.find_element(*self.footer_element)

    def get_messages(self):
        return self.driver.find_element(*self.messages_element)

class ListPage(ManagerPage):
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

    def get_element_detail(self, element):
        return element.find_element(*self.detail)

    def get_element_edit(self, element):
        return element.find_element(*self.edit)

    def get_element_delete(self, element):
        return element.find_element(*self.delete)

    def get_new(self):
        return self.driver.find_element(*self.new)

class DetailPage(ManagerPage):
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

class FormPage(ManagerPage):
    def __init__(self, driver):
        super().__init__(driver)
        self.page_element = (By.TAG_NAME, "form")
        self.form = (By.TAG_NAME, "form")

    def get_form(self):
        return self.driver.find_element(*self.form)

class ChildListPage(ListPage):
    def __init__(self, driver):
        super().__init__(driver)
        self.page_element = (By.ID, "child-list")
        self.list = (By.ID, "child-list")
        self.new = (By.ID, "child-new")
        self.detail = (By.CLASS_NAME, "child-detail")
        self.edit = (By.CLASS_NAME, "child-edit")
        self.delete = (By.CLASS_NAME, "child-delete")

    def goto_child_detail(self, element):
        self.get_element_detail(element).click()
        detail_page = ChildDetailPage(self.driver)
        detail_page.check_page_element()
        return detail_page

    def goto_child_edit(self, element):
        self.get_element_edit(element).click()
        edit_page = ChildFormPage(self.driver)
        edit_page.check_page_element()
        return edit_page

    def delete_child(self, element):
        self.get_element_edit(element).click()
        alert = self.driver.switch_to.alert()
        alert.accept()
        list_page = ChildListPage(self.driver)
        list_page.check_page_element()
        return list_page

    def goto_child_new(self):
        self.get_new().click()
        new_page = ChildFormPage(self.driver)
        new_page.check_page_element()
        return new_page

class ChildDetailPage(DetailPage):
    def __init__(self, driver):
        super().__init__(driver)
        self.page_element = (By.ID, "child-name")
        self.heading = (By.ID, "child-name")
        self.details = (By.ID, "child-details")

class ChildFormPage(FormPage):
    def __init__(self, driver):
        super().__init__(driver)
        self.first_name_input = (By.ID, "id_first_name")
        self.last_name_input = (By.ID, "id_last_name")
        self.active_input = (By.ID, "id_active")

    def get_first_name_input(self):
        return self.driver.find_element(*self.first_name_input)

    def get_last_name_input(self):
        return self.driver.find_element(*self.last_name_input)

    def get_active_input(self):
        return self.driver.find_element(*self.active_input)

    def get_first_name_value(self):
        return self.get_first_name_input().get_attribute("value")

    def get_last_name_value(self):
        return self.get_last_name_input().get_attribute("value")

    def get_active_value(self):
        return self.get_active_input().is_selected()

    def set_first_name_input(self, first_name):
        self.get_first_name_input().send_keys(first_name)

    def set_last_name_input(self, last_name):
        self.get_last_name_input().send_keys(last_name)

    def set_active_input(self, active):
        active_input = self.get_active_input()
        if((active and not active_input.is_selected()) or 
            (not active and active_input.is_selected())):
            active_input.click()

    def fill_out_form(self, first_name, last_name, active):
        self.set_first_name_input(first_name)
        self.set_last_name_input(last_name)
        self.set_active_input(active)

    def submit_form(self):
        self.get_form().submit()
        detail_page = ChildDetailPage(self.driver)
        detail_page.check_page_element()
        return detail_page





    