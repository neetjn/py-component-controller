======================
Getting Started
======================

Components
==========

A component object represents an area in the web application user interface that your test is interacting with.
Component objects were created to represent every possible element a controller and/or test would need to reference.
Component objects allow us to define an element once, and reference it however many times we need by it's defined property.
If any major changes are made to our target interface, we can change the definition of a component's property once and it will work across all of our given controllers and tests. Reference: `Page Object <http://www.guru99.com/page-object-model-pom-page-factory-in-selenium-ultimate-guide.html>`_

Controllers
===========

Controllers were created to utilize our defined component objects and to farm out tedious rudimentary tasks such as navigating and managing our context.
Controllers allow us to define our logic in a behavioral manner, outside of our test cases, keeping everything clean, simple, and manageable.
Controllers also allow us to reference a browser once and pass it to all of our defined components. Reference: `Page Object Model <http://www.guru99.com/page-object-model-pom-page-factory-in-selenium-ultimate-guide.html>`_

Simple Usage
============

The following code is an example of a controller for Google's search engine:

.. code-block:: python

    from pyscc import Controller, Component, component_element, \
        component_elements, component_group


    class Home(Component):

        @component_element
        def search_bar(self):
            # we only need to return the selector
            # pyscc will automatically determine whether it's xpath or css
            return 'input#lst-ib'

        @component_element
        def search_button(self):
            # the element wrapper allows us to format our selectors
            # ref.search_button.fmt(value='Google Search')
            return '//input[@type="submit"][@value="{value}"]'


    class Results(Component):

        @component_elements
        def results(self):
            return 'div.g'


    class Google(Controller):

        def __init__(self, browser, base_url):
            super(Product, self).__init__(browser, base_url, {
                'home': Home,
                'results': Results
            })

        def number_of_results():
            return self.components.results.results.count()


The sample above can be utilized like so:


.. code-block:: python

    from selenium import webdriver

    google = Google(webdriver.Chrome(), 'https://google.com')

    # wait 5 seconds for search bar to be visible
    # write py-component-controller in the search bar
    google.home.search_bar\
        .wait_visible(5, error=True)\
        .send_input('py-component-controller')

    # target the search button with the text "Google Search"
    # click on the search button
    google.home.search_button\
        .fmt('Google Search')\
        .click()

    # wait for at least 1 search result to be available
    google.results.results\
        .wait_for(5, length=1, error=True)

    # terminate our controller's webdriver
    google.exit()


Example Explained
=================

As seen in the example above, components can be defined relatively quickly without any hassle.
Simply import `Component` from pyscc and define your class. When specifying your component properties,
the following decorators can be used to construct `Element <http://github.com/neetjn/py-component-controller>`_ and `Elements <http://github.com/neetjn/py-component-controller>`_ wrappers.

* **@component_element**: Expects a single css or xpath selector, will return an `Element` object when referenced.
* **@component_elements**: Expects a single css or xpath selector, will return an `Elements` object when referenced.
* **@component_group**: Expects a dictionary of element name and selector pairs, will return a resource with attributes relevant to your provided pairs returning `Element` objects when referenced.

Using the intended design pattern, Component instances should never be instantiated outside of the scope of the controller.
When the controller is intantiated, it will take the provided component name pairs and automatically instantiate them in a `components` attribute.
