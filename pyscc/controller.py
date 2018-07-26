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

import io
import logging
import os
import time
from string import Template
from types import MethodType

from pyseleniumjs import E2EJS
from selenium.common.exceptions import InvalidSelectorException, \
    NoSuchElementException, WebDriverException
from selenium.webdriver.remote.remote_connection import LOGGER as SeleniumLogger
from six import iteritems, string_types

from pyscc.resource import Resource


class ControllerLogger(logging.Logger):

    def __init__(self, name, level=0):
        self._filters = []
        super(ControllerLogger, self).__init__(name, level)

    def add_filter(self, source):
        self._filters.append(source)

    # pylint: disable=too-many-arguments,len-as-condition, arguments-differ
    def _log(self, level, msg, args, exc_info=None, extra=None):
        if len(self._filters):
            for source in self._filters:
                if not callable(source) and not source():
                    return

        super(ControllerLogger, self)._log(level, msg, args, exc_info, extra)


# pylint: disable=useless-object-inheritance
class Controller(object):

    _FILTER_SELENIUM_LOGS_ = False
    _FILTER_SELENIUM_LOG_STREAM_ = False
    _LOG_TO_FILE_ = False

    def __init__(self, browser, base_url, components, **env):
        """
        Controller for managing components.

        :param browser: Webdriver for controller and components to reference.
        :type browser: webdriver
        :param base_url: Base url for navigations, will navigate to this url in init.
        :type base_url: string
        :param components: Component objects to instantiate.
        :type components: dict
        :param env: Key value pairs to pass to instantiated components.
        :type env: **kwargs => dict
        """
        self.browser = self.__patch_webdriver(browser)
        self.js = E2EJS(browser) # pylint: disable=invalid-name
        self.base_url = base_url

        log_format = '%(asctime)s - %(name)s - %(funcName)s - %(levelname)s - %(message)s'

        if self._FILTER_SELENIUM_LOGS_:
            SeleniumLogger.propagate = False

        if self._FILTER_SELENIUM_LOG_STREAM_:
            for handler in SeleniumLogger.handlers:
                if isinstance(handler, logging.StreamHandler):
                    SeleniumLogger.removeHandler(handler)

        logging.getLogger().setLevel(logging.DEBUG)

        logging.setLoggerClass(ControllerLogger)
        self.logger = logging.getLogger('pyscc')

        if self._LOG_TO_FILE_:
            if not os.path.exists('logs/'):
                os.makedirs('logs/')
            log_time = str(time.time())
            # -- file logging for all logs
            bfh = logging.FileHandler('logs/{}.log'.format(log_time))
            bfh.setFormatter(logging.Formatter(log_format))
            logging.getLogger().addHandler(bfh)
            # -- file logging for pyscc logs
            pfh = logging.FileHandler('logs/{}_controller.log'.format(log_time))
            pfh.setFormatter(logging.Formatter(log_format))
            self.logger.addHandler(pfh)
            # -- file logging for pyscc logs
            sfh = logging.FileHandler('logs/{}_selenium.log'.format(log_time))
            sfh.setFormatter(logging.Formatter(log_format))
            SeleniumLogger.addHandler(sfh)

        if not isinstance(components, (tuple, list, dict)):
            raise TypeError('Components must be either a tuple, list, or dictionary')

        self.env = Resource(**env) if env else Resource()

        self.components = Resource(**{
            name: component(controller=self) for name, component in iteritems(components)})

        self.services = Resource()

        self.browser.get(self.base_url)

    def __enter__(self):
        return self

    def __exit__(self, e_type, value, traceback):
        self.exit()

    @staticmethod
    def __patch_webdriver(webdriver):
        """
        Patches webdriver instance with polyfills for conformity.

        :param webdriver: Webdriver instance to patch.
        :type webdriver: WebDriver
        :return: WebDriver
        """

        def safari_selector_patch(executor, selector):
            try:
                return executor(selector)
            except (NoSuchElementException, InvalidSelectorException):
                return []

        by_css_selector = webdriver.find_elements_by_css_selector
        webdriver.find_elements_by_css_selector = MethodType(lambda self, selector:\
            safari_selector_patch(by_css_selector, selector), webdriver)

        by_xpath = webdriver.find_elements_by_xpath
        webdriver.find_elements_by_xpath = MethodType(lambda self, selector: safari_selector_patch(
            by_xpath, selector), webdriver)

        return webdriver

    def add_service(self, name, prototype):
        """
        Adds new service to controller.

        :param name: Service alias.
        :type name: string
        :param prototype: Service definition to instantiate.
        :type prototype: Service
        """
        setattr(self.services, name, prototype(self))

    @property
    def location(self):
        """
        Fetch the current url of controller's webdriver instance.

        :return: string
        """
        return self.browser.current_url

    @property
    def title(self):
        """
        Fetch the title of the controller's webdriver instance.

        :return: string
        """
        return self.browser.title

    def refresh(self):
        """
        Refreshes primary window.
        """
        self.browser.switch_to_default_content()  # necessary for safari
        self.browser.refresh()

    def navigate(self, route):
        """
        Navigate to a route using your defined base url.

        :param route: Route to navigate to using defined base url.
        :type route: string
        """
        self.browser.get('{location}/{route}'.format(
            location=self.base_url,
            route=route
        ))

    def is_location(self, route, timeout=0, strict=False, error=False):
        """
        Check current webdriver location.

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

        result = self.wait(timeout=timeout, condition=check_location) \
            if timeout else check_location()
        if error and not result:
            if isinstance(error, string_types):
                msg = Template(error).safe_substitute(expected=route, found=self.location)
            else:
                # pylint: disable=line-too-long
                msg = 'Location "{}" was not matched, instead found: "{}"'.format(route, self.location)
            raise RuntimeError(msg)

        return result

    def window_by_title(self, title, timeout=0, strict=False, error=False):
        """
        Changes to window context by window title.

        :param title: Title of window to switch into.
        :type title: string
        :param timeout: Time in seconds to wait for window.
        :type timeout: int
        :param strict: Adds leniency to window title search.
        :type strict: bool
        :param error: Error upon failure.
        :type error: bool, string
        :return: bool
        """
        def search():
            for handle in self.browser.window_handles:
                self.browser.switch_to_window(handle)
                if strict and title == self.title:
                    return True
                if not strict and title in self.title:
                    return True
            return False

        result = self.wait(timeout=timeout, condition=search) if timeout else search()
        if error and not result:
            if isinstance(error, string_types):
                msg = Template(error).safe_substitute(expected=title, found=self.title)
            else:
                msg = 'Window by title "{}" not found, found: {}'.format(title, self.title)
            raise RuntimeError(msg)

        return result

    def window_by_location(self, location, timeout=0, strict=False, error=False):
        """
        Changes to window context by window path.

        :param location: Path of window to switch into.
        :type location: string
        :param timeout: Time in seconds to wait for window.
        :type timeout: int
        :param strict: Adds leniency to window path search.
        :type strict: bool
        :param error: Error upon failure.
        :type error: bool, string
        :return: bool
        """
        def search():
            for handle in self.browser.window_handles:
                self.browser.switch_to_window(handle)
                if strict and location == self.location:
                    return True
                if not strict and location in self.location:
                    return True
            return False

        result = self.wait(timeout=timeout, condition=search) if timeout else search()
        if error and not result:
            if isinstance(error, string_types):
                msg = Template(error).safe_substitute(expected=location, found=self.location)
            else:
                # pylint: disable=line-too-long
                msg = 'Window by location "{}" not found, found: "{}"'.format(location, self.location)
            raise RuntimeError(msg)

        return result

    @classmethod
    def wait(cls, timeout=1, condition=None, reverse=False, throw_error=False):  # pylint: disable=no-else-return
        """
        Assisted delays between browser and main thread.

        :param timeout: Time in seconds to wait.
        :type timeout: int
        :param condition: (callable) Wait 1 to timeout seconds until condition met.
        :param reverse: Will wait for the condition to evaluate to False instead of True.
        :param throw_error: Will throw error raised by condition at end of timeout.
        :type throw_error: bool
        :return: bool
        """
        # pylint: disable=no-else-return
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
                except Exception as exc: # pylint: disable=broad-except
                    if throw_error:
                        error = exc
                time.sleep(1)
            if error and throw_error:
                raise error # pylint: disable=raising-bad-type
            return reverse
        else:
            time.sleep(timeout)
            return True

    def browser_logs(self, name=None, path=None):
        """
        Dumps browser logs to local directory.

        :Warning: `self.js.console_logger` must be executed to store logs.
        :param name: Name log file dropped to disk, will default to timestamp if not specified.
        :type name: string
        :param path: Path to drop console log in.
        :type path: string
        :return: string
        """
        if path and not os.path.exists(path):
            os.mkdir(path)
        try:
            timestamp = str(int(time.time()))
            log_path = '%sconsole.%s.json' % (path, ('%s.%s' % (name, timestamp)) if \
                name else timestamp)
            with io.open(log_path, 'a', encoding='utf-8') as logfile:
                logfile.write(self.js.console_dump())
            return log_path
        except WebDriverException:
            self.logger.critical('Browser logger object not found, could not return any logs.')

    def screen_shot(self, prefix=None, path=None):
        """
        Takes a screen shot and saves it specified path.

        :param prefix: Prefix for screenshot.
        :type prefix: string
        :param path: Path to drop screen shot in.
        :type path: string
        :return: string
        """
        file_location = os.path.join(
            path if path else './', (prefix + '_' if prefix else '') + str(time.time()) + '.png')
        self.browser.get_screenshot_as_file(filename=file_location)
        return file_location

    def exit(self, safe_exit=False):
        """
        Safely exit instance of webdriver.

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
