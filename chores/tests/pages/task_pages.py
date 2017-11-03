from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import chores.tests.pages.base_pages as base


class TaskDetailPage(base.DetailPage):
    def __init__(self, driver):
        super().__init__(driver)
        self.page_element = (By.ID, "task-name")
        self.heading = (By.ID, "task-name")
        self.details = (By.ID, "task-details")


class TaskFormPage(base.FormPage):
    def __init__(self, driver):
        super().__init__(driver)
        self.name_input = (By.ID, "id_name")
        self.points_input = (By.ID, "id_points")
        self.active_input = (By.ID, "id_active")

    def get_name_input(self):
        return self.driver.find_element(*self.name_input)

    def get_points_input(self):
        return self.driver.find_element(*self.points_input)

    def get_active_input(self):
        return self.driver.find_element(*self.active_input)

    def get_name_value(self):
        return self.get_name_input().get_attribute("value")

    def get_points_value(self):
        return self.get_points_input().get_attribute("value")

    def get_active_value(self):
        return self.get_active_input().is_selected()

    def set_name_input(self, name):
        self.get_name_input().send_keys(name)

    def set_points_input(self, points):
        self.get_points_input().send_keys(points)

    def set_active_input(self, active):
        active_input = self.get_active_input()
        if((active and not active_input.is_selected()) or 
            (not active and active_input.is_selected())):
            active_input.click()

    def fill_out_form(self, name=None, points=None, active=None):
        if(name):
            self.get_name_input().clear()
            self.set_name_input(name)
        if(points):
            self.get_points_input().clear()
            self.set_points_input(points)
        if(active):
            self.set_active_input(active)


class TaskListPage(base.ListPage):
    def __init__(self, driver):
        super().__init__(driver)
        self.page_element = (By.ID, "task-list")
        self.list = (By.ID, "task-list")
        self.new = (By.ID, "task-new")
        self.detail = (By.CLASS_NAME, "task-detail")
        self.edit = (By.CLASS_NAME, "task-edit")
        self.delete = (By.CLASS_NAME, "task-delete")

    def goto_task_detail(self, list_item, page_class=TaskDetailPage):
        return self.goto_page(self.get_item_detail(list_item), page_class)

    def goto_task_edit(self, list_item, page_class=TaskFormPage):
        return self.goto_page(self.get_item_edit(list_item), page_class)

    def delete_task(self, list_item):
        return self.delete_list_item(list_item, TaskListPage)

    def goto_task_new(self, page_class=TaskFormPage):
        return self.goto_page(self.get_new(), page_class)

