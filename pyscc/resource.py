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

class Resource(object):
    """
    :Description: Base object for shenanigans.
    """
    def __init__(self, **kwargs):
        for prop, val in kwargs.items():
            setattr(self, prop, val)
        self.validate()

    def validate(self):
        """
        :Description: Validate resource with defined meta data.
        """
        meta = getattr(self, 'meta', None)
        # TODO: Add type checking
        if meta and meta.get('required_fields'):
            required_fields = meta.get('required_fields')
            if not any(getattr(self, field) is None for field in required_fields):
                raise AttributeError(
                    'Required fields "{}" were not available'.format(required_fields))
