from pyscc import Component, Controller, component_element, component_elements
from selenium import webdriver
from unittest import TestCase
from time import time


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

    def __init__(self, webdriver, base_url, **env):
        super(AppController, self).__init__(self, webdriver, base_url, {
            'home': HomePage}, **env)

    def go_home(self):
        self.components.home.logo.click()

    def deleteTask(self, tasks):
        assert isinstance(tasks, (tuple, list)), 'Expected a tuple or list of tasks'
        home = self.components.home
        home.tasks.wait_for(
            timeout=5, length=1, error='No available tasks to delete')
        for task in tasks:
            task_el = home.task.fmt(id=task)
            # TODO: finish controller
            if 'disabled' not in self.js.get_attribute(task_el, 'class'):
                task_el.click()
                assert home.task.fmt(id=task).click(), 'Could not find task {}'.format(task)
        home.delete_tasks_button.click()

    def createTask(self, assignee, title, content):
        home = self.components.home
        home.create_task_assignee.wait_visible(5)
        home.create_task_assignee.get().send_keys(assignee)
        home.create_task_title.get().send_keys(title)
        home.create_task_content.get().send_keys(content)


class BaseTest(TestCase):

    def setUp(self):
        self.app_url = 'http://localhost:3000'
        self.created = time()
        self.app = AppController(
            webdriver.Chrome(), self.app_url, created=self.created)

    def tearDown(self):
        self.app.exit()
