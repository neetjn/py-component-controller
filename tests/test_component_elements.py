from uuid import uuid4

from pyscc.element import Element, Elements
from tests.utils import BaseTest
from selenium.webdriver.remote.webelement import WebElement


class TestElement(BaseTest):

    def setUp(self):
        super(TestElement, self).setUp()
        self.logo = self.app.components.header.riot_logo
        self.task = self.app.components.home.task
        self.tasks = self.app.components.home.tasks

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

    def test_element_wrapper_check(self):
        """verify element wrapper check module"""
        self.assertTrue(self.logo.check.available())
        self.assertTrue(self.logo.check.visible())
        self.assertTrue(self.app.wait(timeout=5, condition=self.logo.check.invisible))
        self.app.delete_tasks(tasks=2)
        self.assertTrue(self.app.wait(timeout=5, condition=self.task.fmt(id=2).check.not_available))

    def test_elements_wrapper(self):
        """test element wrapper instantiated as intended"""
        self.assertIsInstance(self.tasks, Elements)
        self.assertTrue(hasattr(self.tasks, 'controller'))
        self.assertTrue(hasattr(self.tasks, 'selector'))
        self.assertTrue(hasattr(self.tasks, 'checks'))
        self.assertEqual(self.app, self.tasks.controller)

    def test_elements_wrapper_checks(self):
        """verify element wrapper checks module"""
        pass
