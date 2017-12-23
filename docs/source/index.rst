======================
Introduction
======================

What this project strives to do is deter from redundant tasks, and help provide an interface to tackeling larger web applications.
This project is a wrapper for the official selenium bindings and pyselenium-js, offering a more object orientated approach.
py-component-controller also includes polyfills for conforming webdriver behavior -- such as the safari webdriver's handling of multiple element queries.

About
=====

The official selenium bindings for Python feel rather dated, and a single interaction such as checking an element's visibility after clicking it can take a myriad of api calls.
Additionally, the official Selenium bindings operate in the most natural way a user would operate against a given web page; simple actions such as clicking on an element can be disasterous for modern web applications using a z-index on panels and more commonly modals, because the selenium bindings attempt to get the element's coordinate position before actually executing the click.
Using `pyselenium-js <https://github.com/neetjn/pyselenium-js>`_ under the hood, this framework can alleviate the many burdens regularly encountered while using selenium.

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
