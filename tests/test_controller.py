import os
from tests.utils import BaseTest, HomePage


class TestController(BaseTest):

    # def test_controller_screenshot(self):
    #     """test controller screenshot"""
    #     file_name = self.app.screen_shot(prefix='test')
    #     self.assertTrue(os.stat(file_name))

    def test_controller_browser_logs(self):
        """test controller browser log dump"""
        self.app.js.console_logger()
        self.app.browser.execute_script('console.log("foobar")')
        log_path = self.app.browser_logs(name='test', path='target/')
        self.assertTrue(os.stat(log_path))

    # def test_controller_wait(self):
    #     """"test controller conditional wait"""
    #     self.app.delete_tasks(tasks=1)
    #     home = self.app.components.home
    #     self.assertFalse(self.app.wait(
    #         timeout=5, condition=lambda: home.tasks.count() == 3, reverse=True))
    #     self.assertTrue(self.app.wait(
    #         timeout=5, condition=lambda: home.tasks.count() == 1))

    # def test_controller_navigate(self):
    #     """test controller navigation"""
    #     self.app.navigate('!#/about')
    #     self.assertEqual(self.app.location, self.app_url + '/!#/about')

    # def test_controller_is_location(self):
    #     """test controller is_location"""
    #     self.app.navigate('!#/about')
    #     self.assertTrue(self.app.is_location('/!#/about'))
    #     self.assertTrue(self.app.is_location(self.app_url + '/!#/about', strict=True))
    #     self.assertFalse(self.app.is_location('/!#/about', strict=True))
    #     self.assertTrue(self.app.is_location('/!#/about', timeout=1))
    #     self.assertTrue(self.app.is_location(self.app_url + '/!#/about', timeout=1, strict=True))
    #     self.assertFalse(self.app.is_location('/!#/about', timeout=1, strict=True))
    #     self.assertTrue(self.app.is_location(['/!#/home', '/!#/about'], timeout=1))
    #     self.assertFalse(self.app.is_location(['/!#/home', '/!#/about'], timeout=1, strict=True))
    #     with self.assertRaises(RuntimeError):
    #         self.app.is_location('/!#/about', strict=True, error=True)
    #     with self.assertRaises(RuntimeError):
    #         self.app.is_location('/!#/about', strict=True, timeout=1, error=True)

    # def test_controller_env(self):
    #     """test controller env resource is properly created"""
    #     self.assertTrue(hasattr(self.app, 'env'))
    #     self.assertEqual(self.app.env.created, self.created)

    # def test_controller_component_mapping(self):
    #     """test controller components are instantiated as expected"""
    #     self.assertTrue(hasattr(self.app, 'components'))
    #     self.assertTrue(hasattr(self.app.components, 'home'))
    #     self.assertIsInstance(self.app.components.home, HomePage)

    # def test_controller_window_detection(self):
    #     """test controller window detection"""
    #     header = self.app.components.header
    #     header.social_buttons.twitter.get().click()
    #     self.assertTrue(
    #         self.app.wait(timeout=5, condition=lambda: self.app.window_by_location(
    #             'https://twitter.com/neet_jn')))
    #     self.assertEqual(self.app.location, 'https://twitter.com/neet_jn')
    #     self.assertTrue(self.app.window_by_title('Home'))
    #     self.assertIn(self.app_url, self.app.location)
