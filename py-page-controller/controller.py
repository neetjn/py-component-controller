class Controller(object):

  def __init__(self, webdriver, base_url, components, **env):
    self.webdriver = webdriver
    self.base_url = base_url
    if not isinstance(components, (tuple, list, dict)):
      raise TypeError('Components must be either a tuple, list, or dictionary')
    if isinstance(components, dict):
      self.components = lambda: None
      for name, component in components.iteritems():
        setattr(self.components, name, component(webdriver, env))
    else:
      self.components = [component(webdriver, env) for component in components]

  def wait(self, )