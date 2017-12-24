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

from selenium.common.exceptions import NoSuchElementException, ElementNotVisibleException
from six import string_types, iteritems

from pyscc.controller import Controller
from pyscc.resource import Resource


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
        self.check = Check(self)
        self.wait_handle = None  # used for js waits
        self.validate()

    def __find_element(self, **kwargs):
        try:
            return getattr(self.controller.browser, 'find_element_by_{type}'.format(
                type=self.type))(kwargs.get('selector', self.selector))
        except NoSuchElementException:
            return None

    def fmt(self, **kwargs):
        """
        :Description: Used to format selectors.
        :return: Element
        """
        self.selector = self._selector.format(**kwargs)
        return self

    def get(self):
        """
        :Description: Used to fetch a selenium WebElement.
        :return: WebElement, None
        """
        return self.__find_element()

    def text(self, raw=False):
        """
        :Description: Get element text value.
        :param raw: Extract inner html from element.
        :type raw: bool
        :return: string
        """
        found = self.get()
        if found:
            return self.controller.js.get_raw_text(found) if raw else found.text
        return None

    def value(self):
        """
        :Description: Get input element value.
        :return: string
        """
        found = self.get()
        if found:
            return self.controller.js.get_value(found)
        return None

    def get_attribute(self, attribute):
        """
        :Description: Used to fetch specified element attribute.
        :Warning: This method does not check if element is available.
        :param attribute: Attribute of element to target.
        :type attribute: string
        :return: None, bool, int, float, string
        """
        return self.controller.js.get_attribute(self.get(), attribute)

    def set_attribute(self, attribute, value):
        """
        :Description: Used to set specified element attribute.
        :param attribute: Attribute of element to target.
        :type attribute: string
        :param value: Value to set specified element attribute to.
        :type value: None, bool, int, float, string
        :return: Element, None
        """
        found = self.get()
        if found:
            self.controller.js.set_attribute(found, attribute, value)
            return self
        return None

    def get_property(self, prop):
        """
        :Description: Used to fetch specified element property.
        :Warning: This method does not check if element is available.
        :param prop: Property of element to target.
        :type prop: string
        :return: None, bool, int, float, string
        """
        return self.controller.js.get_property(self.get(), prop)

    def set_property(self, prop, value):
        """
        :Description: Used to set specified element property.
        :param prop: Property of element to target.
        :type prop: string
        :param value: Value to set specified element property to.
        :type value: None, bool, int, float, string
        :return: Element, None
        """
        found = self.get()
        if found:
            self.controller.js.set_property(found, prop, value)
            return self
        return None

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

    def dbl_click(self):
        """
        :Description: Execute a double click on the given element.
        :return: Element, None
        """
        found = self.get()
        if found:
            self.controller.js.dbl_click(found)
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

    def send_input(self, value, force=False):
        """
        :Description: Send input to element.
        :param value: Input to send to given element.
        :type value: string
        :param force: Use for elements without an focus event handler.
        :type force: bool
        :return: Element, none
        """
        found = self.get()
        if found:
            if force:
                self.controller.js.set_property(found, 'innerHTML', value)
            else:
                found.send_keys(value)
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
        :param error: Raise NoSuchElementException on failure.
        :type error: bool, string
        :return: Element, None
        """
        if not self.controller.wait(timeout=timeout, condition=self.check.visible):
            if error:
                raise ElementNotVisibleException(error if isinstance(error, string_types) else \
                    'Element by selector "{}" not found or is not visible'.format(self.selector))
            else:
                return None

        return self

    def wait_invisible(self, timeout, error=None):
        """
        :Description: Wait for given element to become invisible.
        :param timeout: Time in seconds to wait for element.
        :type timeout: int
        :param error: Raise NoSuchElementException on failure.
        :type error: bool, string
        :return: Element, None
        """
        if not self.controller.wait(timeout=timeout, condition=self.check.invisible):
            if error:
                raise NoSuchElementException(error if isinstance(error, string_types) else \
                    'Element by selector "{}" not found or is visible'.format(self.selector))
            else:
                return None

        return self

    def wait_js(self, condition, interval):
        """
        :Description: Wait for element by javascript condition.
        :param condition: Javascript condition to execute.
        :type condition: string
        :param interval: Interval to check condition by in ms.
        :type interval: int
        :return: Element, None
        """
        self.wait_handle = self.controller.js.wait(condition, interval, self.selector)
        return self

    def switch_to(self):
        """
        :Description: Switch into an iframe element context.
        :return: Element, None
        """
        found = self.get()
        if found:
            self.controller.browser.switch_to.frame(found)
            return self
        return None

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
        :Description: Check element available.
        :return: bool
        """
        return bool(self.element.get())

    def not_available(self):
        """
        :Description: Check element not available.
        :return: bool
        """
        return not bool(self.element.get())

    def visible(self):
        """
        :Description: Check element visibility.
        :return: bool
        """
        found = self.element.get()
        return found and \
            self.element.controller.js.is_visible(found)

    def invisible(self):
        """
        :Description: Check element invisible.
        :return: bool
        """
        found = self.element.get()
        return found and \
            not self.element.controller.js.is_visible(found)

    def wait_status(self):
        """
        :Description: Check javascript wait status.
        """
        return self.element.controller.js.wait_status(self.element.wait_handle)

    meta = {'required_fields': [('element', Element)]}


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
        self.checks = Checks(self)
        self.validate()

    def __find_elements(self, **kwargs):
        return getattr(self.controller.browser, 'find_elements_by_{type}'.format(
            type=self.type))(kwargs.get('selector', self.selector))

    def fmt(self, **kwargs):
        """
        :Description: Used to format selectors.
        :return: Elements
        """
        self.selector = self._selector.format(**kwargs)
        return self

    def get(self):
        """
        :Description: Used to fetch a selenium WebElement.
        :return: [WebElement, ...], None
        """
        return self.__find_elements()

    def count(self):
        """
        :Description: Used to count number of found elements.
        :return: int
        """
        return len(self.get())

    def text(self, raw=False):
        """
        :Description: Get list of element text values.
        :param raw: Extract inner html from element.
        :type raw: bool
        :return: [string, ...], None
        """
        found = self.get()
        if found:
            collection = []
            if raw:
                for element in found:
                    collection.append(self.controller.js.get_raw_text(element))
            else:
                for element in found:
                    collection.append(element.text)
            return collection
        return None

    def value(self):
        """
        :Description: Get list of input element values.
        :return: [string, ...], None
        """
        found = self.get()
        if found:
            return [self.controller.js.get_value(element) for element in found]
        return None

    def wait_for(self, timeout, length=1, strict=False, error=None):
        """
        :Description: Wait for given length of elements to be available.
        :param timeout: Time in seconds to wait for elements.
        :type timeout: int
        :param length: Number of elements to wait for.
        :type length: int
        :param strict: Expect exactly the length of elements, no more.
        :type strict: bool
        :param error: Raise NoSuchElementException on failure.
        :type error: bool, string
        :return: Elements
        """
        if not self.controller.wait(timeout=timeout, condition=lambda: self.count() == length if \
            strict else self.count() >= length):
            if error:
                raise NoSuchElementException(error if isinstance(error, string_types) else \
                    '{} elements by selector "{}" not found'.format(length, self.selector))

        return self

    def wait_visible(self, timeout, length=1, strict=False, error=None):
        """
        :Description: Wait for given length of elements to be available and visible.
        :param timeout: Time in seconds to wait for elements.
        :type timeout: int
        :param length: Number of elements to wait for.
        :type length: int
        :param strict: Expect exactly the length of elements, no more.
        :type strict: bool
        :param error: Raise ElementNotVisibleException on failure.
        :type error: bool, string
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
            for element in found:
                if not self.elements.controller.js.is_visible(element):
                    return False
        else:
            return False
        return True

    meta = {'required_fields': [('elements', Elements)]}


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

def component_group(ref):
    """
    :Description: Wrapper for component element groups.
    :return: Resource
    """
    @property
    def wrapper(self): #pylint: disable=missing-docstring
        return Resource(**{
            element: Element(self.controller, selector) \
                for element, selector in iteritems(ref(self))})
    return wrapper
