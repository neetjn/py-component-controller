import os
from tests.utils import BaseTest, HomePage


class TestController(BaseTest):

    def test_controller_screenshot(self):
        """test controller screenshot"""
        file_name = self.app.screen_shot(prefix='test')
        self.assertTrue(os.stat(file_name))

    def test_controller_wait(self):
        """"test controller conditional wait"""
        self.app.delete_tasks(tasks=1)
        home = self.app.components.home
        self.assertFalse(self.app.wait(
            timeout=5, condition=lambda: home.tasks.count() == 3, reverse=True))
        self.assertTrue(self.app.wait(
            timeout=5, condition=lambda: home.tasks.count() == 1))

    def test_controller_navigate(self):
        """test controller navigation"""
        self.app.navigate('!#/about')
        self.assertEqual(self.app.location, self.app_url + '/!#/about')

    def test_controller_env(self):
        """test controller env resource is properly created"""
        self.assertTrue(hasattr(self.app, 'env'))
        self.assertEqual(self.app.env.created, self.created)

    def test_controller_component_mapping(self):
        """test controller components are instantiated as expected"""
        self.assertTrue(hasattr(self.app, 'components'))
        self.assertTrue(hasattr(self.app.components, 'home'))
        self.assertIsInstance(self.app.components.home, HomePage)

    def test_controller_window_by_title(self):
        """test controller switch window by title"""
        pass
