import time
from pyseleniumjs import E2EJS


class Controller(object):

  def __init__(self, webdriver, base_url, components, **env):
    """
    :Description: Controller for managing components.
    :param webdriver: Webdriver for controller and components to refernece.
    """
    self.webdriver = webdriver
    self.js = E2EJS(webdriver)
    self.base_url = base_url
    if not isinstance(components, (tuple, list, dict)):
      raise TypeError('Components must be either a tuple, list, or dictionary')
    if isinstance(components, dict):
      self.components = lambda: None
      for name, component in components.iteritems():
        setattr(self.components, name, component(webdriver, env))
    else:
      self.components = [component(webdriver, env) for component in components]

  @staticmethod
  def __patch_webdriver():


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
    """
    return self.webdriver.title

  def navigate(self, route):
    """
    :Description: Navigate to a
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
