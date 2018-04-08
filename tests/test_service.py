from pyscc.controller import Controller
from tests.utils import BaseTest

from selenium import webdriver


class TestService(BaseTest):

    def setUp(self):
        super(TestService, self).__init__()
        self.tasks_service = self.app.services.tasks

    def test_service_webdriver(self):
        """test service has reference to webdriver"""
        self.assertTrue(hasattr(self.tasks_service, 'browser'))
        self.assertIsInstance(self.tasks_service.browser, webdriver.Chrome)
        self.assertEqual(self.tasks_service.browser, self.app.browser)

    def test_service_components(self):
        """test service has reference to components"""
        self.assertTrue(hasattr(self.tasks_service, 'browser'))
        self.assertEqual(self.task_service.components, self.app.components)

    def test_service_env(self):
        """test service has reference to env"""
        self.assertTrue(hasattr(self.tasks_service, 'env'))
        self.assertEqual(self.tasks_service.env, self.app.env)
        self.assertEqual(self.tasks_service.env.created, self.created)
