# py-page-controller

PCC is an opinionated framework for structuring selenium test suites. This project depends on the [pyselenium-js](https://github.com/neetjn/pyselenium-js) project.

## About

PCC takes the pain out of redundant tasks, and helps provide an interface to tackeling larger web applications. This project is a wrapper for the official selenium bindings and pyselenium-js, offering a more object orientated approach. PCC also includes polyfills for conforming webdriver behavior -- such as the safari webdriver's handling of multiple element queries.

A component object represents an area in the web application user interface that your test is interacting with. Component objects were created to represent every possible element a controller and/or test would need to reference. Component objects allow us to define an element once, and reference it however many times we need by it's defined property. If any major changes are made to our target interface, we can change the definition of a component's property once and it will work across all of our given controllers and tests. Reference: [Page Object](http://selenium-python.readthedocs.io/page-objects.html)

Controllers were created to utilize our defined component objects and to farm out tedious rudimentary tasks such as navigating and managing our context. Controllers allow us to define our logic in a behavioral manner, outside of our test cases, keeping everything clean, simple, and manageable. Controllers also allow us to reference a browser once and pass it to all of our defined components. Reference: [Page Object Model](http://www.guru99.com/page-object-model-pom-page-factory-in-selenium-ultimate-guide.html)

## Usage

This project was created using Python 2.7, selenium `3.0.0b3`, and pyseleniumjs `1.3.1`. An update for Python 3 will be available with pyseleniumjs version 2, as well as the latest version of selenium.

PCC can be installed using pip like so,

```sh
pip install pcc
```

To define a new component, simply import `Component` from `pcc`.

```python
from pcc import Component


class Home(Component):

  @property
  def articles(self):
    return self.webdriver.find_elements_by_css_selector('div.article')
```

Controllers can be defined using the `Controller` class which can also be imported from ppc.

```python
from pcc import Controller
from project.components import Home


class Product(Controller):

  def __init__(self, webdriver, base_url, **env):
    super(Product, self).__init__(
      webdriver=webdriver,
      base_url=base_url,
      components={
        'home': Home
      },
      env=**env
    )

  def login(self, username, password):
    # do login
    self.loggedIn = True
    ...
```

---
Copyright (c) 2017 John Nolette Licensed under the Apache License, Version 2.0.