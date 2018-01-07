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

from six import iteritems


class Resource(object): # pylint: disable=too-few-public-methods
    """
    :Description: Base object for shenanigans.
    """
    def __init__(self, **kwargs):
        for prop, val in iteritems(kwargs):
            setattr(self, prop, val)
        self.validate()

    def validate(self):
        """
        :Description: Validate resource with defined meta data.
        """
        meta = getattr(self, 'meta', None)
        if meta and meta.get('required_fields'):
            required_fields = meta.get('required_fields')
            for field in required_fields:
                if isinstance(field, (list, tuple)):
                    field, types = field
                    if not hasattr(self, field):
                        raise AttributeError('Resource missing required field "{}"'.format(field))
                    if not isinstance(getattr(self, field), types):
                        raise ValueError(
                            'Field "{}" is not of type "{}" as expected'.format(field, types))
                else:
                    if not hasattr(self, field):
                        raise AttributeError('Resource missing required field "{}"'.format(field))
