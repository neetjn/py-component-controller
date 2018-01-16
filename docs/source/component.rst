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

When a component is instantiated, the constructor automatically binds the following attributes:

* **controller**: Reference to parent controller instance.
* **browser**: Reference to parent controller's webdriver.
* **env**: Reference to parent controller's env resource.

Element (wrapper)
=================

The Element object, is a wrapper for managing individual web elements.
This object provides a targeted api for particular elements, rather than having to depend solely on the selenium webdriver.
It features many useful short-hand properties and methods, and uses the pyselenium-js driver under the hood for stability.

This entity is not to be confused with the official selenium api's WebElement entity.
Given the decorator **@component_element**, whenever referenced the component property will return a *new* instance of the Element wrapper catered to the specific element using the provided selector.

Formatting Selectors
--------------------

As shown in `Getting Started <http://py-component-controller.readthedocs.io/en/latest/getting_started.html>`_, elements may be defined with template selectors.
Take for example the following component element provider:

.. code-block:: python

    @component_element
    def button(self):
        return 'button[ng-click="${method}"]'

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

Additionally, an element's attribute can be set using the *set_property* api method (chainable):

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

Additionally, for elements that do not listen on the click event but rather mouseup or mousedown, you may refer to the api methods `mouseup` and `mousedown` (chainable):

.. code-block:: python

    component.button\
        .mouseup()\
        .mousedown()

Scrolling To an Element
-----------------------

Scrolling to an element can be done using the *scroll_to* api method (chainable).

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

To send input to an element, refer to the *send_input* api method (chainable):

.. code-block:: python

    # send_input will always clear the provided field or element before sending input
    component.username_field\
        .send_input('py-component-controller')\
        .get_attribute('class')

    # you may disable the field or element clearing by using the clear flag
    component.username_field\
        .send_input('rocks', clear=False)

    # in the event the component element is a custom element that accepts input
    # and it does not support the focus event, the selenium bindings will raise a WebDriverException
    # you may use the force flag to overwrite the innerhtml of the element rather than
    # traditionally sending input
    component.email_field.send_input('pyscc', force=True)

Waiting For an Element
----------------------

One of the more helpful features of the element wrapper is it's suite of built in waits.
To simply wait for an element to be available, you may use the *wait_for* api method (chainable) like so:

.. code-block:: python

    # wait 5 seconds for element to be available
    component.button\
        .wait_for(5)\
        .click()

    # alternatively you can also have the wait automatically error out if the condition is not met
    component.button\
        .wait_for(5, error=True)\
        .click()

    # custom error messages can also be specified as the error flag
    component.button\
        .wait_for(5, error='Component button was not avaialable as expected')\
        .click()

    # when waiting for an element to be unavailable, simply use the available flag
    component.button\
        .click()\
        .wait_for(5, available=False, error=True)

Waiting For Visibility
----------------------

If you require the visibility of an element, the element wrapper allows you to wait for the visibility or invisibility of an element with the api methods *wait_visible* and *wait_invisible* (chainable).

.. code-block:: python

    # wait for an element to become visible
    component.button\
        .wait_visible(5, error=True)\
        .click()

    # wait for an element to become invisible
    component.button\
        .click()\
        .wait_invisible(5)

Javascript Conditional Wait
---------------------------

Pulling from the pyselenium-js api, you may alternatively asynchronously farm a wait to your target browser.
This can also be especially useful when waiting for conditions that occur in timespans < 1 second.

Syntax is as follows:

.. code-block:: python

    # wait on an interval of every 150 ms for element to include as class 'btn-danger'
    component.button.wait_js('$el.getAttribute("class").includes("btn-danger")', 150)

The element can be accessed within the condition by the alias $el.
To validate the javascript wait status, refer to `Checking Wait Status (javascript) <http://py-component-controller.readthedocs.io/en/latest/component.html#checking-wait-status-javascript>`_.

Checking Availability
---------------------

The element wrapper provides two callable, explicit check for element availablity. Refer to the `available` and `not_available` api methods.

.. code-block:: python

    component.button.check.available()
    >> True, False

    component.button.check.not_available()
    >> True, False

Checking Visibility
-------------------

The element wrapper provides two callable, explicit check for element visibility. Refer to the `visible` and `invisible` api methods.

.. code-block:: python

    component.button.check.visible()
    >> True, False

    component.button.check.invisible()
    >> True, False

Checking Wait Status (javascript)
---------------------------------

The api method *wait_status* can be used to validate the wait status of a previously dispatched wait request on an element instance.

.. code-block:: python

    button = component.button
    # wait on an interval of every 150 ms for element to include as class 'btn-danger'
    button.wait_js('$el.getAttribute("class").includes("btn-danger")', 150)
    ...
    button.check.wait_status()
    >> True, False


Elements (wrapper)
==================

The Elements object, is a wrapper for managing groups of web elements.
This object provides a targeted api for particular elements, rather than having to depend solely on the selenium webdriver.
It features many useful short-hand properties and methods, and uses the pyselenium-js driver under the hood for stability.

This entity is not to be confused with the official selenium api's WebElement entity.
Given the decorator **@component_elements**, whenever referenced the component property will return a *new* instance of the Elements wrapper catered to the specific elements using the provided selector.

Formatting Selectors
--------------------

