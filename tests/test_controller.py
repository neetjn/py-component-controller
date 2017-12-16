import os
from tests.utils import BaseTest


class TestController(BaseTest):

    def test_controller_screenshot(self):
        """test controller screenshot"""
        file_name = self.app.screen_shot(prefix='test')
        self.assertTrue(os.stat(file_name))

    def test_controller_wait(self):
        """"test controller conditional wait"""
        self.app.delete_tasks(tasks=[1])

    def test_controller_navigate(self):
        pass
