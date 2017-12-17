from pyscc import Component, Controller, component_element, component_elements
from selenium import webdriver
from unittest import TestCase
from time import time


class Header(Component):

    @component_element
    def riot_logo(self):
        return '#riot'

    @component_element
    def twitter_button(self):
        return 'a[title="twitter"]'

    @component_element
    def linkedin_button(self):
        return 'a[title="linked"]'

    @component_element
    def facebook_button(self):
        return 'a[title="facebook"]'


class HomePage(Component):

    @component_element
    def logo(self):
        return 'header-partial h1.logo'

    @component_element
    def task(self):
        return 'todo-task#task-{id}'

    @component_elements
    def tasks(self):
        return 'todo-task'

    @component_elements
    def task_assignees(self):
        return 'todo-task #assignee'

    @component_element
    def delete_tasks_button(self):
        return '#deleteTasks'

    @component_element
    def create_task_assignee(self):
        return '#taskAssignee'

    @component_element
    def create_task_title(self):
        return '#taskTitle'

    @component_element
    def create_task_content(self):
        return '#taskContent'


class AppController(Controller):

    def __init__(self, browser, base_url, **env):
        super(AppController, self).__init__(browser, base_url, {
            'header': Header,
            'home': HomePage
        }, **env)

    def go_home(self):
        self.components.home.logo.click()

    def delete_tasks(self, tasks):
        home = self.components.home
        if isinstance(tasks, (tuple, list)):
            home.tasks.wait_for(
                timeout=5, error='No available tasks to delete')
            for task in tasks:
                task_el = home.task.fmt(id=task)
                if 'disabled' not in task_el.get_attribute('class'):
                    task_el.click()
        elif isinstance(tasks, int):
            task_el = home.task.fmt(id=tasks).wait_for(timeout=5, error=True)
            task_class = task_el.get_attribute('class')
            if not task_class or 'disabled' not in task_class:
                task_el.click()
        else:
            raise RuntimeError('Expected a task or list of tasks')
        home.delete_tasks_button.get().click()

    def create_tasks(self, assignee, title, content):
        home = self.components.home
        home.create_task_assignee.wait_for(5, error=True)\
            .send_input(assignee)
        home.create_task_assignee.send_input(assignee)
        home.create_task_title.send_input(title)
        home.create_task_content.send_input(content)


class BaseTest(TestCase):

    def setUp(self):
        self.app_url = 'http://localhost:3000'
        self.created = time()
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        self.app = AppController(
            webdriver.Chrome(chrome_options=chrome_options), self.app_url, created=self.created)

    def tearDown(self):
        self.app.exit()
