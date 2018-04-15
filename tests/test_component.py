from tests.utils import BaseTest

from selenium import webdriver


class TestComponent(BaseTest):

    def test_component_webdriver(self):
        """test component has reference to webdriver"""
        self.assertTrue(hasattr(self.app.components.home, 'browser'))
        self.assertIsInstance(self.app.components.home.browser, webdriver.Chrome)
        self.assertEqual(self.app.components.home.browser, self.app.browser)

    def test_component_env(self):
        """test component has reference to env"""
        self.assertTrue(hasattr(self.app.components.home, 'env'))
        self.assertEqual(self.app.components.home.env, self.app.env)
        self.assertEqual(self.app.components.home.env.created, self.created)

    def test_component_root_selector(self):
        """test component root selector applies to element, elements, and group"""
        home = self.app.components.home
        self.assertTrue(home.logo.selector.startswith('body '))
        self.assertTrue(home.task_group.desc.selector.startswith('body '))
        self.assertTrue(home.task_assignees.selector.startswith('body '))

    def test_component_description(self):
        """test component description works as intended"""
        description = self.app.components.home.__describe__
        self.assertListEqual(description['element'], [
            'create_task_assignee', 'create_task_assignee_label', 'create_task_content',
            'create_task_title', 'delete_tasks_button', 'logo', 'task'])
        self.assertListEqual(description['elements'], ['task_assignees', 'tasks'])
        self.assertListEqual(description['group'], ['task_form', 'task_group'])
