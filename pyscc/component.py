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
from pyscc.element import Element, Elements
from pyscc.resource import Resource


class Component(Resource): # pylint: disable=too-few-public-methods
    """
    Base resource for web components.

    :param controller: Parent controller reference.
    :type controller: Controller
    """
    def __init__(self, controller):
        self.controller = controller
        self.browser = controller.browser
        self.env = controller.env
        self.validate()

    @property
    def __describe__(self):
        """
        Fetch component description with attribute names for Element, Elements,
        and Component Group instances.

        :example: { 'element': [...], 'elements': [...], 'group': [...] }
        :return: dict
        """
        # pylint: disable=line-too-long
        expected_attributes = ['controller', 'browser', 'env', 'validate']
        base_attributes = [child for child in dir(self) if not child.startswith('_') and child not in expected_attributes]
        element_instances = [el for el in base_attributes if isinstance(getattr(self, el), Element)]
        elements_instances = [el for el in base_attributes if isinstance(getattr(self, el), Elements)]
        group_instances = [el for el in base_attributes if el not in element_instances + elements_instances and isinstance(getattr(self, el), Resource)]
        return {
            'element': element_instances,
            'elements': elements_instances,
            'group': group_instances
        }

    meta = {'required_fields': [('controller', Controller)]}