As shown in `Getting Started <http://py-component-controller.readthedocs.io/en/latest/getting_started.html>`_, elements may be defined with template selectors.
Take for example the following component elements provider:

.. code-block:: python

    @component_elements
    def users(self):
        return 'a.users.${class}'

You can format the element's selector prior to executing any operations.

.. code-block:: python

    component.users\
        .fmt(class="active")\
        .wait_for(5, length=1)

Fetching List of Selenium WebElements
-------------------------------------

The elements wrapper will still allow you to fetch selenium WebElements and access the standard selenium bindings.

.. code-block:: python

    component.users.get()
    >> [WebElement, ...]

.. code-block:: python

    for user in component.users.get():
        user.click()

Counting Existing Matches
-------------------------

The elements wrapper provides an api method *count* to allow you to fetch the number of given elements available.

.. code-block:: python

    component.users.count()
    >> int

Getting List of Element Text
----------------------------

To pull the text from every available element into a list, you may use the *text* api method like so:

.. code-block:: python

    component.users.text()
    >> [string, ...]

    # scrape raw text (inner html)
    component.users.text(raw=True)
    >> [string, ...]

Getting List of Element Values
------------------------------

Input elements provide a property, value, which selenium does not provide explicit bindings for. Using the api method value you may pull the value from any input element (including select, button, radiobutton).

.. code-block:: python

    component.users.value()
    >> [string, ...]

Waiting For Number of Elements
------------------------------

A helpful feature of the elements wrapper, is the ability to wait for a number of elements to become available. This can be done using the `wait_for` api method (chainable).

.. code-block:: python

    component.users.wait_for(5, length=3)

    # alternatively you can also have the wait automatically error out if the condition is not met
    component.users.wait_for(5, length=3, error=True)

    # custom error messages can also be specified as the error flag
    component.users.wait_for(5, length=3,
        error="Expected at least 3 users to be available within 5 seconds")

    # by default, wait_for will wait for the number of specified elements to be present
    # to execute a strict wait on length, you may use the strict flag
    component.users.wait_for(5, length=5, strict=True,
        error="Expected 5 users to be available within 5 seconds")

Waiting For Visibility of Elements
----------------------------------

Another powerful feature of the elements wrapper, is the ability to wait for both a number of elements to be available **and** visible.
Refer to the *wait_visible* api method (chainable):

.. code-block:: python

    component.users.wait_visible(5, length=5, error=True)

Check Visibility
----------------

The api method *visible* is a callable check to ensure the currently available elements are all visible.

.. code-block:: python

    component.users.check.visible()
    >> True, False


Component Groups
================

Several elements that can be attributed to a particular root element, can be denoted as a component group.
Component groups help keep our component objects clean, readable, and maintanable.
The following is an example of when you would use a component group,

.. image:: https://image.prntscr.com/image/Frqjg7b5Ru_96NURbUHT7g.png
   :height: 500
   :scale: 50

As can be seen from the image above, a *task* can be interpreted as a component group because each task is composed of
several elements that are a child of the task's container. This can be converted into a component group like so:

.. code-block:: python

    @component_group
    def task(self):
        return {
            '_': 'todo-task#${id}',  # optional root selector
            'checkbox': ' input[type="checkbox"]', # becomes: 'todo-task#${id} input[type="checkbox"]'
            'title': 'span#title',
            'created': 'span#created',
            'assignee': 'a#assignee'
        }

    ...

    task = component.task.fmt(id=1)
    task.check.available()
    task.checkbox\
        .wait_visible(5, error=True)\
        .click()

Component groups also have a very simplistic api to exercise basic checks on their child elements.

Check For Availability of Elements
----------------------------------

You may check if a component group's child elements are available with a single call to the *available* api method:

.. code-block:: python

    component.group.check.available()
    >> True, False

Alternatively, you may also check if all child elements are unavailable by using *not_available*.

.. code-block:: python

    component.group.check.not_available()
    >> True, False

Check For Visibility of Elements
--------------------------------

To check the visibility of a component group's child elements, you may refer to the api methods *visible* and *invisible*.

.. code-block:: python

    component.group.check.visible()
    >> True, False

    component.group.check.invisible()
    >> True, False

Getting and Setting Elements' Attribute
---------------------------------------

Using the elements wrapper, an attribute of a given list of elements can be fetched like so:

.. code-block:: python

    component.user_list.get_attribute('aria-toggled')

Additionally, a list of elements' attribute can be set using the *set_attribute* api method (chainable):

.. code-block:: python

    component.user_list\
        .set_attribute('hidden', False)\
        .wait_visible(3, error=True)

Under the hood, pyselenium-js will automatically convert javascript types into pythonic types and inverse.

Getting and Setting Elements' Property
--------------------------------------

**This feature is not supported by the official selenium bindings (or remote api).**

Using the elements wrapper, a property of a given list of elements can be fetched like so:

.. code-block:: python

    component.user_list.get_property('disabled')

Additionally, a list of elements' properties can be set using the *set_property* api method (chainable):

.. code-block:: python

    component.user_list\
        .set_property('disabled', True)\
        .fmt(class='disabled')\
        .wait_for(3, error=True)

As explained in the attribute section, pyselenium-js under the hood will automatically convert javascript types into pythonic types and inverse.
