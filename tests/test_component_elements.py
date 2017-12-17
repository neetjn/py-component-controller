from pyscc.controller import Controller
from pyscc.element import Element, Elements
from tests.utils import BaseTest
from selenium.webdriver.remote.webelement import WebElement
from uuid import uuid4


class TestElement(BaseTest):

    def setUp(self):
        super(TestElement, self).setUp()
        self.logo = self.app.components.header.riot_logo
        self.task = self.app.components.home.task
        self.tasks = self.app.components.home.tasks

    # def test_element_wrapper(self):
    #     self.assertIsInstance(self.logo, Element)
    #     self.assertTrue(hasattr(self.logo, 'controller'))
    #     self.assertTrue(hasattr(self.logo, 'selector'))
    #     self.assertTrue(hasattr(self.logo, 'check'))
    #     self.assertEqual(self.app, self.logo.controller)

    # def test_element_wrapper_fmt(self):
    #     task = self.task.fmt(id=1)
    #     self.assertIsInstance(task.get(), WebElement)
    #     self.assertEqual(task.fmt(id=str(uuid4())).get(), None)

    def test_element_wrapper_check(self):
        self.assertTrue(self.logo.check.visible())
        self.assertTrue(self.app.wait(timeout=5, condition=self.logo.check.invisible),
            msg='found: {}'.format(self.logo.check.visible()))

    # def test_elements_wrapper(self):
    #     self.assertIsInstance(self.tasks, Elements)
    #     self.assertTrue(hasattr(self.tasks, 'controller'))
    #     self.assertTrue(hasattr(self.tasks, 'selector'))
    #     self.assertTrue(hasattr(self.tasks, 'checks'))
    #     self.assertEqual(self.app, self.tasks.controller)

    # def test_elements_wrapper_checks(self):
    #     pass
