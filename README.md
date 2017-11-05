# Objectives
In this lab we will be working with the ChoreTracker Django application and fully testing it out. There are three main test categories that are covered:
  - Model/Unit tests (uses the python unittest library)
  - View tests (equivalent to controller tests for rails also using unittest)
  - Functional tests (uses selenium to interact with the actual application)

# Part 1 - Model/Unit Tests
We will start by writing unit tests for our three models. Factories have been provided in `chores/tests/factories.py` and contexts for our tests have been created in `utilities.py`. Within our `chores/tests/` directory, add a subdirectory named `test_models`. Here, first add a `__init__.py` file, and then add our three unit test files: `test_child_models.py`, `test_chore_models.py`, and `test_task_models.py`.

1. We'll start by writing our unit tests for the child model. First, add the imports we'll need at the top of the file:

```python
    from django.core.exceptions import ValidationError
    from django.utils import timezone

    from chores.models import *
    from chores.tests.utilities import *
```

2. Let's first build the child test class and our initial setup method that makes use of our factories and contexts:

```python
    class ChildTests(FactoryTestCase):

        def setUp(self):
            self.factories.populate_chores()

```

3. First, we'll test the built-in validations that ensure blank values aren't accepted for first and last names. By default, Django fields don't accept blank values, so we should see these tests pass. Add the following code to the test class:

```python
    def test_validations(self):
        with self.assertRaises(ValidationError):
            bad_child1 = ChildFactory.create(first_name="")
            bad_child1.full_clean()

        with self.assertRaises(ValidationError):
            bad_child1 = ChildFactory.create(last_name="")
            bad_child1.full_clean()

```

4. Next, we'll test the `name` and `points_earned` methods by adding the following code to the test calss:

```python
    def test_name(self):
        self.assertEqual("Alex Heimann", self.factories.alex.name())
        self.assertEqual("Mark Heimann", self.factories.mark.name())
        self.assertEqual("Rachel Heimann", self.factories.rachel.name())

    def test_points_earned(self):
        self.assertEqual(4, self.factories.alex.points_earned())
        self.assertEqual(1, self.factories.mark.points_earned())
        self.assertEqual(0, self.factories.rachel.points_earned())

```

5. Finally, we'll test our two scopes, `alphabetical` and `active`:

```python
    def test_alphabetical(self):
        self.assertEqual(list(map(lambda child: child.first_name, Child.objects.alphabetical())), ["Alex", "Mark", "Rachel"])

    def test_active(self):
        self.assertEqual(list(map(lambda child: child.first_name, Child.objects.active().alphabetical())), ["Alex", "Mark"])

```

And that's it - we're done unit testing the Child model. For brevity, we'll leave testing the Task model to you as an additional exercise (your app should still be 100% tested!), and we'll move on to the Chore model.

1. In `test_chore_model.py`, make the same imports as you did for Child at the top of the file.

2. Start again by building our test class and the initial setup method:
    
```python
    class ChoreTests(FactoryTestCase):

    def setUp(self):
        self.factories.populate_chores()

```

3. We have a series of scopes to test for this model. Look through the following code to make sure you understand what is being tested, and add it to our test class:

```python
    def test_by_task(self):
        self.assertEqual(list(map(lambda chore: chore.task.name, Chore.objects.by_task())), ["Shovel driveway","Sweep floor","Sweep floor","Sweep floor", "Wash dishes","Wash dishes","Wash dishes"])

    def test_chronological(self):
        self.assertEqual(list(map(lambda chore: chore.task.name, Chore.objects.chronological())), ["Shovel driveway","Sweep floor","Wash dishes","Sweep floor","Wash dishes","Sweep floor","Wash dishes"])

    def test_pending(self):
        self.assertEqual(4, len(Chore.objects.pending()))

    def test_done(self):
        self.assertEqual(3, len(Chore.objects.done()))

    def test_upcoming(self):
        self.assertEqual(6, len(Chore.objects.upcoming()))

    def test_past(self):
        self.assertEqual(1, len(Chore.objects.past()))

```

4. Finally, add a couple of tests for the `status` method (alternatively, we could cover this in a single test method with more than one assertion, but for more complicated model methods you might separate this out):

```python
    def test_status_completed(self):
        self.assertEqual("Completed", self.factories.ac3.status())

    def test_status_pending(self):
        self.assertEqual("Pending", self.factories.mc1.status())

```

And that's it! Make sure all your tests are passing and that all of your business logic is accounted for.

# Part 2 - View Tests

Now, we'll write some tests for our views. First, within our `chores/tests/` directory, add a subdirectory named `test_views`. Here, first add a `__init__.py` file, and then add our three view test files: `test_chore_views.py`, `test_child_views.py`, and `test_task_views.py`.

