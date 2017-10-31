# Objectives
In this lab we will be working with the ChoreTracker Django application and fully testing it out. There are three main test categories that are covered:
  - Model/Unit tests (uses the python unittest library)
  - View tests (equivalent to controller tests for rails also using unittest)
  - Functional tests (uses selenium to interact with the actual application)

# Part 1 - Model/Unit Tests

# Part 2 - View Tests

# Part 3 - Functional test
We will actually be using this framework called Selenium to help with functional tests. Usually we will need to pip install it, but we already have included it in the started code as part of the requirements. To learn more about the framework check this out (especially since you will be needing their documentation to write these tests): http://selenium-python.readthedocs.io/

1. To get started, just like with the model and view test, we will need to createa a new file called ```test_functionals.py``` under the tests directory of the chores app. 

2. Just like before we will probably need some factory test class, that all the other test classes will extend, to contain the factories and a way to populate the databse. However, since this is a functional test, this class will need to extend the ```StaticLiveServerTestCase```. There are two other helper functions that we need:
    - In this super class, we will also need a helper method to get the absolute full URL of the pages we are visiting since the ```reverse``` function can only get us the relative path. We also can't assume that it will always be at localhost:3000, so we will need to get the host from the ```live_server_url``` field.
    - We will also need a ```wait_page_load``` helper method. This method is very useful when loading a new page or navigating to another page. What it does is, given an element (let's say a heading) it will wait until that element shows up. If it doesn't show up before some unit of time (10 seconds for now) then the test fails. Basically it's used to make sure that the specified page has successfully loaded. What this means is that the element that we pass in has to be an element that uniquely identifies the existence of the page. So for example, if we are navigating to Google, we will probably pass in the google logo element to the function and wait until Google has loaded and the logo shows up.
    
    ```python
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC

    from django.core.urlresolvers import reverse
    from django.contrib.staticfiles.testing import StaticLiveServerTestCase

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
    ```

3. Before we continue we will also need something called a web driver which allows us to interact with a browser (either Firefox or Chrome in this case). To do so, go to the following respective links and download the right driver for your system. Then move that driver from your Downloads folder to a new folder called drivers under the tests directory: ```/chores/tests/drivers```.
  - Firefox: https://github.com/mozilla/geckodriver/releases
  - Chrome: https://sites.google.com/a/chromium.org/chromedriver/downloads

3. First let's get started on testing out the Child pages (list, detail, new, edit) and how a user can do the CRUD operations. Let's create a new test class called ```ChildFunctionalTests``` and have it extend the ```FactoryFunctionalTestCase``` class that we just created. In each of these classes we can override the ```setUp``` and ```tearDown``` methods. Let's create those methods! 
    - In the setUp method we need to define the driver, set an implicit wait of 3 seconds to not treat a slow load times as failure, and populating the children.
        ```python
        def setUp(self):
            # For chrome do:
            # self.driver = webdriver.Chrome(executable_path="chores/tests/drivers/chromedriver.exe")
            self.driver = webdriver.Firefox(executable_path="chores/tests/drivers/geckodriver.exe")
            self.driver.implicitly_wait(3)
            self.factories.populate_children()
        ```
    - In the tearDown method, all we need to do is quit the driver/browser once the test is done. A refresh is also needed in order to make sure that the browser is ready to quit. 
        ```python
        def tearDown(self):
            self.driver.refresh()
            self.driver.quit()
        ```



