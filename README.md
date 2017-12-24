# py-component-controller

[![build](https://travis-ci.org/neetjn/py-component-controller.svg?branch=master)](https://travis-ci.org/neetjn/py-component-controller)
[![Documentation Status](https://readthedocs.org/projects/py-component-controller/badge/?version=latest)](http://py-component-controller.readthedocs.io/en/latest/?badge=latest)
[![PyPI version](https://badge.fury.io/py/pyscc.svg)](https://badge.fury.io/py/pyscc)
[![codecov](https://codecov.io/gh/neetjn/py-component-controller/branch/master/graph/badge.svg)](https://codecov.io/gh/neetjn/py-component-controller)
[![Join the chat at https://gitter.im/py-component-controller/Lobby](https://badges.gitter.im/py-component-controller/Lobby.svg)](https://gitter.im/py-component-controller/Lobby?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

**py-component-controller** is an opinionated framework for structuring selenium test suites.

This project depends on the [pyselenium-js](https://github.com/neetjn/pyselenium-js) project.

Official documentation be be read [here](http://py-component-controller.readthedocs.io/en/latest/).

## About

What this project strives to do is deter from redundant tasks, and help provide an interface to tackeling larger web applications. This project is a wrapper for the official selenium bindings and pyselenium-js, offering a more object orientated approach. **py-component-controller** also includes polyfills for conforming webdriver behavior -- such as the safari webdriver's handling of multiple element queries.

## Why

The official selenium bindings for Python feel rather dated, and a single interaction such as checking an element's visibility after clicking it can take a myriad of api calls. Additionally, the official Selenium bindings operate in the most natural way a user would operate against a given web page; simple actions such as clicking on an element can be disasterous for modern web applications using a `z-index` on panels and more commonly modals, because the selenium bindings attempt to get the element's coordinate position before actually executing the click. Using [pyselenium-js](https://github.com/neetjn/pyselenium-js) under the hood, this framework can alleviate the many burdens regularly encountered while using selenium.

**py-component-controller** also offers a very easy-to-use interface for structuring selenium tests, with method chaining functionality. Take the following example,

```python
app = App(webdriver, base_url, {
  'header', Header,
  'footer': Footer,
  'home': Home
})

assert app.components.header.log_in\
  .wait_visible(timeout=1, error=True)\
  .click()\
  .wait_invisible(timeout=3)\
  .get_attribute('toggled')
```
Looks easy to maintain, no?

## Breakdown

A component represents an area in the web application user interface that your test is interacting with. Component objects were created to represent every possible element a controller and/or test would need to reference. Component objects allow us to define an element once, and reference it however many times we need by it's defined property. If any major changes are made to our target interface, we can change the definition of a component's property once and it will work across all of our given controllers and tests. Reference: [Page Object](http://selenium-python.readthedocs.io/page-objects.html)

Controllers were created to utilize our defined component objects and to farm out tedious rudimentary tasks such as navigating and managing our context. Controllers allow us to define our logic in a behavioral manner, outside of our test cases, keeping everything clean, simple, and manageable. Controllers also allow us to reference a browser once and pass it to all of our defined components. Reference: [Page Object Model](http://www.guru99.com/page-object-model-pom-page-factory-in-selenium-ultimate-guide.html)

## Usage

This project was created using selenium `3.6.0`, and pyseleniumjs `1.3.6`.

Support is available for both Python 2.7 and 3.6.

**py-component-controller** can be installed using pip like so,

```sh
pip install pyscc
```

To define a new component, simply import `Component`, `component_element`, `component_elements`, and `component_group` from `pyscc`.

```python
from pyscc import Component, component_element, component_elements, component_group


class Home(Component):

  @component_element
  def username(self):
    return '#user' if self.env.legacy else '#username'

  @component_elements
  def articles(self):
    return 'div.articles'

  @component_group
  def social_links(self):
    return {
      'facebook': 'a#facebook',
      'twitter': 'a#twitter',
      'linkedin': 'a#linkedin',
    }
```

Controllers can be defined using the `Controller` class which can also be imported from `pyscc`.

```python
from pyscc import Controller
from project.components import Home


class Product(Controller):

  def __init__(self, browser, base_url, **env):
    super(Product, self).__init__(browser, base_url, {
        'home': Home
      },
      env=**env
    )
    self.logged_in = False

  def count_articles(self):
    return self.components.home.articles.count()

  def login(self, username, password):
    home = self.components.home
    home.username.wait_visible(5, error=True)\
      .send_input(username)
    home.password.wait_for(5, error=True)\
      .send_input(password, force=True)
    home.country_selection.trigger_event(event='change')\
      .click()
    self.wait(timeout=5, condition=home.country_selection.check.invisible)
    self.logged_in = True

product = Product(webdriver.Chrome(), 'https://mysite.com', legacy=False)
```

As can be seen in the controller example, a component included in the constructor can be accessed at any time by it's key pair name. The `env` variable we instantiate in our `Product` instance `legacy`, is also trickeled down into each of `Product`'s components which can then be processed as done in the `Component` example.

## Testing

All module related e2e tests are in the `tests` subdirectory. To setup your environment run `make setup`. To stand up the mock site, run `make app`. This will serve the site on localhost:3000. To run the test suite, use `make test`.

The mock site was created using Riot.js 3, SkeletonCSS, and webpack 3. It was designed to represent a common website layout with responsive capabilities. To add new features for unit tests, refer to [riot-todo](https://github.com/neetjn/riot-todo) and be sure to update the submodule commit accordingly.

Requirements:
* Python 2.7, 3.6 (with pip)
* Chrome or Chromium (*last confirmed test used version 62*)
* ChromeDriver (*last confirmed test used version 2.33*)
* Node.js 6+ (with npm)

### Contributors

* **John Nolette** (john@neetgroup.net)

Contributing guidelines are as follows,

* Any new features added must also be unit tested in the `tests` subdirectory.
* Branches for bugs and features should be structued like so, `issue-x-username`.
* Include your name and email in the contributors list.

---
Copyright (c) 2017 John Nolette Licensed under the Apache License, Version 2.0.
