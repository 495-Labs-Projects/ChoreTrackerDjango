from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import chores.tests.pages.base_pages as base

class ChoreListPage(base.ListPage):
  def __init__(self, driver):
    super().__init__(driver)
    self.page_element = (By.ID, "chore-list")
    self.list = (By.ID, "chore-list")
    self.new = (By.ID, "chore-new")
    self.detail = (By.CLASS_NAME, "chore-detail")
    self.edit = (By.CLASS_NAME, "chore-edit")
    self.delete = (By.CLASS_NAME, "chore-delete")


class ChoreDetailPage(base.DetailPage):
  pass

class ChoreFormPage(base.FormPage):
  pass