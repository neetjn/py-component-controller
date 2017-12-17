from uuid import uuid4

from pyscc.element import Element, Elements
from pyscc.resource import Resource
from tests.utils import BaseTest
from selenium.webdriver.remote.webelement import WebElement


class TestElement(BaseTest):

    def setUp(self):
        super(TestElement, self).setUp()
        self.social_buttons = self.app.components.header.social_buttons
        self.logo = self.app.components.header.riot_logo
        self.create_task_assignee_label = self.app.components.home.create_task_assignee_label
        self.create_task_assignee = self.app.components.home.create_task_assignee
        self.task = self.app.components.home.task
        self.tasks = self.app.components.home.tasks
        self.delete_tasks = self.app.components.home.delete_tasks_button
        self.author = self.app.components.footer.author

    def test_element_group(self):
        """test element groups are generated as intended"""
        self.assertIsInstance(self.social_buttons, Resource)
        for s in ('twitter', 'facebook', 'linkedin'):
            self.assertTrue(hasattr(self.social_buttons, s))
            self.assertIsInstance(getattr(self.social_buttons, s), Element)

    def test_element_wrapper(self):
        """test element wrapper instantiated as intended"""
        self.assertIsInstance(self.logo, Element)
        self.assertTrue(hasattr(self.logo, 'controller'))
        self.assertTrue(hasattr(self.logo, 'selector'))
        self.assertTrue(hasattr(self.logo, 'check'))
        self.assertEqual(self.app, self.logo.controller)

    def test_element_wrapper_fmt(self):
        """test element wrapper selector formatting"""
        task = self.task.fmt(id=1)
        self.app.wait(timeout=5, condition=task.get)
        self.assertIsInstance(task.get(), WebElement)
        self.assertEqual(task.fmt(id=str(uuid4())).get(), None)

    def test_element_wrapper_wait(self):
        """test element wrapper wait"""
        self.assertEqual(self.logo.wait_for(timeout=1), self.logo)
        self.assertEqual(self.task.wait_for(timeout=1), None)

    def test_element_wrapper_wait_visibility(self):
        """test element wrapper visibility wait"""
        self.assertEqual(self.logo.wait_visible(timeout=1), self.logo)
        self.assertEqual(self.logo.wait_invisible(timeout=5), self.logo)

    def test_element_wrapper_js_wait(self):
        """test element wrapper javascript wait"""
        self.task.fmt(id=2)
        self.assertEqual(
            self.delete_tasks.wait_js(
                '$el.getAttribute("class").indexOf("is-danger") == -1', 50), self.delete_tasks)
        self.assertFalse(self.delete_tasks.check.wait_status())
        self.task.click()
        self.assertTrue(self.app.wait(timeout=5, condition=self.delete_tasks.check.wait_status))

    def test_element_wrapper_attribute(self):
        """test element wrapper get set attribute"""
        self.assertEqual(self.logo.set_attribute(attribute='some', value='value'), self.logo)
        self.assertEqual(self.logo.get_attribute(attribute='some'), 'value')

    def test_element_wrapper_property(self):
        """test element wrapper get set property"""
        self.assertEqual(self.logo.set_property(prop='some', value='value'), self.logo)
        self.assertEqual(self.logo.get_property(prop='some'), 'value')

    def test_element_wraooer_send_input_get_value(self):
        """test element wrapper send input and get value"""
        random_str = str(uuid4())
        self.assertEqual(self.create_task_assignee.send_input(random_str), self.create_task_assignee)
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
        self.app.delete_tasks(tasks=2)
        self.assertTrue(self.app.wait(timeout=5, condition=self.task.fmt(id=2).check.not_available))

    def test_elements_wrapper(self):
        """test elements wrapper instantiated as intended"""
        self.assertIsInstance(self.tasks, Elements)
        self.assertTrue(hasattr(self.tasks, 'controller'))
        self.assertTrue(hasattr(self.tasks, 'selector'))
        self.assertTrue(hasattr(self.tasks, 'checks'))
        self.assertEqual(self.app, self.tasks.controller)

    def test_elements_wrapper_checks(self):
        """verify elements wrapper checks module"""
        pass
