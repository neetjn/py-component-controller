<a target='_blank' rel='nofollow' href='https://app.codesponsor.io/link/ymhxqZ47jLBFuVrU2iywqLGC/neetjn/py-component-controller'>
  <img alt='Sponsor' width='888' height='68' src='https://app.codesponsor.io/embed/ymhxqZ47jLBFuVrU2iywqLGC/neetjn/py-component-controller.svg' />
</a>

# py-component-controller

[![build](https://travis-ci.org/neetjn/py-component-controller.svg?branch=master)](https://travis-ci.org/neetjn/py-component-controller)
[![Join the chat at https://gitter.im/py-component-controller/Lobby](https://badges.gitter.im/py-component-controller/Lobby.svg)](https://gitter.im/py-component-controller/Lobby?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

PCC is an opinionated framework for structuring selenium test suites. This project depends on the [pyselenium-js](https://github.com/neetjn/pyselenium-js) project.

## About

What this project strives to do is deter from redundant tasks, and help provide an interface to tackeling larger web applications. This project is a wrapper for the official selenium bindings and pyselenium-js, offering a more object orientated approach. PCC also includes polyfills for conforming webdriver behavior -- such as the safari webdriver's handling of multiple element queries.

## Breakdown

A component object represents an area in the web application user interface that your test is interacting with. Component objects were created to represent every possible element a controller and/or test would need to reference. Component objects allow us to define an element once, and reference it however many times we need by it's defined property. If any major changes are made to our target interface, we can change the definition of a component's property once and it will work across all of our given controllers and tests. Reference: [Page Object](http://selenium-python.readthedocs.io/page-objects.html)

Controllers were created to utilize our defined component objects and to farm out tedious rudimentary tasks such as navigating and managing our context. Controllers allow us to define our logic in a behavioral manner, outside of our test cases, keeping everything clean, simple, and manageable. Controllers also allow us to reference a browser once and pass it to all of our defined components. Reference: [Page Object Model](http://www.guru99.com/page-object-model-pom-page-factory-in-selenium-ultimate-guide.html)

## Usage

This project was created using Python 2.7, selenium `3.0.0b3`, and pyseleniumjs `1.3.1`. An update for Python 3 will be available with pyseleniumjs version 2, as well as the latest version of selenium.

PCC can be installed using pip like so,

```sh
pip install py-component-controller
```

To define a new component, simply import `Component` from `py_component_controller`.

```python
from py_component_controller import Component


class Home(Component):

  @property
  def username(self):
    return self.find_element_by_css_selector('#username') if \
      self.env.legacy else self.find_element_by_css_selector('#newUsername')

  @property
  def articles(self):
    return self.webdriver.find_elements_by_css_selector('div.article')
```

Controllers can be defined using the `Controller` class which can also be imported from `py_component_controller`.

```python
from py_component_controller import Controller
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
    self.logged_in = False

  def count_articles(self):
    return len(self.components.home.articles)

  def login(self, username, password):
    # do login
    self.logged_in = True
    ...

product = Product(webdriver.Chrome(), 'https://mysite.com', legacy=False)
```

As can be seen in the controller example, a component included in the constructor can be accessed at any time by it's key pair name. The `env` variable we instantiate in our `Product` instance `legacy`, is also trickeled down into each of `Product`'s components which can then be processed as done in the `Component` example.

## Testing

All module related e2e tests are in the `py_component_controller/tests` subdirectory. To setup your environment run `make setup`. To stand up the mock site, run `make app`. This will serve the site on localhost:3000. To run the test suite, use `make tests`.

The mock site was created using Riot.js 3, TWBS, webpack 2.2, and webpack dev server. It was designed to represent a common website layout with responsive capabilities. To add new features for unit tests, refer to [pcc-mock-site](https://github.com/neetjn/pcc-mock-site) and be sure to update the submodule commit accordingly.

Requirements:

* Chromium 60
* ChromeDriver 2.32.3
* Node.js 6
* Python 2.7
* Pip

### Contributors

* **John Nolette** (john@neetgroup.net)

Contributing guidelines are as follows,

* Any new features added must also be unit tested in the `pcc/tests` subdirectory.
* Branches for bugs and features should be structued like so, `issue-x-username`.
* Include your name and email in the contributors list.

---
Copyright (c) 2017 John Nolette Licensed under the Apache License, Version 2.0.
