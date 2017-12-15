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
from selenium.common.exceptions import NoSuchElementException
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
        self.check = Check(element)

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

    @property
    def click(self):
        """
        :Description: Execute a click on the given element.
        """
        found = self.get()
        if found:
            self.controller.js.click(found)
            return True
        return False

    @property
    def scroll_to(self):
        """
        :Description: Scroll to the given element.
        """
        found = self.get()
        if found:
            self.controller.js.scroll_into_view(found)
            return True
        return False

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

    def available(self):
        """
        :Description: Get element availability.
        """
        return bool(self.element.get())

    def visible(self):
        """
        :Description: Get element visibility.
        """
        found = self.element.get()
        return found and \
            self.element.controller.js.is_visible(found)

    meta = {'required_fields': (('element', Element))}


class Elements(Resource):
    """
    :Description: Base resource for component elements.
    """
    def __init__(self, controller, selector):
        self.controller = controller
        self.type = 'xpath' if '/' in selector else 'css_selector'
        self.selector = self._selector = selector
        self.formatted = False

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

    meta = {
        'required_fields': (
            ('controller', Controller),
            ('selector', string_types)
        )
    }


def element(ref):
    @property
    def wrapper(self):
        return Element(self.controller, ref(self))
    return wrapper


def elements(ref):
    @property
    def wrapper(self):
        return Elements(self.controller, ref(self))
    return wrapper