1. We will start with the Chore view tests. Start by importing the following code at the top of `test_chore_views.py`:

```python
    from django.test import RequestFactory
    from django.urls import reverse
    from django.utils import timezone

    from chores.models import *
    from chores.forms import *
    from chores.views import *
    from chores.tests.utilities import *

```

2. Add a test class and our initial setup method:

```python
    class ChoreViewTests(FactoryTestCase):
    
        def setUp(self):
            self.factories.populate_chores()
```

3. Let's first test that our list view is working as expected, with the correct information set in the variables we pass to our templates. Add the following code to the test class:

```python
    def test_list_view_with_no_chores(self):
        Chore.objects.all().delete()

        response = self.client.get(reverse('chores:chore_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No chores are available.")
        self.assertQuerysetEqual(response.context['chores'], [])

    # Not really necessary since we are partially testing chronological here, but just to be safe
    def test_list_view_with_chores(self):
        response = self.client.get(reverse('chores:chore_list'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(list(response.context['chores']), 
            [repr(self.factories.ac3),repr(self.factories.mc3),repr(self.factories.ac4),repr(self.factories.mc1),repr(self.factories.ac1),repr(self.factories.ac2),repr(self.factories.mc2)])
```

4. We want to make sure our form for chores is rendering correctly. Add the following code to the test class:

```python
    def test_new_chore_view(self):
        response = self.client.get(reverse('chores:chore_new'))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], ChoreForm)
        self.assertContains(response, "Create Chore")
```

5. We also want to test that when a valid chore is created, it is saved in the database and increments our total chores by one. Similarly, if we attempt to create an invalid chore, it is not saved to the database and the object count remains the same:

```python
    def test_create_chore_view(self):
        num_chores = Chore.objects.count()
        response = self.client.post(reverse('chores:chore_new'),
            {'child': self.factories.alex.id, 'task': self.factories.shovel.id, 'due_on': timezone.now().date() + timezone.timedelta(days=3), 'completed': False}) 
        self.assertEqual(Chore.objects.count(), num_chores + 1)
        self.assertRedirects(response, reverse('chores:chore_detail', args=(num_chores+1,)))

    def test_create_bad_chore_view(self):
        num_chores = Chore.objects.count()
        response = self.client.post(reverse('chores:chore_new'),
            {'child': self.factories.alex.id, 'task': 500, 'due_on': timezone.now() + timezone.timedelta(days=3), 'completed': False}) 
        self.assertEqual(Chore.objects.count(), num_chores)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], ChoreForm)
```

6. Add the following code to test that our edit form is rendered correctly:

```python
    def test_edit_chore_view(self):
        response = self.client.get(reverse('chores:chore_edit', args=(self.factories.ac1.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], ChoreForm)
        self.assertContains(response, "Update Chore")
```

7. Add the following code to test that updating an object with valid values sees those changes are made in the database, and otherwise the object remains unchanged:

```python
    def test_update_chore_view(self):
        response = self.client.post(reverse('chores:chore_edit', args=(self.factories.ac1.id,)),
            {'child': self.factories.alex.id, 'task': self.factories.dishes.id, 'due_on': timezone.now().date() + timezone.timedelta(days=3), 'completed': False})
        self.factories.ac1.refresh_from_db()
        self.assertEqual(self.factories.ac1.due_on, timezone.now().date() + timezone.timedelta(days=3))
        self.assertRedirects(response, reverse('chores:chore_detail', args=(self.factories.ac1.id,)))

    def test_update_bad_chore_view(self):
        response = self.client.post(reverse('chores:chore_edit', args=(self.factories.ac1.id,)),
            {'child': self.factories.alex.id, 'task': 500, 'due_on': timezone.now() + timezone.timedelta(days=3), 'completed': False})
        self.factories.ac1.refresh_from_db()
        self.assertEqual(self.factories.ac1.due_on, timezone.now().date() + timezone.timedelta(days=1))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], ChoreForm)
```

8. Finally, test that deleting a chore works as expected and our total chore count is decremented by one after deleting it in the database:

```python
    def test_delete_chore_view(self):
        num_chores = Chore.objects.count()
        response = self.client.post(reverse('chores:chore_delete', args=(self.factories.ac1.id,)))
        self.assertEqual(Chore.objects.count(), num_chores - 1)
        self.assertRedirects(response, reverse('chores:chore_list'))
```

And that's it for testing Chore views! This can get pretty repetitive, so we'll leave testing the Child and Task views up to you as an additional exercise. 

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

