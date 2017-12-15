# Licensed to the Software Freedom Conservancy (SFC) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The SFC licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

from pyscc.controller import Controller
from pyscc.resource import Resource
from selenium.common.exceptions import NoSuchElementException, ElementNotVisibleException
from six import string_types


class Element(Resource):
    """
    :Description: Base resource for component element.
    :param controller: Parent controller reference.
    :type controller: Controller
    :param selector: Selector of given element.
    :type selector: string
    """
    def __init__(self, controller, selector):
        self.controller = controller
        self.type = 'xpath' if '/' in selector else 'css_selector'
        self.selector = self._selector = selector
        self.formatted = False
        self.check = Check(self)
        self.validate()

    def __find_element(self, **kwargs):
        try:
            return getattr(self.controller.webdriver, 'find_element_by_{type}'.format(
                type=self.type))(kwargs.get('selector', self.selector))
        except NoSuchElementException:
            return None

    def get(self):
        """
        :Description: Used to fetch a selenium WebElement.
        :return: WebElement, None
        """
        found = self.__find_element()
        if self.formatted:
            self.selector = self._selector
            self.formatted = False
        return found

    def fmt(self, **kwargs):
        """
        :Description: Used to format selectors.
        :return: Element
        """
        self.selector = self.selector.format(**kwargs)
        self.formatted = True
        return self

    def click(self):
        """
        :Description: Execute a click on the given element.
        :return: Element, None
        """
        found = self.get()
        if found:
            self.controller.js.click(found)
            return self
        return None

    def scroll_to(self):
        """
        :Description: Scroll to the given element.
        :return: Element, None
        """
        found = self.get()
        if found:
            self.controller.js.scroll_into_view(found)
            return self
        return None

    def trigger_event(self, event, event_type=None, options=None):
        """
        :Description: Dispatch event to given element.
        :param event: Name of event to dispatch.
        :type event: string
        :param event_type: Type of the event to dispatch.
        :type event_type: string
        :param options: Options for event to dispatch.
        :type options: dict
        :return: Element, None
        """
        found = self.get()
        if found:
            self.controller.js.trigger_event(found, event, event_type, options)
            return self
        return None

    def send_input(self, input, force=False):
        """
        :Description: Send input to element.
        :param input: Input to send to given element.
        :type input: string
        :param force: Use for elements without an focus event handler.
        :type force: bool
        :return: Element, none
        """
        found = self.get()
        if found:
            if force:
                self.controller.js.set_property(found, 'innerText', input)
            else:
                found.send_keys(input)
            return self
        return None

    def wait_for(self, timeout, error=None):
        """
        :Description: Wait for a given element to become available.
        :param timeout: Time in seconds to wait for element.
        :type timeout: int
        :param error: Error message, if passed will raise NoSuchElementException.
        :type error: string, bool
        :return: Element, None
        """
        if not self.controller.wait(timeout=timeout, condition=self.check.available):
            if error:
                raise NoSuchElementException(error if isinstance(error, string_types) else \
                    'Element by selector "{}" not found'.format(self.selector))
            else:
                return None

        return self

    def wait_visible(self, timeout, error=None):
        """
        :Description: Wait for given element to become visible.
        :param timeout: Time in seconds to wait for element.
        :type timeout: int
        :param error: Error message, if passed will raise a ElementNotVisibleException.
        :type error: string, bool
        :return: Element, None
        """
        if not self.controller.wait(timeout=timeout, condition=self.check.visible):
            if error:
                raise ElementNotVisibleException(error if isinstance(error, string_types) else \
                    'Element by selector "{}" not found or is not visible'.format(self.selector))
            else:
                return None

        return self

    meta = {
        'required_fields': (
            ('controller', Controller),
            ('selector', string_types)
        )
    }


