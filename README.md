# Objectives
In this lab we will be working with the ChoreTracker Django application and fully testing it out. There are three main test categories that are covered:
  - Model/Unit tests (uses the python unittest library)
  - View tests (equivalent to controller tests for rails also using unittest)
  - Functional tests (uses selenium to interact with the actual application)

# Part 1 - Model/Unit Tests

# Part 2 - View Tests

# Part 3 - Functional test
We will actually be using this framework called Selenium to help with functional tests. Usually we will need to pip install it, but we already have included it in the started code as part of the requirements. To learn more about the framework check this out (especially since you will be needing their documentation to write these tests): http://selenium-python.readthedocs.io/

### Setup Selenium Tests
1. To get started, just like with the view tests, we will need to create a new folder under the chores tests folder called test_functionals: ```chores/tests/test_functionals```. Within this folder, let's first create a file called ```test_base_functionals.py```. 

2. Just like before we will probably need some factory test class, that all the other test classes will extend, to contain the factories and a way to populate the database. However, since this is a functional test, this class will need to extend the ```StaticLiveServerTestCase```. There are two other helper functions that we need:
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


### Testing out Children Pages

4. First let's get started on testing out the Child pages (list, detail, new, edit) and how a user can do the CRUD operations. Before we do so, we will need to create a new file under the test_functionals folder called test_child_functionals: ```chores/tests/test_functionals/test_child_functionals.py```

5. Within the new file that you created, let's create a new test class called ```ChildFunctionalTests``` and have it extend the ```FactoryFunctionalTestCase``` class that we just created. In each of these classes we can override the ```setUp``` and ```tearDown``` methods. Let's create those methods! 
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
        
  6. Now we can go and test the list/index page of the children views. Add the following to the new test class that you created and fill in the blanks denoted by <>. Read the comments carefully and carefully read the documentation to figure out how to find web elements and use selenium.
    - What reverse does is a reverse lookup of the relative path associated to the child_list page. The name chores:child_list is from the urls.py file which denotes the app name and the path name.
    - self.driver.get() actually goes to the specified url on the browser
    - when you use any sort of ```find_element_by_*()``` it will return a WebElement object. You can cann find_element again on the WebElement to find a nested tag (hint: maybe you can use it for finding the list elements).
      - ```find_element_by_*()``` finds and returns only 1 element and raises an error if none is found
      - ```find_elements_by_*()``` finds and returns a list of the elements and returns an emtpy list if none is found
      - Look at the documentation for details, but common ones are: ```find_element_by_id```, ```find_element_by_class_name```, ```find_element_by_tag_name```, ```find_element_by_css_selector```

    ```python
    def test_child_list(self):
        # Go to the Children List page
        # finds the relative path using reverse and get the full path using our helper method
        url = self.get_full_url(reverse("chores:child_list")) 
        # actually goes to the url specified
        self.driver.get(url) 
    
        # Check that the page's title is right
        self.assertIn("Chore Tracker", "<the page title>") # look at the selenium api to see how to get the page's title
    
        # Check that the page heading is right
        heading = self.driver.find_element_by_tag_name("h1")
        self.assertIn("Children", "<the heading's text>") # figure out how to get a web element's text
    
        # Check that the number of children listed is equal to the number of children in the database
        children = "<list of children list items>" # figure out how to find the list of web elements 
        self.assertEqual(len(children), Child.objects.count()) 
    ```
7. If you don't get how to fill in the blanks, please ask a TA for help since this is crucial for all Selenium testing in the future! Once you are done, we will try to run the test! But first we will need to add one more file in the ```test_functionals``` folder called ```__init__.py``` to set up the package and in this file all we need is the following:
```python
from .test_base_functionals import *
from .test_child_functionals import *
```

8. After we add the init file, we can finally run the functional tests and see selenium in action! Go to your command prompt and run: ```python manage.py test chores.tests.test_functionals``` This should open up Firefox and Chrome really quickly, run the tests and then quit.

9. Now that we have written a quick test for testing out the child list page, we will do the same for a child detail page and creating a new child. Fill in the blanks just like before between the <>. 

```python
def test_child_detail(self):
        # Go to Alex's detail page by his id
        url = self.get_full_url(reverse("chores:child_detail", args=(self.factories.alex.id,)))
        self.driver.get(url)

        # Check that the child's name is correct
        name = "<the element containing the child name>" # to make things simple you can just find the element for the heading, which has the child's name
        # Then assert that the name is correct and is as expected

    def test_create_new_child(self):
        url = "<the new page's url>" # use reverse and get_full_url to return the right url for the new child page
        self.driver.get(url)

        # In this section we will be trying to create a new child called John Smith, by filling out the new form step by step
        # Use the following example to fill out the first and last name input fields
        # An example of finding an input tag and entering in some text is the following:
        # input = self.driver.find_element_by_id("some_input_id")
        # input.send_keys("Some Text")
        
        self.driver.find_element_by_tag_name("form").submit() # actually submits the form

        self.wait_page_load((By.ID, "<the detail page's defining element>")) # pick an id to put in here so that that wait_page_load knows that the new child's detail page is loaded

        name = self.driver.find_element_by_id("child-name")
        self.assertEqual("John Smith", name.text) 
```

