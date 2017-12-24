==========
Controller
==========

As explained in the introduction, controllers were created to simplify redundant tasks and approach the selenium framework with a more object orientated approach.
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

Properties
==========

Methods
=======

