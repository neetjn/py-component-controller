class Component(object):

  def __init__(self, webdriver, env):
    """
    :Description: Base for web components.
    :param webdriver: Webdriver instance to reference.
    :type webdriver: WebDriver
    :param env: Additional variables to be used in properties.
    :type env: dict
    """
    self.webdriver = webdriver
    self.env = env