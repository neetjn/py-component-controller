==================
Controller Service
==================

About
=====

Controller services allow developers to modularize controllers for larger web applications.
Services are a lightweight resource that simply consume a given controller, and allow developers to
design functionality using the same contextual logic as they would within a controller.

Best Practices
==============

If a controller is exceeding some 800 lines of code, it may be beneficial for both
organization and productivity to compartementalize strings of functionality operating
off of the same base component.

Implementation
==============

Services are part of the 0.2.1 Controller specification. To use this functionality in the meantime,
import and reference `ControllerSpec` instead of the `Controller` object from the `controller` module.

Example
=======

The following example is an abstraction of the `Google` controller featured on `Getting Started <http://py-component-controller.readthedocs.io/en/latest/getting_started.html>`_:

.. code-block:: python

    from pyscc import Controller, Component, Service, component_element, \
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


    class SearchService(Service):

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


    class Google(Controller):

        def __init__(self, browser, base_url):
            super(Product, self).__init__(
                browser,
                base_url,
                components={
                    'home': Home,
                    'results': Results
                },
                services={'search': SearchService}
            )

        def number_of_results():
            return self.components.results.results.count()


The sample above can be utilized like so:

.. code-block:: python

    from selenium import webdriver

    google = Google(webdriver.Chrome(), 'https://google.com')
    google.services.search.search('py-component-controller')
    # ensure at least one result is available within 5 seconds
    assert google.components.results.results\
        .wait_for(5, length=1)

    # terminate our controller's webdriver
    google.exit()
