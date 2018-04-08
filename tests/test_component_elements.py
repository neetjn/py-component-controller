import datetime
from uuid import uuid4

from pyscc.element import Element, Elements
from pyscc.resource import Resource
from tests.utils import BaseTest
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException, ElementNotVisibleException, \
    InvalidElementStateException


class TestElement(BaseTest):

    def setUp(self):
        super(TestElement, self).setUp()
        self.social_buttons = self.app.components.header.social_buttons
        self.logo = self.app.components.header.riot_logo
        self.create_task_assignee_label = self.app.components.home.create_task_assignee_label
        self.create_task_assignee = self.app.components.home.create_task_assignee
        self.task = self.app.components.home.task
        self.task_group = self.app.components.home.task_group
        self.tasks = self.app.components.home.tasks
        self.task_form = self.app.components.home.task_form
        self.delete_tasks = self.app.components.home.delete_tasks_button
        self.author = self.app.components.footer.author

    def test_element_group(self):
        """test element groups are generated as intended"""
        self.assertIsInstance(self.social_buttons, Resource)
        expected_attributes = ('twitter', 'github', 'linkedin')
        self.assertTrue(all(item in expected_attributes for item in self.social_buttons.__group__))
        for sb in expected_attributes:
            self.assertTrue(hasattr(self.social_buttons, sb))
            self.assertIsInstance(getattr(self.social_buttons, sb), Element)
        self.assertEqual(self.social_buttons.find('twitter'), self.social_buttons.twitter)

    def test_element_group_checks(self):
        """test element group checks work as intended"""
        self.assertTrue(self.social_buttons.check.available())
        self.assertFalse(self.social_buttons.check.not_available())
        self.assertTrue(self.social_buttons.check.visible())
        self.assertFalse(self.social_buttons.check.invisible())

    def test_element_group_fmt(self):
        """test element groups format selectors as intended"""
        self.assertEqual(self.task_form.fmt(form='create-todo'), self.task_form)
        self.assertEqual(self.task_form.assignee.selector, 'body create-todo #taskAssignee')
        self.task_form.title.fmt(class_name='u-full-width')
        self.assertEqual(self.task_form.title.selector, 'body create-todo #taskTitle.u-full-width')

    def test_element_group_root(self):
        """test element group root element"""
        self.assertTrue('_' not in self.task_group.__group__)  # gh issue 54
        task = self.task_group.fmt(id='1')
        self.assertEqual(task.desc.selector, 'body todo-task#task-1 h4')

    def test_element_wrapper(self):
        """test element wrapper instantiated as intended"""
        self.assertIsInstance(self.logo, Element)
        self.assertTrue(hasattr(self.logo, 'controller'))
        self.assertTrue(hasattr(self.logo, 'selector'))
        self.assertTrue(hasattr(self.logo, 'check'))
        self.assertEqual(self.app, self.logo.controller)

    def test_element_wrapper_fmt(self):
        """test element wrapper selector formatting"""
        with self.task.fmt(id=1) as task:
            self.app.wait(timeout=5, condition=task.get)
            self.assertIsInstance(task.get(), WebElement)
            self.assertEqual(task.fmt(id=str(uuid4())).get(), None)

    def test_element_wrapper_wait(self):
        """test element wrapper wait"""
        self.assertEqual(self.logo.wait_for(timeout=1), self.logo)
        self.assertEqual(self.task.wait_for(timeout=1), None)
        with self.assertRaises(NoSuchElementException):
            self.task.wait_for(timeout=1, error=True)
        task = self.task.fmt(id=2)
        self.delete_tasks.click()
        self.assertEqual(task.wait_for(timeout=5, available=False), task)
        self.assertEqual(task.wait_for(timeout=5, available=True), None)

    def test_element_wrapper_wait_visibility(self):
        """test element wrapper visibility wait"""
        self.assertEqual(self.logo.wait_visible(timeout=1), self.logo)
        self.assertEqual(self.logo.wait_invisible(timeout=5), self.logo)
        with self.assertRaises(ElementNotVisibleException):
            self.logo.wait_visible(timeout=1, error=True)

    def test_element_wrapper_wait_enabled_disabled(self):
        """test element wrapper enabled wait"""
        self.assertEqual(self.delete_tasks.wait_enabled(1), self.delete_tasks)
        self.assertEqual(self.delete_tasks.wait_disabled(1), None)
        with self.assertRaises(InvalidElementStateException):
            self.delete_tasks.wait_disabled(1, error=True)
        self.delete_tasks.get().click()
        self.assertEqual(self.delete_tasks.wait_disabled(5), self.delete_tasks)
        self.assertEqual(self.delete_tasks.wait_enabled(1), None)
        with self.assertRaises(InvalidElementStateException):
            self.delete_tasks.wait_enabled(1, error=True)

    def test_element_wrapper_js_wait(self):
        """test element wrapper javascript wait"""
        self.task.fmt(id=2)
        self.assertEqual(
            self.delete_tasks.wait_js(
                '$el.getAttribute("class").indexOf("is-danger") == -1', 50), self.delete_tasks)
        self.assertFalse(self.delete_tasks.check.wait_status())
        self.task.get().click()
        self.assertTrue(self.app.wait(timeout=5, condition=self.delete_tasks.check.wait_status))

    def test_element_wrapper_attribute(self):
        """test element wrapper get set attribute"""
        self.assertEqual(self.logo.set_attribute(attribute='some', value='value'), self.logo)
        self.assertEqual(self.logo.get_attribute(attribute='some'), 'value')

    def test_element_wrapper_property(self):
        """test element wrapper get set property"""
        self.assertEqual(self.logo.set_property(prop='some', value='value'), self.logo)
        self.assertEqual(self.logo.get_property(prop='some'), 'value')

    def test_element_wrapper_send_input_get_value(self):
        """test element wrapper send input and get value"""
        random_str = str(uuid4())
        self.assertEqual(self.create_task_assignee.send_input(random_str),
                         self.create_task_assignee)
        self.assertEqual(self.create_task_assignee.value(), random_str)
        self.create_task_assignee.send_input(random_str, clear=False)
        self.assertEqual(self.create_task_assignee.value(), random_str + random_str)
        self.create_task_assignee.send_input(random_str)
        self.assertEqual(self.create_task_assignee.value(), random_str)

    def test_element_wrapper_get_text(self):
        """test element wrapper get text"""
        self.assertEqual(self.create_task_assignee_label.text(), 'Assignee')
        self.assertEqual(
            self.delete_tasks.text(raw=True), ' <i class=\"ico ico-left fi-trash\"></i> Delete Completed ')

    def test_element_wrapper_trigger_event(self):
        """test element wrapper trigger event"""
        self.delete_tasks.trigger_event('click', 'MouseEvent', {'bubbles': True})
        self.task.fmt(id=2)
        self.assertTrue(self.app.wait(timeout=5, condition=self.task.check.not_available))

    def test_element_wrapper_scroll_to(self):
        """test element wrapper scroll to"""
        original_offsets = self.app.js.get_scrolling_offsets
        self.assertEqual(self.author.scroll_to(), self.author)
        self.assertTrue(self.app.js.get_scrolling_offsets['y'] > original_offsets['y'])

    def test_element_wrapper_check(self):
        """verify element wrapper check module"""
        self.assertTrue(self.logo.check.available())
        self.assertTrue(self.logo.check.visible())
        self.assertTrue(self.app.wait(timeout=5, condition=self.logo.check.invisible))
        self.assertTrue(self.delete_tasks.check.enabled())
        self.assertFalse(self.delete_tasks.check.disabled())
        self.app.services.tasks.delete_tasks(tasks=2)
        self.assertTrue(self.app.wait(timeout=5, condition=self.task.fmt(id=2).check.not_available))
        self.assertFalse(self.delete_tasks.check.enabled())
        self.assertTrue(self.delete_tasks.check.disabled())

    def test_elements_wrapper(self):
        """test elements wrapper instantiated as intended"""
        self.assertIsInstance(self.tasks, Elements)
        self.assertTrue(hasattr(self.tasks, 'controller'))
        self.assertTrue(hasattr(self.tasks, 'selector'))
        self.assertTrue(hasattr(self.tasks, 'checks'))
        self.assertEqual(self.app, self.tasks.controller)

    def test_elements_wrapper_wait_for(self):
        """test elements wrapper wait for"""
        self.assertEqual(self.tasks.wait_for(timeout=5, length=3), self.tasks)
        self.assertEqual(self.tasks.wait_for(timeout=1, length=4), None)
        with self.assertRaises(NoSuchElementException) as err:
            self.tasks.wait_for(timeout=1, length=4, error=True)
        self.assertIn('"4"', str(err.exception))
        self.assertIn('"3"', str(err.exception))
        with self.assertRaises(NoSuchElementException) as err:
            self.tasks.wait_for(timeout=1, length=4, error="f: ${found}, e: ${expected}")
        self.assertIn('f: 3, e: 4', str(err.exception))

    def test_elements_wrapper_wait_visible(self):
        """test elements wrapper wait visible"""
        start = datetime.datetime.now()
        self.assertEqual(self.tasks.wait_visible(timeout=5, length=3), self.tasks)
        # time delta, check should have passed so it should not have taken 5 seconds
        self.assertTrue(datetime.datetime.now() - start < datetime.timedelta(seconds=5))
        start = datetime.datetime.now()
        self.assertEqual(self.tasks.wait_invisible(timeout=5, length=3), self.tasks)
        # time delta, check should have failed so it should have taken 5 seconds
        self.assertTrue(datetime.datetime.now() - start >= datetime.timedelta(seconds=5))
        with self.assertRaises(ElementNotVisibleException):
            self.tasks.wait_visible(timeout=1, length=4, error=True)
        with self.assertRaises(InvalidElementStateException):
            self.tasks.wait_invisible(timeout=1, length=4, error=True)

    def test_elements_wrapper_text(self):
        """test elements wrapper text aggregation"""
        self.app.wait(timeout=1)  # wait for transitions
        self.assertEqual(len(self.tasks.text()), 3)
        for task in self.tasks.text():
            self.assertIn('2017', task)
        for task in self.tasks.text(raw=True):
            self.assertIn('href="/#!/profile', task)

    def test_elements_wrapper_attributes(self):
        """test elements wrapper attribute aggregation and specification"""
        self.app.wait(timeout=1)  # wait for transitions
        self.assertEqual(self.tasks.count(), 3)
        self.assertEqual(self.tasks.set_attribute('foobar', 'barfoo'), self.tasks)
        attributes = self.tasks.get_attribute('foobar')
        self.assertEqual(len(attributes), 3)
        for attr in attributes:
            self.assertEqual(attr, 'barfoo')

    def test_elements_wrapper_properties(self):
        """test elements wrapper property aggregation and specification"""
        self.app.wait(timeout=1)  # wait for transitions
        self.assertEqual(self.tasks.count(), 3)
        self.assertEqual(self.tasks.set_property('foobar', 'barfoo'), self.tasks)
        properties = self.tasks.get_property('foobar')
        self.assertEqual(len(properties), 3)
        for prop in properties:
            self.assertEqual(prop, 'barfoo')
