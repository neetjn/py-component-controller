from time import time
from unittest import TestCase

from pyscc import Component, Controller, ControllerSpec, Service, \
    component_element, component_elements, component_group
from selenium import webdriver


class Header(Component):

    @component_element
    def riot_logo(self):
        return '#riot'

    @component_group
    def social_buttons(self):
        return {
            'twitter': 'a[title="twitter"]',
            'linkedin': 'a[title="linkedin"]',
            'github': 'a[title="github"]'
        }


class HomePage(Component):

    _ = 'body'

    @component_element
    def logo(self):
        return 'header-partial h1.logo'

    @component_element
    def task(self):
        return 'todo-task#task-${id}'

    @component_group
    def task_group(self):
        return {
            '_': 'todo-task#task-${id}',
            'desc': 'h4',
            'assignee': 'span:nth-child(2)',
            'created': 'span:nth-child(4)'
        }

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
    def create_task_assignee_label(self):
        return 'label[for="taskAssignee"]'

    @component_element
    def create_task_assignee(self):
        return '#taskAssignee'

    @component_element
    def create_task_title(self):
        return '#taskTitle'

    @component_element
    def create_task_content(self):
        return '#taskContent'

    @component_group
    def task_form(self):
        return {
            'assignee': '${form} #taskAssignee',
            'title': '${form} #taskTitle.${class_name}',
            'content': '${form} #taskContent'
        }


class Footer(Component):

    @component_element
    def author(self):
        return 'a#author'


class TaskService(Service):

    def delete_tasks(self, tasks):
        home = self.components.home
        if isinstance(tasks, (tuple, list)):
            home.tasks.wait_for(
                timeout=5, error='No available tasks to delete')
            for task in tasks:
                task_el = home.task.fmt(id=task)
                if 'disabled' not in task_el.get_attribute('class'):
                    task_el.get().click()
        elif isinstance(tasks, int):
            task_el = home.task.fmt(id=tasks).wait_for(timeout=5, error=True)
            task_class = task_el.get_attribute('class')
            if not task_class or 'disabled' not in task_class:
                task_el.get().click()
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


class AppController(ControllerSpec):

    def __init__(self, browser, base_url, **env):
        super(AppController, self).__init__(browser, base_url, {
            'header': Header,
            'footer': Footer,
            'home': HomePage
        }, **env)

    def go_home(self):
        self.components.home.logo.click()


class BaseTest(TestCase):

    def setUp(self):
        self.app_url = 'https://riot-todo-84334.firebaseapp.com/#!/'
        self.created = time()
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-gpu')
        chrome_options.add_argument('--no-sandbox')
        self.app = AppController(
            webdriver.Chrome(chrome_options=chrome_options), self.app_url, created=self.created)

    def tearDown(self):
        self.app.exit()
