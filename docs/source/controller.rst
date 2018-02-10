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

Best Practices
==============

Following this architectural pattern (controller, component) your controller **not** contain any accessory methods to search for or provide elements.
This class of functionality should be handled exclusively by your defined components.

If you haven't already check out `Getting Started <http://py-component-controller.readthedocs.io/en/latest/getting_started.html>`_ for examples.

Polyfills
=========

Believe it or not, each webdriver for each major browser is maintained by their respective company.
Selenium offers an api and a spec that these companies simply adhere to, which is what allows the selenium bindings to conformally speak to any of your desired browsers (for the most part).
When a controller instance is instantiated, it will consume the webdriver passed and monkey patch operations and or functions for equality.

The most prevelant polyfill featured is uniformity for `find_elements_by_x`. Every webdriver, but Safari (of course), will return an empty list as where Safari's will raise an `ElementNotFoundException`.

Any irregularities between webdrivers should be reported via the py-component-controller github with steps to reproduce and a related issue or task if available for the corresponding webdriver.

Contructor
==========

When a controller is instantiated, the constructor automatically binds the following attributes:

* **browser**: Webdriver consumed in the constructor.
* **js**: Reference to instantiated pyselenium-js driver.
* **logger**: Python logger reference.
* **components** Resource for instantiated components constructed using the dictionarty provided in the constructor.
* **env**: Resource for environmental variables consumed in the form of kwargs from the constructor.

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

    # check against a list of possible routes
    controller.is_location('/neetjn/pyselenium-js', '/neetjn/py-component-controller')

Switching to Window by Title
===============================

For window management, the controller provides a method that allows you to switch to a window by title:

.. code-block:: python

    # partial window title check
    controller.window_by_title('readthedocs')
    >> True, False

    # strict window title check
    controller.window_by_title('readthedocs - My Docs', strict=True)
    >> True, False

    # polling for window by title
    controller.window_by_title('readthedocs', timeout=5)
    >> True, False

    # error if condition is not met
    controller.window_by_title('readthedocs', timeout=5, error=True)
    controller.window_by_title('readthedocs', timeout=5,
        error='Could not find the expected readthedocs window')

Switching to Window by Location
===============================

The controller also provided a method that allows you to switch to a window by location:

.. code-block:: python

    # partial window location check
    controller.window_by_location('readthedocs.io')
    >> True, False

    # strict window location check
    controller.window_by_location('https://readthedocs.io/neetjn', strict=True)
    >> True, False

    # poll for window by location
    controller.window_by_location('readthedocs.io', timeout=5)
    >> True, False

    # error if condition is not met
    controller.window_by_location('readthedocs.io', timeout=5, error=True)
    controller.window_by_location('readthedocs.io', timeout=5,
        error='Could not find the expected readthedocs window')

Conditional Waits
=================

Unlike the official selenium bindings, the controller allows an interface for an all-purpose general conditional wait.

.. code-block:: python

    # wait 5 seconds for element to be visible
    # you may pass any callable object as a condition that returns a truthy value
    controller.wait(timeout=5, condition=element.check.visible)

    # wait for 10 seconds for window to be available with the title "Github"
    controller.wait(timeout=10,
        condition=lambda: controller.window_by_title('Github'))
    >> True, False

    # by design the wait will ignore any exceptions raised while checking the condition
    # for debugging purposes, you may toggle the throw_error flag to raise the last error
    controller.wait(timeout=5, throw_error=True, condition=lambda: 0/0)

    # you may toggle the reverse flag to check for a falsy value
    controller.wait(timeout=5, reverse=True, condition=element.check.invisible)


Take a Screenshot
=================

To take a screenshot and drop it to your host machine, use the *screen_shot* method:

.. code-block:: python

    controller.screen_shot('logout')

The screenshot prefix is optional, but this method will automatically generate a unique file name to deter from any io errors and preserve your artifacts.

Get Browser Console Logs
========================

Using `pyselenium-js <https://github.com/neetjn/pyselenium-js/blob/master/pyseleniumjs/e2ejs.py#L130>`_ under the hood we can log our browser's console output.
To initialize the logger, you can reference the *console_logger* method from the controller's js attribute (pysjs reference).
Once you've initialized the logger, use the controller api method *browser_logs* to drop your logs to your host machine.

.. code-block:: python

    # initialize logger
    controller.js.console_logger()

    # dump browser console logs
    controller.browser_logs()

    # dump browsers logs with a log name
    controller.browser_logs('error.logout.redirect')


Terminate Webdriver Session
===========================

Equipped with the controller is an all-webdriver termination mechanism.
This can be especially helpful for provisioned environments using both local and remote webdrivers.

.. code-block:: python

    controller.exit()
