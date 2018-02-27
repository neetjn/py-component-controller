# py-component-controller

[![build](https://travis-ci.org/neetjn/py-component-controller.svg?branch=master)](https://travis-ci.org/neetjn/py-component-controller)
[![Documentation Status](https://readthedocs.org/projects/py-component-controller/badge/?version=latest)](http://py-component-controller.readthedocs.io/en/latest/?badge=latest)
[![Code Health](https://landscape.io/github/neetjn/py-component-controller/master/landscape.svg?style=flat)](https://landscape.io/github/neetjn/py-component-controller/master)
[![codecov](https://codecov.io/gh/neetjn/py-component-controller/branch/master/graph/badge.svg)](https://codecov.io/gh/neetjn/py-component-controller)

[![PyPI version](https://badge.fury.io/py/pyscc.svg)](https://badge.fury.io/py/pyscc)
[![Join the chat at https://gitter.im/py-component-controller/Lobby](https://badges.gitter.im/py-component-controller/Lobby.svg)](https://gitter.im/py-component-controller/Lobby?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

**py-component-controller** is an opinionated framework for structuring selenium test suites.

This project depends on the [pyselenium-js](https://github.com/neetjn/pyselenium-js) project.

Official documentation be be read [here](http://py-component-controller.readthedocs.io).

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

For more information refer to the official documentation [here](http://py-component-controller.readthedocs.io)

## Testing

All module related e2e tests are in the `tests` subdirectory. This project uses pipenv, so to setup your environment install pipenv from pip using `pip install pipenv` and create your environment with `pipenv install --dev`. For test coverage pytest is used; to run the suite use `pipenv run pytest tests`.

The mock site can be accessed [here](http://riot-todo-84334.firebaseapp.com/); it was created using Riot.js 3, SkeletonCSS, and webpack 3. It was designed to represent a common website layout with responsive capabilities.

Requirements:
* Python 2.7, 3.6 (with pip/pipenv)
* Chrome or Chromium (Chrome 60-64)
* ChromeDriver (version 2.3.3)

### Contributors

* **John Nolette** (john@neetgroup.net)

Contributing guidelines are as follows,

* Any new features added must also be unit tested in the `tests` subdirectory.
  * Branches for bugs and features should be structured like so, `issue-x-username`.
* Include your name and email in the contributors list.

---
Copyright (c) 2017 John Nolette Licensed under the Apache License, Version 2.0.
