==========
Controller
==========

About
=====

Controllers were created to utilize our defined components and to farm out tedious rudimentary tasks such as navigating and managing our context.
Controllers allow us to define our logic in a behavioral manner, outside of our test cases, keeping everything clean, simple, and manageable.
Controllers also allow us to reference a browser once and pass it to all of our defined components. Reference: `Page Object Model <http://www.guru99.com/page-object-model-pom-page-factory-in-selenium-ultimate-guide.html>`_

There are a vast other quirks to using the controller, component architecture -- such as:

* Simple exportable client packages for larger suites (multi-application end to end tests).
* Clean tests; no need for instance-hacks.
* Maintainability, easily documentable.
* Application/website state management.

Polyfills
=========

Believe it or not, each webdriver for each major browser is maintained by their respective company.
Selenium offers an api and a spec that these companies simply adhere to, which is what allows the selenium bindings to conformally speak to any of your desired browsers (for the most part).
When a controller instance is instantiated, it will consume the webdriver passed and monkey patch operations and or functions for equality.

The most prevelant polyfill featured is uniformity for `find_elements_by_x`. Every webdriver, but Safari (of course), will return an empty list as where Safari's will raise an `ElementNotFoundException`.

Any irregularities between webdrivers should be reported via the py-component-controller github with steps to reproduce and a related issue or task if available for the corresponding webdriver.

Contructor
==========

When inheriting from the `Controller` class, it's important to understand that

Getting Current Location
==========================

The controller provides a property *navigation* that can be referenced to fetch your webdriver's current location.

.. code-block:: python
    controller.location
    >> http://github.com

Getting Current Page Title
==========================

Refer to the controller's *title* property to pull the current page title from your webdriver.

.. code-block:: python
    controller.title
    >> Github

Navigation
==========

When a controller is instantiated, it will automatically send the webdriver to the base url specified.
You may then navigate to other routes off of the base url like so:

.. code-block:: python
    controller.navigate('/about')

For a *hard* navigation, you may use the selenium webdriver api method **get**.

.. code-block:: python
    controller.browser.get('http://github.com')

Checking Location
=================

To check against your webdriver's current location, you can use the *is_location* method:

.. code-block:: python
    # check if the route is in your webdrivers location
    controller.is_location('/neetjn/py-component-controller')
    # strict check on absolute location
    controller.is_location('https://github.com/neetjn/py-component-controller', strict=True)
    # timed location check, will check every second until condition met or timeout exceeded
    controller.is_location('/neetjn/py-component-controller', timeout=5)
    # error if condition is not met
    controller.is_location('/neetjn/py-component-controller', timeout=5, error=True)
    controller.is_location('/neetjn/py-component-controller', timeout=5,
        error='Expected to be on py-component-controller repository page')

Switching to Window by Title
===============================

For window management, the controller provides a method that allows you to switch to a window by title:

.. code-block:: python
    # absolute window title check
    self.assertTrue(controller.window_by_title('readthedocs'))
    # partial window title check
    self.assertTrue(controller.window_by_title('readthedocs', graceful=True))

Switching to Window by Location
===============================

The controller also provided a method that allows you to switch to a window by location:

.. code-block:: python
    # absolute location check
    self.assertTrue(controller.window_by_title('https://readthedocs.io/neetjn'))
    # partial location title check
    self.assertTrue(controller.window_by_title('readthedocs.io', graceful=True))

Conditional Waits
=================

Take a Screenshot
=================

Get Browser Console Logs
========================

Terminate Webdriver Session
===========================
