==========
Components
==========

About
=====

A component represents an area in the web application user interface that your test is interacting with.
Component objects were created to represent every possible element a controller and/or test would need to reference.
Component objects allow us to define an element once, and reference it however many times we need by it's defined property.
If any major changes are made to our target interface, we can change the definition of a component's property once and it will work across all of our given controllers and tests. Reference: `Page Object <http://www.guru99.com/page-object-model-pom-page-factory-in-selenium-ultimate-guide.html>`_

Best Practices
==============

Following this architectural pattern (controller, component) your component should **only** consist of element properties.
Any accessory functionality should be provided by your controller.

If you haven't already check out `Getting Started <http://py-component-controller.readthedocs.io/en/latest/getting_started.html>`_ for examples.

Contructor
==========

When a component is instantiated, the constructor automatically constructs the following attributes:

* **controller**: Reference to parent controller instance.
* **browser**: Reference to parent controller's webdriver.
* **env**: Reference to parent controller's env resource.

Element (wrapper)
=================

Formatting Selectors
--------------------

As shown in `Getting Started <http://py-component-controller.readthedocs.io/en/latest/getting_started.html>`_, elements may be defined with template selectors.
Take for example the following component element provider:

.. code-block:: python

    @component_element
    def button(self):
        return 'button[ng-click="{method}"]'

You can format the element's selector prior to executing any operations.

.. code-block:: python

    component.button.fmt(method="addUser()")\
        .wait_for(5)\
        .click()

Fetching a Selenium WebElement
------------------------------

The element wrapper will still allow you to fetch selenium WebElement objects and access the standard selenium bindings.

.. code-block:: python

    component.button.get()
    >> WebElement

Getting Element Text
--------------------

To scrape text from an element, the element wrapper provides an api method *text*:

.. code-block:: python

    component.button.text()

    # scrape raw text (inner html)
    component.button.text(raw=True)

Getting Element Value
---------------------

Input elements provide a property, **value**, which selenium does not provide explicit bindings for.
Using the api method *value* you may pull the value from any input element (including select, button, radiobutton).

.. code-block:: python

    component.username_field.value()

Getting and Setting Element Attribute
-------------------------------------

Using the element wrapper, an element's attribute can be fetched like so:

.. code-block:: python

    component.username_field.get_attribute('aria-toggled')

Additionally, an element's attribute can be set using the *set_attribute* api method (chainable):

.. code-block:: python

    component.username_field\
        .set_attribute('hidden', False)\
        .wait_visible(3, error=True)

Under the hood, pyselenium-js will automatically convert javascript types into pythonic types and inverse.

Getting and Setting Element Property
------------------------------------

**This feature is not supported by the official selenium bindings (or remote api).**

Using the element wrapper, an element's property can be fetched like so:

.. code-block:: python

    component.remind_me.get_property('checked')

Additionally, an element's attribute can be set using the *set_attribute* api method (chainable):

.. code-block:: python

    component.username_field\
        .set_property('checked', True)\
        .fmt(class='checked')\
        .wait_for(3, error=True)

As explained in the attribute section, pyselenium-js under the hood will automatically convert javascript types into pythonic types and inverse.

Clicking and Double Clicking an Element
---------------------------------------

The official selenium bindings attempt to click on an element based on it's coordinate position, to emulate a natural click event on a given element.
The problem with this, is more modern websites rely on *z-index* styling rules for pop ups and raised panels; making it impossible to locate the correct coordinates otherwise raising a WebDriverException exception.
This behavior has also shown to be especially problematic in nested iframes.

The element wrapper's *click* method will dispatch a click event directly to the target element.
Additionally, the wrapper provides an api method *dbl_click* to double click on a given element -- **this feature is not supported by the official selenium bindings**.

These two methods are also chainable:

.. code-block:: python

    component.button\
        .click()\
        .dbl_click()

If you require the traditional clicking behavior, simplify fetch a selenium WebElement like so:

.. code-block:: python

    component.button.get().click()

Scrolling To an Element
-----------------------

Scroll to an element can be done using the *scroll_to* api method (chainable).

.. code-block:: python

    component.button\
        .scroll_to()\
        .click()

Dispatching an Event
--------------------

Flexing the capabilities of pyselenium-js, we can construct and dispatch events to a given element like so:

.. code-block:: python

    component.button\
        .trigger_event('click', 'MouseEvent', {'bubbles': True})\
        .wait_invisible(timeout=5, error=True)

This method is chainable as the example details.

Sending Input
-------------

Waiting For an Element
----------------------

Waiting For Visibility
----------------------

Javascript Conditional Wait
---------------------------

Checking Availability
---------------------

Checking Visibility
-------------------

Checking Wait Status (javascript)
---------------------------------


Elements (wrapper)
==================

Formatting Selectors
--------------------

Fetching List of Selenium WebElements
-------------------------------------

Counting Existing Matches
-------------------------

Getting List of Element Text
----------------------------

Getting List of Element Value
-----------------------------

Waiting For Number of Elements
------------------------------

Waiting For Visibility of Elements
----------------------------------

Check Visibility
----------------