10. Now that we have written all the tests, you can run them using the same command as before! Make sure that everything passes.

Note: If you had trouble writing all the tests, and didn't want to keep on rerunning the tests, you can use this tool called pdb. It's basically a Python debugger like byebug and you can set a breakpoint within your selenium tests and you can interact with the browser and see if your code found the right elements or clicked the right things.

Another Note: ```python manage.py test chores.tests.test_functionals``` runs all your tests, but if you want to run a specific test class like your child test class you would run ```python manage.py test chores.tests.test_functionals.ChildFunctionalTests``` and if you want to drill even more down to a specific test function then you will need to run ```python manage.py test chores.tests.test_functionals.ChildFunctionalTests.test_child_list```

# <span class="mega-icon mega-icon-issue-opened"></span>Stop
Show a TA that you have completed writing the first part of the selenium tests. Make sure the TA initials your sheet.
* * *

### Improving the Child Tests

11. Now that we have written some basic Selenium test, testing out the child's list, detail, and new page, we may realize how tedious this may be. In order to improve the format of these tests, we have actually created a framework for you guys to use! This framework is built on the idea of not having you write so many ```find_element_by_*``` just to fill out a form. This framework that we built uses the idea of pages and having each page that you visit be represented by a page object. In each page class (either child list page, detail page, form page, etc.) there are certain actions that you can take like filling out a form. All you need to do now is to call the ```fill_out_form(param)``` on the child form object and it'll fill out the form for you with the right information without having you to find all the right elements. Please go to the ```chores/tests/pages``` folder and look over the ```base_pages.py``` and ```child_pages.py``` files and make sure you understand the general framework and all the functions available to you. Please ask a TA if you need help understanding what is going on!

12. Once you have familiarized yourself with the pages framework we will write the same tests using the framework. Comment out the old test class and create a whole new class like the following:
```python
class ChildFunctionalTests(FactoryFunctionalTestCase):
    def setUp(self):
        self.driver = webdriver.Firefox(executable_path="chores/tests/drivers/geckodriver.exe")
        self.driver.implicitly_wait(3)
        self.factories.populate_children()
        # Now in the setup we actually want to first go to the child list page and set the field child_list_page to a new ChildListPage object. In the following tests, we can just interact with the child_list_page object.
        self.driver.get(self.get_full_url(reverse("chores:child_list")))
        self.child_list_page = ChildListPage(self.driver)

    def tearDown(self):
        self.driver.refresh()
        self.driver.quit()
```

13. Now that you have the setup/teardown finished, we can start writing the tests! Just like before we will have 3 tests (testing the child list page, a child detail page, and creating a new child). There are just some places where you will need to fill in the blanks again, but these tests will basically do the exact same thing as the previous tests that we wrote, except much more simpler and easy.
```python
    def test_child_list(self):
        self.assertEqual(self.child_list_page.get_title(), "Chore Tracker")
        self.assertEqual(self.child_list_page.get_heading().text, "Children")
        # Assert that the number of list items equals the number of child objects in the database

    def test_child_detail(self):
        children = self.child_list_page.get_list_elements()
        detail_page = self.child_list_page.goto_child_detail(children[0])
        # Assert that the detail page's heading name is the correct name

    def test_create_new_child(self):
        new_child_page = self.child_list_page.goto_child_new()
        self.assertEqual(new_child_page.get_heading().text, "New Child")
        new_child_page.fill_out_form("John", "Smith", True)
        detail_page = new_child_page.submit_form(ChildDetailPage) # We will need to pass in ChildDetailPage because that is the type of page that we expect back since all validations should pass. If validations fail we should expect back a ChildFormPage again but with the errors
        # Assert that the detail page heading is John Smith
        # Assert that the proper success message is shown
```

13. Run these tests and make sure that they all pass just like before.

14. Now that you got the hang of writing the same selenium tests using the pages framework, you will need to write 2 more tests, testing out the edit and delete functionality! To do this you will need to go through the child list page and click on the edit and delete buttons for any of the children. 

# <span class="mega-icon mega-icon-issue-opened"></span>Stop
Show a TA that you have completed writing all the child page tests using the pages framework. Make sure the TA initials your sheet.
* * *

### Writing all the other tests

14. We will now have you write all the tests for the task pages by yourself. You will need to create a new file called ```chores/tests/test_functionals/test_task_functionals.py```. Basically test exactly the same things as we did for the child pages but for the task pages. One extra thing that you would want to test in the task pages is what happens when you submit a bad form (like maybe with a negative points value?).

15. There are also 2 hidden bugs that we want you to find out during your tests! Fix these bugs and make sure all your tests pass!

(Hint 1: You should probably test out the basic page links like maybe if the navbar links lead you to the right pages?)

(Hint 2: You should so make sure that all page headings are right for each page.)

(Hint 3: If hint 2 didn't help, take a closer look at the edit page for tasks and see if there is anything wrong.)

