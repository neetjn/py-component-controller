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

from string import Template
from types import MethodType
from selenium.common.exceptions import NoSuchElementException, ElementNotVisibleException, \
    InvalidSelectorException, InvalidElementStateException
from six import string_types, iteritems

from pyscc.controller import Controller
from pyscc.resource import Resource


# pylint: disable=too-many-public-methods
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
        self.selector = self._selector = selector
        self.check = Check(self)
        self.wait_handle = None  # used for js waits
        self.validate()

    def __enter__(self):
        return self

    def __exit__(self, _type, value, traceback):
        return True

    def __find_element(self):
        expected_exceptions = (NoSuchElementException, InvalidSelectorException)
        try:
            return self.controller.browser.find_element_by_css_selector(self.selector)
        except expected_exceptions:
            try:
                return self.controller.browser.find_element_by_xpath(self.selector)
            except expected_exceptions:
                return None

    def fmt(self, **kwargs):
        """
        :Description: Used to format selectors.
        :return: Element
        """
        self.selector = Template(self._selector).safe_substitute(**kwargs)
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
        return self.controller.js.get_value(self.get())

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
            self.controller.js.scroll_into_view(found)
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
            self.controller.js.scroll_into_view(found)
            self.controller.js.dbl_click(found)
            return self
        return None

    def mouseup(self):
        """
        :Description: Dispatches a mouseup event on the given element.
        :return: Element, None
        """
        # ignoring from coverage, assume covered by trigger_event test
        found = self.get()
        if found:
            self.controller.js.scroll_into_view(found)
            return self.trigger_event('mouseup', 'MouseEvent') # pragma: no cover
        return None

    def mousedown(self):
        """
        :Description: Dispatches a mousedown event on the given element.
        :return: Element, None
        """
        # ignoring from coverage, assume covered by trigger_event test
        found = self.get()
        if found:
            self.controller.js.scroll_into_view(found)
            return self.trigger_event('mousedown', 'MouseEvent') # pragma: no cover
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

    def send_input(self, value, force=False, clear=True):
        """
        :Description: Send input to element.
        :param value: Input to send to given element.
        :type value: string
        :param force: Use for elements without an focus event handler.
        :type force: bool
        :param clear_field: Clear the element's input text prior to sending input.
        :type clear_field: bool
        :return: Element, none
        """
        found = self.get()
        if found:
            if force:
                self.controller.js.set_property(
                    found, 'innerHTML',
                    value if clear else self.controller.js.get_raw_text(found) + value)
            else:
                if clear:
                    found.clear()
                found.send_keys(value)
            return self
        return None

    def wait_for(self, timeout, available=True, error=None):
        """
        :Description: Wait for a given element to become available.
        :param timeout: Time in seconds to wait for element.
        :type timeout: int
        :available: Used to check whether element is available or not available.
        :type available: bool
        :param error: Error message, if passed will raise NoSuchElementException.
        :type error: string, bool
        :return: Element, None
        """
        if not self.controller.wait(timeout=timeout, condition=self.check.available \
            if available else self.check.not_available):

            if error:
                raise NoSuchElementException(error if isinstance(error, string_types) else \
                    'Element by selector "{}" was {}'\
                    .format(self.selector, 'not found' if available else 'found'))
            return None

        return self

    def wait_visible(self, timeout, error=None):
        """
        :Description: Wait for given element to be visible.
        :param timeout: Time in seconds to wait for element.
        :type timeout: int
        :param error: Raise ElementNotVisibleException on failure.
        :type error: bool, string
        :return: Element, None
        """
        if not self.controller.wait(timeout=timeout, condition=self.check.visible):
            if error:
                raise ElementNotVisibleException(error if isinstance(error, string_types) else \
                    'Element by selector "{}" not found or is not visible'.format(self.selector))
            return None

        return self

    def wait_invisible(self, timeout, error=None):
        """
        :Description: Wait for given element to be invisible.
        :param timeout: Time in seconds to wait for element.
        :type timeout: int
        :param error: Raise InvalidElementStateException on failure.
        :type error: bool, string
        :return: Element, None
        """
        if not self.controller.wait(timeout=timeout, condition=self.check.invisible):
            if error:
                raise InvalidElementStateException(error if isinstance(error, string_types) else \
                    'Element by selector "{}" not found or is visible'.format(self.selector))
            return None

        return self

    def wait_enabled(self, timeout, error=None):
        """
        :Description: Wait for given element to be enabled.
        :param timeout: Time in seconds to wait for element.
        :type timeout: int
        :param error: Raise InvalidElementStateException on failure.
        :type error: bool, string
        :return: Element, None
        """
        if not self.controller.wait(timeout=timeout, condition=self.check.enabled):
            if error:
                raise InvalidElementStateException(error if isinstance(error, string_types) else \
                    'Element by selector "{}" not found or is disabled'.format(self.selector))
            return None

        return self

    def wait_disabled(self, timeout, error=None):
        """
        :Description: Wait for given element to be disabled.
        :param timeout: Time in seconds to wait for element.
        :type timeout: int
        :param error: Raise InvalidElementStateException on failure.
        :type error: bool, string
        :return: Element, None
        """
        if not self.controller.wait(timeout=timeout, condition=self.check.disabled):
            if error:
                raise InvalidElementStateException(error if isinstance(error, string_types) else \
                    'Element by selector "{}" not found or is enabled'.format(self.selector))
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
        self.selector = self._selector = selector
        self.checks = Checks(self)
        self.validate()

    def __enter__(self):
        return self

    def __exit__(self, _type, value, traceback):
        return True

    def __find_elements(self):
        return self.controller.browser.find_elements_by_css_selector(self.selector) \
            or self.controller.browser.find_elements_by_xpath(self.selector)

    def fmt(self, **kwargs):
        """
        :Description: Used to format selectors.
        :return: Elements
        """
        self.selector = Template(self._selector).safe_substitute(**kwargs)
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
        return []

    def value(self):
        """
        :Description: Get list of input element values.
        :return: [string, ...], None
        """
        return [self.controller.js.get_value(element) for element in self.get()]

    def get_attribute(self, attribute):
        """
        :Description: Used to fetch list of elements attributes.
        :param attribute: Attribute of elements to target.
        :type attribute: string
        :return: [(None, bool, int, float, string), ...]
        """
        return [self.controller.js.get_attribute(element, attribute) for element in self.get()]

    def set_attribute(self, attribute, value):
        """
        :Description: Used to set specified element attribute.
        :param attribute: Attribute of element to target.
        :type attribute: string
        :param value: Value to set elements attributes to.
        :type value: None, bool, int, float, string
        :return: Element, None
        """
        for element in self.get():
            self.controller.js.set_attribute(element, attribute, value)
        return self

    def get_property(self, prop):
        """
        :Description: Used to fetch list of elements properties.
        :param prop: Property of elements to target.
        :type prop: string
        :return: None, bool, int, float, string
        """
        return [self.controller.js.get_property(element, prop) for element in self.get()]

    def set_property(self, prop, value):
        """
        :Description: Used to set specified element property.
        :param prop: Property of element to target.
        :type prop: string
        :param value: Value to set specified element property to.
        :type value: None, bool, int, float, string
        :return: Element, None
        """
        for element in self.get():
            self.controller.js.set_property(element, prop, value)
        return self

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
                if isinstance(error, string_types):
                    msg = Template(error).safe_substitute(expected=length, found=self.count())
                else:
                    msg = '"{}" elements by selector "{}" found, expected "{}"'\
                          .format(self.count(), self.selector, length)
                raise NoSuchElementException(msg)
            else:
                return None

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
        def check():
            # pylint: disable=line-too-long
            return self.count() == length if strict else self.count() >= length and self.checks.visible()

        if not self.controller.wait(timeout=timeout, condition=check):
            if error:
                raise ElementNotVisibleException(error if isinstance(error, string_types) else \
                    '{} elements by selector "{}" not visible'.format(length, self.selector))

        return self

    def wait_invisible(self, timeout, length=1, strict=False, error=None):
        """
        :Description: Wait for given length of elements to be available and invisible.
        :param timeout: Time in seconds to wait for elements.
        :type timeout: int
        :param length: Number of elements to wait for.
        :type length: int
        :param strict: Expect exactly the length of elements, no more.
        :type strict: bool
        :param error: Raise InvalidElementStateException on failure.
        :type error: bool, string
        :return: Elements
        """
        def check():
            # pylint: disable=line-too-long
            return self.count() == length if strict else self.count() >= length and self.checks.invisible()

        if not self.controller.wait(timeout=timeout, condition=check):
            if error:
                raise InvalidElementStateException(error if isinstance(error, string_types) else \
                    '{} elements by selector "{}" not invisible'.format(length, self.selector))

        return self

    def wait_enabled(self, timeout, length=1, strict=False, error=None):
        """
        :Description: Wait for given length of elements to be available and enabled.
        :param timeout: Time in seconds to wait for elements.
        :type timeout: int
        :param length: Number of elements to wait for.
        :type length: int
        :param strict: Expect exactly the length of elements, no more.
        :type strict: bool
        :param error: Raise InvalidElementStateException on failure.
        :type error: bool, string
        :return: Elements
        """
        def check():
            # pylint: disable=line-too-long
            return self.count() == length if strict else self.count() >= length and self.checks.enabled()

        if not self.controller.wait(timeout=timeout, condition=check):
            if error:
                raise InvalidElementStateException(error if isinstance(error, string_types) else \
                    '{} elements by selector "{}" not enabled'.format(length, self.selector))

        return self

    def wait_disabled(self, timeout, length=1, strict=False, error=None):
        """
        :Description: Wait for given length of elements to be available and disabled.
        :param timeout: Time in seconds to wait for elements.
        :type timeout: int
        :param length: Number of elements to wait for.
        :type length: int
        :param strict: Expect exactly the length of elements, no more.
        :type strict: bool
        :param error: Raise InvalidElementStateException on failure.
        :type error: bool, string
        :return: Elements
        """
        def check():
            # pylint: disable=line-too-long
            return self.count() == length if strict else self.count() >= length and self.checks.disabled()

        if not self.controller.wait(timeout=timeout, condition=check):
            if error:
                raise InvalidElementStateException(error if isinstance(error, string_types) else \
                    '{} elements by selector "{}" not disabled'.format(length, self.selector))

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

    def enabled(self):
        """
        :Description: Check element DOM node enabled.
        :return: bool
        """
        found = self.element.get()
        return found and \
            not self.element.controller.js.get_property(found, 'disabled')

    def disabled(self):
        """
        :Description: Check element DOM node disabled.
        :return: bool
        """
        found = self.element.get()
        return found and \
            self.element.controller.js.get_property(found, 'disabled')

    def wait_status(self):
        """
        :Description: Check javascript wait status.
        """
        return self.element.controller.js.wait_status(self.element.wait_handle)

    meta = {'required_fields': [('element', Element)]}


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
        :Description: Used to check at least one element is available and all are visible.
        :return: bool
        """
        found = self.elements.get()
        if not len(found):  # pylint: disable=len-as-condition
            return False
        for element in found:
            if not self.elements.controller.js.is_visible(element):
                return False
        return True

    def invisible(self):
        """
        :Description: Used to check at least one element is available and all are invisible.
        :return: bool
        """
        found = self.elements.get()
        if not len(found):  # pylint: disable=len-as-condition
            return False
        for element in found:
            if self.elements.controller.js.is_visible(element):
                return False
        return True

    def enabled(self):
        """
        :Description: Used to check at least one element is available and all are enabled.
        :return: bool
        """
        found = self.elements.get()
        if not len(found):  # pylint: disable=len-as-condition
            return False
        for element in found:
            if self.elements.controller.js.get_property(element, 'disabled'):
                return False
        return True

    def disabled(self):
        """
        :Description: Used to check at least one element is available and all are disabled.
        :return: bool
        """
        found = self.elements.get()
        if not len(found):  # pylint: disable=len-as-condition
            return False
        for element in found:
            if not self.elements.controller.js.get_property(element, 'disabled'):
                return False
        return True

    meta = {'required_fields': [('elements', Elements)]}


class CheckGroup(Resource):
    """
    :Description: Base resource for component group element checks.
    :param group: Group resource to reference.
    :type group: Resource
    """
    def __init__(self, group):
        self.group = group
        self.validate()

    def __enter__(self):
        return self

    def __exit__(self, _type, value, traceback):
        return True

    def available(self):
        """
        :Description: Check group of elements available.
        :return: bool
        """
        for element in self.group.__group__:
            if not getattr(self.group, element).check.available():
                return False
        return True

    def not_available(self):
        """
        :Description: Check group of elements not available.
        :return: bool
        """
        for element in self.group.__group__:
            if not getattr(self.group, element).check.not_available():
                return False
        return True

    def visible(self):
        """
        :Description: Check group of elements visible.
        :return: bool
        """
        for element in self.group.__group__:
            if not getattr(self.group, element).check.visible():
                return False
        return True

    def invisible(self):
        """
        :Description: Check group of elements invisible.
        :return: bool
        """
        for element in self.group.__group__:
            if not getattr(self.group, element).check.invisible():
                return False
        return True

    def enabled(self):
        """
        :Description: Check group elements enabled.
        :return: bool
        """
        for element in self.__group__:
            if not getattr(self.group, element).check.enabled():
                return False
        return True

    def disabled(self):
        """
        :Description: Check group elements disabled.
        :return: bool
        """
        for element in self.__group__:
            if not getattr(self.group, element).check.disabled():
                return False
        return True

    meta = {'required_fields': [('group', Resource)]}


def component_element(ref):
    """
    :Description: Wrapper for singular component element.
    :return: Element
    """
    @property
    def wrapper(self):  # pylint: disable=missing-docstring
        return Element(self.controller, ref(self))
    return wrapper


def component_elements(ref):
    """
    :Description: Wrapper for multiple component element.
    :return: Elements
    """
    @property
    def wrapper(self):  # pylint: disable=missing-docstring
        return Elements(self.controller, ref(self))
    return wrapper


def component_group(ref):
    """
    :Description: Wrapper for component element groups.
    :return: Resource
    """
    def fmt(self, **kwargs): # pylint: disable=missing-docstring
        # pylint: disable=C0103, W0212
        for element in self.__group__:
            el = getattr(self, element)
            el._selector = Template(el._selector).safe_substitute(**kwargs)
            el.selector = el._selector
        return self

    @property
    def wrapper(self): # pylint: disable=missing-docstring
        group_def = ref(self)
        # pylint: disable=line-too-long
        group = Resource(**{element: Element(self.controller, (group_def.get('_') + ' ' + selector) if \
            group_def.get('_') else selector) for element, selector in iteritems(group_def) \
            if selector != '_'})
        group.__group__ = [element for element, _ in iteritems(group_def) if element != '_']
        group.fmt = MethodType(fmt, group)
        group.check = CheckGroup(group)
        # pylint: disable=no-value-for-parameter
        group.find = lambda x: getattr(group, x)
        return group

    return wrapper
