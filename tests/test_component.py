from pyscc.controller import Controller
from tests.utils import BaseTest

from selenium import webdriver


class TestComponent(BaseTest):

    def test_component_controller(self):
        """test component has reference to controller"""
        self.assertTrue(hasattr(self.app.components.home, 'controller'))
        self.assertIsInstance(self.app.components.home.controller, Controller)
        self.assertEqual(self.app, self.app.components.home.controller)

    # def test_component_webdriver(self):
    #     """test component has reference to webdriver"""
    #     self.assertTrue(hasattr(self.app.components.home, 'browser'))
    #     self.assertIsInstance(self.app.components.home.browser, webdriver.Chrome)
    #     self.assertEqual(self.app.components.home.browser, self.app.browser)

    # def test_component_env(self):
    #     """test component has reference to env"""
    #     self.assertTrue(hasattr(self.app.components.home, 'env'))
    #     self.assertEqual(self.app.components.home.env, self.app.env)
    #     self.assertEqual(self.app.components.home.env.created, self.created)
