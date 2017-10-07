import time
import os
import logging as logger

from selenium.common.exceptions import NoSuchElementException
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
    :type env: dict
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
        find_elements_by_css_selector = self.webdriver.find_elements_by_css_selector
        self.webdriver.find_elements_by_css_selector = MethodType(
          lambda self, css_selector: _safari_patch(
            executor=find_elements_by_css_selector,
            selector=css_selector
          ), self.webdriver)
        # make copy of function
        find_elements_by_tag_name = self.webdriver.find_elements_by_tag_name  # make copy of function
        self.webdriver.find_elements_by_tag_name = MethodType(
          lambda self, name: _safari_patch(
            executor=find_elements_by_tag_name,
            selector=name
          ), self.webdriver)
        # make copy of function
        find_elements_by_id = self.webdriver.find_elements_by_id  # make copy of function
        self.webdriver.find_elements_by_id = MethodType(
          lambda self, id: _safari_patch(
            executor=find_elements_by_id,
            selector=id
          ), self.webdriver)
        # make copy of function
        find_elements_by_class_name = self.webdriver.find_elements_by_class_name  # make copy of function
        self.webdriver.find_elements_by_class_name = MethodType(
          lambda self, name: _safari_patch(
            executor=find_elements_by_class_name,
            selector=name
          ), self.webdriver)
        # make copy of function
        find_elements_by_xpath = self.webdriver.find_elements_by_xpath  # make copy of function
        self.webdriver.find_elements_by_xpath = MethodType(
          lambda self, xpath: _safari_patch(
            executor=find_elements_by_xpath,
            selector=xpath
          ), self.webdriver)
        # make copy of function
        find_elements_by_name = self.webdriver.find_elements_by_name  # make copy of function
        self.webdriver.find_elements_by_name = MethodType(
          lambda self, name: _safari_patch(
            executor=find_elements_by_name,
            selector=name
          ), self.webdriver)
        # make copy of function
        find_elements_by_link_text = self.webdriver.find_elements_by_link_text  # make copy of function
        self.webdriver.find_elements_by_link_text = MethodType(
          lambda self, text: _safari_patch(
            executor=find_elements_by_link_text,
            selector=text
          ), self.webdriver)
        # make copy of function
        find_elements_by_partial_link_text = self.webdriver.find_elements_by_partial_link_text  # make copy of function
        self.webdriver.find_elements_by_partial_link_text = MethodType(
          lambda self, text: _safari_patch(
            executor=find_elements_by_partial_link_text,
            selector=text
          ), self.webdriver)

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
      log_name = 'console.%s.log' % (('%s.%s' % (name, timestamp)) if name else timestamp)
      if not os.path.exists('artifacts'):
        os.makedirs('artifacts')
        with open('artifacts/%s' % log_name, 'a') as logfile:
          logfile.write(logs)
    except WebDriverException:
      self.logger.critical('Browser console was not overridden, could not return any logs.')

  def window_by_handle(self, window=None):
    """
    :Description: Changes to specified window or most recently opened.
    :param window: (window handle) If specified, browser instance will focus on window handle, else focus on parent window.
    """
    self.browser.switch_to_window(self.windows.parent) \
      if window is None else self.browser.switch_to_window(window)

  def window_by_title(self, title, graceful=False):
    # todo: refactor these to use the window function already included in the controller (self.windows)
    """
    :Description: Changes to window context by window title.
    :param title: Title of window to switch into.
    :type title: basestring
    :param graceful: Adds leniency to window title search.
    :type graceful: bool
    """
    for handle in self.browser.window_handles:
      self.browser.switch_to_window(handle)
      if graceful and title in self.title:
        return True
      if not graceful and self.title == title:
        return True
    return False

  def window_by_location(self, location, graceful=False):
    # todo: refactor these to use the window function already included in the controller (self.windows)
    """
    :Description: Changes to window context by window path.
    :param location: Path of window to switch into.
    :type location: basestring
    :param graceful: Adds leniency to window path search.
    :type graceful: bool
    """
    for handle in self.browser.window_handles:
      self.browser.switch_to_window(handle)
      if graceful and location in self.location:
        return True
      if not graceful and self.location == location:
        return True
    return False

  def wait(self, timeout, condition=None):
