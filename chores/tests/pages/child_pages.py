from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import chores.tests.pages.base_pages as base

class ChildListPage(base.ListPage):
    def __init__(self, driver):
        super().__init__(driver)
        self.page_element = (By.ID, "child-list")
        self.list = (By.ID, "child-list")
        self.new = (By.ID, "child-new")
        self.detail = (By.CLASS_NAME, "child-detail")
        self.edit = (By.CLASS_NAME, "child-edit")
        self.delete = (By.CLASS_NAME, "child-delete")

    def goto_child_detail(self, list_item):
        self.get_item_detail(list_item).click()
        detail_page = ChildDetailPage(self.driver)
        detail_page.check_page_element()
        return detail_page

    def goto_child_edit(self, list_item):
        self.get_item_edit(list_item).click()
        edit_page = ChildFormPage(self.driver)
        edit_page.check_page_element()
        return edit_page

    def delete_child(self, list_item):
        self.get_item_delete(list_item).click()
        alert = self.driver.switch_to_alert()
        alert.accept()
        list_page = ChildListPage(self.driver)
        list_page.check_page_element()
        return list_page

    def goto_child_new(self):
        self.get_new().click()
        new_page = ChildFormPage(self.driver)
        new_page.check_page_element()
        return new_page

class ChildDetailPage(base.DetailPage):
    def __init__(self, driver):
        super().__init__(driver)
        self.page_element = (By.ID, "child-name")
        self.heading = (By.ID, "child-name")
        self.details = (By.ID, "child-details")

class ChildFormPage(base.FormPage):
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

    def fill_out_form(self, first_name=None, last_name=None, active=None):
        if(first_name):
            self.get_first_name_input().clear()
            self.set_first_name_input(first_name)
        if(last_name):
            self.get_last_name_input().clear()
            self.set_last_name_input(last_name)
        if(active):
            self.set_active_input(active)

    def submit_form(self):
        self.get_form().submit()
        detail_page = ChildDetailPage(self.driver)
        detail_page.check_page_element()
        return detail_page