class Check(Resource):
    """
    :Description: Base resource for individual element checks.
    :param element: Element instance to reference.
    :type element: Element
    """
    def __init__(self, element):
        self.element = element
        self.validate()

    def available(self):
        """
        :Description: Get element availability.
        :return: bool
        """
        return bool(self.element.get())

    def visible(self):
        """
        :Description: Get element visibility.
        :return: bool
        """
        found = self.element.get()
        return found and \
            self.element.controller.js.is_visible(found)

    meta = {'required_fields': (('element', Element))}


class Elements(Resource):
    """
    :Description: Base resource for component elements.
    :param controller: Parent controller reference.
    :type controller: Controller
    :param selector: Selector of given elements.
    :type selector: string
    """
    def __init__(self, controller, selector):
        self.controller = controller
        self.type = 'xpath' if '/' in selector else 'css_selector'
        self.selector = self._selector = selector
        self.formatted = False
        self.checks = Checks(self)
        self.validate()

    def __find_elements(self, **kwargs):
        getattr(self.controller.webdriver, 'find_elements_by_{type}'.format(
            type=self.type))(kwargs.get('selector', self.selector))

    def get(self):
        """
        :Description: Used to fetch a selenium WebElement.
        :return: WebElement, None
        """
        found = self.__find_elements()
        if self.formatted:
            self.selector = self._selector # reset formatted selector
            self.formatted = False
        return found

    def fmt(self, **kwargs):
        """
        :Description: Used to format selectors.
        :return: Elements
        """
        self.selector = self.selector.format(**kwargs)
        return self

    def count(self):
        """
        :Description: Used to count number of found elements.
        :return: int
        """
        return len(self.get())

    def wait_for(self, timeout, length, strict=False, error=None):
        """
        :Description: Wait for given length of elements to be available.
        :param timeout: Time in seconds to wait for elements.
        :type timeout: int
        :param length: Number of elements to wait for.
        :type length: int
        :param strict: Expect exactly the length of elements, no more.
        :type strict: bool
        :param error: Error message, if passed will raise NoSuchElementException.
        :type error: string
        :return: Elements
        """
        if not self.controller.wait(timeout=timeout, condition=lambda: self.count() == length if \
            strict else self.count() >= length):
            if error:
                raise NoSuchElementException(error if isinstance(error, string_types) else \
                    '{} elements by selector "{}" not found'.format(length, self.selector))

        return self


    def wait_visible(self, timeout, length, strict=False, error=None):
        """
        :Description: Wait for given length of elements to be available and visible.
        :param timeout: Time in seconds to wait for elements.
        :type timeout: int
        :param length: Number of elements to wait for.
        :type length: int
        :param strict: Expect exactly the length of elements, no more.
        :type strict: bool
        :param error: Error message, if passed will raise ElementNotVisibleException.
        :type error: string
        :return: Elements
        """
        self.wait_for(timeout, length, strict, error)
        if not self.checks.visible():
            if error:
                raise ElementNotVisibleException(error if isinstance(error, string_types) else \
                    '{} elements by selector "{}" not visible'.format(length, self.selector))

        return self


    meta = {
        'required_fields': (
            ('controller', Controller),
            ('selector', string_types)
        )
    }


class Checks(Resource):
    """
    :Description: Base resource for multiple element checks.
    :param elements: Elements instance to reference.
    :type element: Elements
    """
    def __init__(self, elements):
        self.elements = elements
        self.validate()

    def visible(self):
        """
        :Description: Used to check at least one element is available and all visible.
        :return: bool
        """
        found = self.elements.get()
        if len(found):  #pylint: disable=len-as-condition
            return False
        else:
            for element in found:
                if not self.elements.controller.js.is_visible(element):
                    return False
        return True

    meta = {'required_fields': (('elements', Elements))}


def component_element(ref):
    """
    :Description: Wrapper for singular component element.
    :return: Element
    """
    @property
    def wrapper(self):  #pylint: disable=missing-docstring
        return Element(self.controller, ref(self))
    return wrapper


def component_elements(ref):
    """
    :Description: Wrapper for multiple component element.
    :return: Elements
    """
    @property
    def wrapper(self):  #pylint: disable=missing-docstring
        return Elements(self.controller, ref(self))
    return wrapper
