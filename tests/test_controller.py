import random
import os
from tests.utils import BaseTest


class TestController(BaseTest):

    def test_controller_screenshot(self):
        """Ensure screenshot logic works"""
        file_name = self.app.screen_shot(folder=os.path.join(os.getcwd(), "artifacts"))
        self.assertTrue(os.stat(file_name))

    def test_controller_wait(self):
        pass

    def test_controller_navigate():
        pass
