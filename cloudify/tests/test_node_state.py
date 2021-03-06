########
# Copyright (c) 2013 GigaSpaces Technologies Ltd. All rights reserved
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
#    * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    * See the License for the specific language governing permissions and
#    * limitations under the License.

__author__ = 'idanmo'


import unittest
from cloudify.manager import NodeState


class NodeStateTest(unittest.TestCase):

    def test_put_get(self):
        node = NodeState('id', {})
        node['key'] = 'value'
        self.assertEqual('value', node['key'])
        props = node.runtime_properties
        self.assertEqual(1, len(props))
        self.assertEqual('value', props['key'])

    def test_no_updates_to_empty_node(self):
        node = NodeState('id')
        self.assertEqual(0, len(node.runtime_properties))

    def test_put_new_property(self):
        node = NodeState('id')
        node.put('key', 'value')
        self.assertEqual('value', node.get('key'))
        props = node.runtime_properties
        self.assertEqual(1, len(props))
        self.assertEqual('value', props['key'])

    def test_put_several_properties(self):
        node = NodeState('id', {'key0': 'value0'})
        node.put('key1', 'value1')
        node.put('key2', 'value2')
        props = node.runtime_properties
        self.assertEqual(3, len(props))
        self.assertEqual('value0', props['key0'])
        self.assertEqual('value1', props['key1'])
        self.assertEqual('value2', props['key2'])

    def test_update_property(self):
        node = NodeState('id')
        node.put('key', 'value')
        self.assertEqual('value', node.get('key'))
        props = node.runtime_properties
        self.assertEqual(1, len(props))
        self.assertEqual('value', props['key'])

    def test_put_new_property_twice(self):
        node = NodeState('id')
        node.put('key', 'value')
        node.put('key', 'v')
        self.assertEqual('v', node.get('key'))
        props = node.runtime_properties
        self.assertEqual(1, len(props))
        self.assertEqual('v', props['key'])
