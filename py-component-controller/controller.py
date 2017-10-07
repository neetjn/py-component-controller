import time
import os
import uuid
import logging as logger
from types import MethodType

from selenium.common.exceptions import NoSuchElementException, \
    WebDriverException
from pyseleniumjs import E2EJS


class Controller(object):

    def __init__(self, webdriver, base_url, components, **env):
        """
        :Description: Controller for managing components.
        :param webdriver: Webdriver for controller and components to reference.
        :type webdriver: WebDriver
        :param base_url: Base url for navigations, will navigate to this url in init.
        :type base_url: basestring
        :param components: Component objects to instantiate.
        :type components: tuple, list, dict
        :param env: Key value pairs to pass to instantiated components.
        :type env: **kwargs => dict
        """
        self.webdriver = self.__patch_webdriver(webdriver)
        self.js = E2EJS(webdriver)
        self.base_url = base_url
        if base_url:
            self.webdriver.get(base_url)
        self.logger = logger
        if not isinstance(components, (tuple, list, dict)):
            raise TypeError('Components must be either a tuple, list, or dictionary')
        if isinstance(components, dict):
            self.components = lambda: None
            for name, component in components.iteritems():
                setattr(self.components, name, component(webdriver, env))
        else:
            self.components = [component(webdriver, env) for component in components]

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
            # make copy of function
            find_elements_by_css_selector = webdriver.find_elements_by_css_selector
            webdriver.find_elements_by_css_selector = MethodType(
                lambda self, css_selector: _safari_patch(
                    executor=find_elements_by_css_selector,
                    selector=css_selector
                ), webdriver)
            # make copy of function
            find_elements_by_tag_name = webdriver.find_elements_by_tag_name
            webdriver.find_elements_by_tag_name = MethodType(
                lambda self, name: _safari_patch(
                    executor=find_elements_by_tag_name,
                    selector=name
                ), webdriver)
            # make copy of function
            find_elements_by_id = webdriver.find_elements_by_id
            webdriver.find_elements_by_id = MethodType(
                lambda self, id: _safari_patch(
                    executor=find_elements_by_id,
                    selector=id
                ), webdriver)
            # make copy of function
            find_elements_by_class_name = webdriver.find_elements_by_class_name
            webdriver.find_elements_by_class_name = MethodType(
                lambda self, name: _safari_patch(
                    executor=find_elements_by_class_name,
                    selector=name
                ), webdriver)
            # make copy of function
            find_elements_by_xpath = webdriver.find_elements_by_xpath
            webdriver.find_elements_by_xpath = MethodType(
                lambda self, xpath: _safari_patch(
                    executor=find_elements_by_xpath,
                    selector=xpath
                ), webdriver)
            # make copy of function
            find_elements_by_name = webdriver.find_elements_by_name
            webdriver.find_elements_by_name = MethodType(
                lambda self, name: _safari_patch(
                    executor=find_elements_by_name,
                    selector=name
                ), webdriver)
            # make copy of function
            find_elements_by_link_text = webdriver.find_elements_by_link_text
            webdriver.find_elements_by_link_text = MethodType(
                lambda self, text: _safari_patch(
                    executor=find_elements_by_link_text,
                    selector=text
                ), webdriver)
            # make copy of function
            find_elements_by_partial_link_text = webdriver.find_elements_by_partial_link_text
            webdriver.find_elements_by_partial_link_text = MethodType(
                lambda self, text: _safari_patch(
                    executor=find_elements_by_partial_link_text,
                    selector=text
                ), webdriver)

        return webdriver

    @property
    def location(self):
        """
        :Description: Fetch the current url of controller's webdriver instance.
        :return: basestring
        """
        return self.webdriver.current_url

    @property
    def title(self):
        """
        :Description: Fetch the title of the controller's webdriver instance.
        :return: basestring
        """
        return self.webdriver.title

    def refresh(self):
        """
        :Description: Refreshes primary window.
        """
        self.webdriver.switch_to_default_content()  # necessary for safari
        self.webdriver.refresh()

    def navigate(self, route):
        """
        :Description: Navigate to a route using your defined base url.
        :param route: Route to navigate to using defined base url.
        :type route: basestring
        """
        self.webdriver.get('{location}/{route}'.format(
            location = self.base_url,
            route=route
        ))

    def window_by_title(self, title, graceful=False):
        """
        :Description: Changes to window context by window title.
        :param title: Title of window to switch into.
        :type title: basestring
        :param graceful: Adds leniency to window title search.
        :type graceful: bool
        :return: bool
        """
        for handle in self.webdriver.window_handles:
            self.webdriver.switch_to_window(handle)
            if graceful and title in self.title:
                return True
            if not graceful and self.title == title:
                return True
        return False

    def window_by_location(self, location, graceful=False):
        """
        :Description: Changes to window context by window path.
        :param location: Path of window to switch into.
        :type location: basestring
        :param graceful: Adds leniency to window path search.
        :type graceful: bool
        :return: bool
        """
        for handle in self.webdriver.window_handles:
            self.webdriver.switch_to_window(handle)
            if graceful and location in self.location:
                return True
            if not graceful and self.location == location:
                return True
        return False

    def wait(self, timeout=0, condition=None, reverse=False, throw_error=False):
        """
        :Description: Assisted delays between browser and main thread.
        :param timeout: Time in seconds to wait.
        :type timeout: int
        :param condition: (lambda|function) If callable, will wait 1 to timeout seconds until condition met.
        :param reverse: Will wait for the condition to evaluate to False instead of True.
        :param throw_error: Will throw error raised by condition at end of timeout.
        :type throw_error: bool
        :return: None or condition()
        """
        if callable(condition):
            if not isinstance(timeout, (int, float)) or timeout <= 0:
                raise ValueError('`timeout` must be an integer or float greater than or equal to 1')
            error = None
            for i in range(timeout):
                try:

                    if reverse:
                        if not condition():
                            return False
                    else:
                        if condition():
                            if i >= timeout/2:
                                self.logger.warning(
                                    'Wait took `%s` seconds, more than half of the expected wait time' % str(i+1))
                            return True

                except Exception as e:

                    if throw_error:
                        error = e

                time.sleep(1)

            if error and throw_error:
                raise error
            return reverse
        else:
            time.sleep(timeout)

    def dump_browser_logs(self, name=None):
        """
        :Description: Dumps browser logs to local directory.
        :Warning: `self.js.console_logger` must be executed to store logs.
        :param name: Name log file dropped to disk, will default to timestamp if not specified.
        :type name: basestring
        """
        try:
            logs = self.js.console_dump()
            timestamp = str(int(time.time()))
            log_name = 'console.%s.json' % (('%s.%s' % (name, timestamp)) if name else timestamp)
            with open('%s' % log_name, 'a') as logfile:
                logfile.write(logs)
        except WebDriverException:
            self.logger.critical('Browser console was not overridden, could not return any logs.')

    def screen_shot(self, prefix=''):
        """
        :Description: Takes a screen shot and saves it specified path.
        :param prefix: Prefix for screenshot.
        :type prefix: basestring
        :return: basestring
        """
        file_location = os.path.join('./', prefix + str(uuid.uuid4()) + '.png')
        self.webdriver.get_screenshot_as_file(filename=file_location)
        return file_location

    def element_exists(self, expression):
        """
        :Description: Verifies the expression
        :param expression: (lambda|function) Expression to check against.
        :return: bool
        """
        if callable(expression):
            try:
                return True if expression() else False
            except NoSuchElementException:
                return False
        return False

    def element_available(self, component, prop, visible=True, error=True, timeout=1, msg=None, reverse=False):
        """
        :Description: Verify component element both exists and is visible.
        :param component: Component reference to target.
        :type component: Component
        :param prop: Property of component to check.
        :type prop: basestring
        :param visible: Check for visibility.
        :type visible: bool
        :param error: Error on failure, else return bool status.
        :type error: bool
        :param timeout: Time in seconds to wait for property.
        :type timeout: int
        :param msg: Message to throw if property validity not met and @error is True.
        :type msg: basestring
        :param reverse: Check for the inavailability of target element.
        :return: bool
        """
        status = self.wait(
            timeout=timeout, reverse=reverse, condition=lambda: self.element_exists(
            expression=lambda: self.js.is_visible(
                element=getattr(component, prop)
            ) if visible else getattr(component, prop)
        ))  # exit on completion
        failed = (reverse and status) or (not reverse and not status)
        if error and failed:
            raise RuntimeError(msg if msg else 'Component property "%s" %s %s' % (
                prop, 'exists' if reverse else 'does not exist', 'or is not visible' \
                    if not reverse and visible else ''
            ))
        else:
            return not failed
