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

Fetching a Selenium WebElement
------------------------------

Getting Element Text
--------------------

Getting Element Value
---------------------

Getting and Setting Element Attribute
-------------------------------------

Getting and Setting Element Property
------------------------------------

Clicking and Double Clicking an Element
---------------------------------------

Scrolling To an Element
-----------------------

Dispatching an Event
--------------------

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
