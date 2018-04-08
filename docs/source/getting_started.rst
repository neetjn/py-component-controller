======================
Getting Started
======================

Sample Usage
============

The following code is an example of a controller for Google's search engine:

.. code-block:: python

    from pyscc import Controller, Component, component_element, \
        component_elements, component_group


    class Home(Component):

        _ = 'body > app'  # optional root selector to be applied to all component items

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

        def search(self, query, redirect=False):
            # navigate to base url
            self.navigate('/')
            # create reference to our home component
            home = self.components.home
            # wait 5 seconds for search bar to be visible
            # write query in the search bar
            home.search_bar\
                .wait_visible(5, error=True)\
                .send_input(query)

            # target the search button with the text "Google Search"
            # click on the search button
            home.search_button\
                .fmt('Google Search')\
                .click()

        def number_of_results():
            return self.components.results.results.count()


The sample above can be utilized like so:


.. code-block:: python

    from selenium import webdriver

    google = Google(webdriver.Chrome(), 'https://google.com')
    google.search('py-component-controller')
    # ensure at least one result is available within 5 seconds
    assert google.components.results.results\
        .wait_for(5, length=1)

    # terminate our controller's webdriver
    google.exit()


Example Explained
=================

As seen in the example above, components can be defined relatively quickly without any hassle.
Simply import `Component` from pyscc and define your class. When specifying your component properties,
the following decorators can be used to construct `Element <http://py-component-controller.readthedocs.io/en/latest/component.html#element-wrapper>`_ and `Elements <http://py-component-controller.readthedocs.io/en/latest/component.html#elements-wrapper>`_ wrappers.

* **@component_element**: Expects a single css or xpath selector, will return an `Element` object when referenced.
* **@component_elements**: Expects a single css or xpath selector, will return an `Elements` object when referenced.
* **@component_group**: Expects a dictionary of element name and selector pairs, will return a resource with attributes relevant to your provided pairs returning `Element` objects when referenced.

Using the intended design pattern, Component instances should never be instantiated outside of the scope of the controller.
When the controller is intantiated, it will take the provided component name pairs and automatically instantiate them in a `components` attribute.

Writing Tests
=============

The pyscc framework works very well for creating scrapers and other automation tools, but it was designed with end to end testing in mind.
Controllers were also designed to allow developers to easily export their work into client packages for larger suites.
The following is an example as to how one may structure tests:


.. code-block:: python

    from project import Google
    from selenium import webdriver
    from unittest import TestCase


    class GoogleBaseTest(TestCase):

        def setUp(self):
            self.google = Google(webdriver.Chrome(), 'https://google.com')

        def tearDown(self):
            self.google.exit()


    ...


    class TestGoogleHome(GoogleBaseTest):

        def test_search(self):
            self.google.search('py-component-controller')
            # ensure at least one result is available within 5 seconds
            self.assertNotNone(self.google.components.results.results\
                .wait_for(5, length=1))

        def test_search_autocomplete(self):
            home = self.google.components.home
            home.search_bar\
                .wait_visible(5, error='Google search bar was not visible')\
                .click()\
                .send_input("python")
            # ensure autocomplete popup appears
            self.assertEqual(home.get_attribute('aria-haspopup'))


As can be seen in the example above, our product logic is actually loosely coupled with the test.
Our controller allows us to define shorthand functionality ie; search, but we can still directly access each individual component and their respective elements.
The controller and component have also been designed to work on any webdriver across any platform (excluding mobile forks) using polyfills, so you can write your code once and provision it to run in any environment you please!
