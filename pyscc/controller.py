# Licensed to the Software Freedom Conservancy (SFC) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The SFC licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

import os
import uuid
import logging as logger
import time
from types import MethodType

from pyseleniumjs import E2EJS
from selenium.common.exceptions import NoSuchElementException, \
    WebDriverException
from six import iteritems, string_types

from pyscc.resource import Resource


class Controller(object):
    """
    :Description: Controller for managing components.
    :param browser: Webdriver for controller and components to reference.
    :type browser: webdriver
    :param base_url: Base url for navigations, will navigate to this url in init.
    :type base_url: string
    :param components: Component objects to instantiate.
    :type components: dict
    :param env: Key value pairs to pass to instantiated components.
    :type env: **kwargs => dict
    """
    def __init__(self, browser, base_url, components, **env):
        self.browser = self.__patch_webdriver(browser)
        self.js = E2EJS(browser) #pylint: disable=invalid-name
        self.base_url = base_url
        self.logger = logger
        if not isinstance(components, (tuple, list, dict)):
            raise TypeError('Components must be either a tuple, list, or dictionary')

        self.env = Resource(**env) if env else Resource()

        self.components = Resource(**{
            name: component(controller=self) for name, component in iteritems(components)})

        self.browser.get(self.base_url)

    @staticmethod
    def __patch_webdriver(webdriver):
        """
        :Description: Patches webdriver instance with polyfills for conformity.
        :param webdriver: Webdriver instance to patch.
        :type webdriver: WebDriver
        :return: WebDriver
        """
        if webdriver.capabilities['browserName'] == 'safari':

            def _safari_patch(executor, selector):
                try:
                    return executor(selector)
                except NoSuchElementException:
                    return []

            methods = (
                'css_selector',
                'tag_name',
                'id',
                'xpath',
                'name',
                'link_text',
                'partial_link_text')

            for method in methods:
                complete_method_name = 'find_elements_by_{method}'.format(method=method)
                method = getattr(webdriver, complete_method_name)
                setattr(webdriver, complete_method_name, MethodType(
                    lambda self, selector: _safari_patch(executor=method, selector=selector), #pylint: disable=cell-var-from-loop
                    webdriver))

        return webdriver

    @property
    def location(self):
        """
        :Description: Fetch the current url of controller's webdriver instance.
        :return: string
        """
        return self.browser.current_url

    @property
    def title(self):
        """
        :Description: Fetch the title of the controller's webdriver instance.
        :return: string
        """
        return self.browser.title

    def refresh(self):
        """
        :Description: Refreshes primary window.
        """
        self.browser.switch_to_default_content()  # necessary for safari
        self.browser.refresh()

    def navigate(self, route):
        """
        :Description: Navigate to a route using your defined base url.
        :param route: Route to navigate to using defined base url.
        :type route: string
        """
        self.browser.get('{location}/{route}'.format(
            location=self.base_url,
            route=route
        ))

    def is_location(self, route, timeout=0, strict=False, error=False):
        """
        :Description: Check current webdriver location.
        :param route: Route or list of routes to check against.
        :type route: string, iterable
        :param timeout: Time in seconds to wait for route.
        :type timeout: int
        :param strict: Adds leniency to route comparison.
        :type strict: bool
        :param error: Error upon failure.
        :type error: bool, string
        """
        def check_location():
            if hasattr(route, '__iter__') and not isinstance(route, string_types):
                return any(loc == self.location if strict \
                    else loc in self.location for loc in route)
            return route == self.location if strict else route in self.location
        if timeout:
            if error and not self.wait(timeout=timeout, condition=check_location):
                raise RuntimeError(
                    error if isinstance(error, string_types) else 'Location was not matched')
            return self.wait(timeout=timeout, condition=check_location)
        else:
            if error and not check_location():
                raise RuntimeError(
                    error if isinstance(error, string_types) else 'Location was not matched')
            return check_location()

    def window_by_title(self, title, graceful=False):
        """
        :Description: Changes to window context by window title.
        :param title: Title of window to switch into.
        :type title: string
        :param graceful: Adds leniency to window title search.
        :type graceful: bool
        :return: bool
        """
        for handle in self.browser.window_handles:
            self.browser.switch_to_window(handle)
            if graceful and title in self.title:
                return True
            if not graceful and self.title == title:
                return True
        return False

    def window_by_location(self, location, graceful=False):
        """
        :Description: Changes to window context by window path.
        :param location: Path of window to switch into.
        :type location: string
        :param graceful: Adds leniency to window path search.
        :type graceful: bool
        :return: bool
        """
        for handle in self.browser.window_handles:
            self.browser.switch_to_window(handle)
            if graceful and location in self.location:
                return True
            if not graceful and self.location == location:
                return True
        return False

    @classmethod
    def wait(cls, timeout=1, condition=None, reverse=False, throw_error=False):
        """
        :Description: Assisted delays between browser and main thread.
        :param timeout: Time in seconds to wait.
        :type timeout: int
        :param condition: (callable) Wait 1 to timeout seconds until condition met.
        :param reverse: Will wait for the condition to evaluate to False instead of True.
        :param throw_error: Will throw error raised by condition at end of timeout.
        :type throw_error: bool
        :return: bool
        """
        if callable(condition):
            if not isinstance(timeout, int) or timeout < 1:
                raise ValueError('Timeout must be an integer or float greater than or equal to 1')
            error = None
            for _ in range(timeout):
                try:
                    if reverse:
                        if not condition():
                            return False
                    else:
                        if condition():
                            return True
                except Exception as exc: #pylint: disable=broad-except
                    if throw_error:
                        error = exc
                time.sleep(1)
            if error and throw_error:
                raise error #pylint: disable=raising-bad-type
            return reverse
        else:
            time.sleep(timeout)
            return True

    def dump_browser_logs(self, name=None):
        """
        :Description: Dumps browser logs to local directory.
        :Warning: `self.js.console_logger` must be executed to store logs.
        :param name: Name log file dropped to disk, will default to timestamp if not specified.
        :type name: string
        """
        try:
            logs = self.js.console_dump()
            timestamp = str(int(time.time()))
            log_name = 'console.%s.json' % (('%s.%s' % (name, timestamp)) if name else timestamp)
            with open('%s' % log_name, 'a') as logfile:
                logfile.write(logs)
        except WebDriverException:
            self.logger.critical('Browser console was not overridden, could not return any logs.')

    def screen_shot(self, prefix=None):
        """
        :Description: Takes a screen shot and saves it specified path.
        :param prefix: Prefix for screenshot.
        :type prefix: string
        :return: string
        """
        file_location = os.path.join(
            './', (prefix + '_' if prefix else '') + str(uuid.uuid4()) + '.png')
        self.browser.get_screenshot_as_file(filename=file_location)
        return file_location

    def exit(self, safe_exit=False):
        """
        :Description: Safely exit instance of webdriver.
        :param safe_exit: Disable any possible alert or confirmation popup windows.
        :type safe_exit: bool
        """
        if safe_exit:
            self.browser.execute_script('delete window.alert; delete window.confirm')
        try:
            self.browser.stop_client()
        except (WebDriverException, AttributeError):
            self.logger.warning('Could not close remote driver')
        finally:
            self.browser.quit()
