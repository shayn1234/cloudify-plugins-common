########
# Copyright (c) 2014 GigaSpaces Technologies Ltd. All rights reserved
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

import urllib2
import os

from cosmo_manager_rest_client.cosmo_manager_rest_client \
    import CosmoManagerRestClient

from cloudify.exceptions import HttpException
import utils


class NodeState(object):
    """Represents a deployment node state.
    An instance of this class contains runtime information retrieved
    from Cloudify's runtime storage.
    Its API allows to set and get properties of the node's state,
     generate an updates dict to be used when requesting to save changes
     back to the storage (in an optimistic locking manner).
    """
    def __init__(self, node_id, runtime_properties=None, state_version=None):
        self.id = node_id
        self._runtime_properties = \
            DirtyTrackingDict((runtime_properties or {}).copy())
        self._state_version = state_version

    def get(self, key):
        return self._runtime_properties.get(key)

    def put(self, key, value):
        self._runtime_properties[key] = value

    __setitem__ = put

    __getitem__ = get

    def __contains__(self, key):
        return key in self._runtime_properties

    @property
    def runtime_properties(self):
        return self._runtime_properties

    @property
    def state_version(self):
        return self._state_version

    @property
    def dirty(self):
        return self._runtime_properties.dirty


def get_manager_rest_client():
    return CosmoManagerRestClient(utils.get_manager_ip(),
                                  utils.get_manager_rest_service_port())


def _save_resource(logger, resource, resource_path, target_path):
    if not target_path:
        target_path = os.path.join(utils.create_temp_folder(),
                                   os.path.basename(resource_path))
    with open(target_path, 'w') as f:
        f.write(resource)
    logger.info("Downloaded %s to %s" % (resource_path, target_path))
    return target_path


def download_resource(resource_path, logger, target_path=None):
    resource = get_resource(resource_path)
    return _save_resource(logger, resource, resource_path, target_path)


def download_blueprint_resource(blueprint_id,
                                resource_path,
                                logger,
                                target_path=None):
    resource = get_blueprint_resource(blueprint_id, resource_path)
    return _save_resource(logger, resource, resource_path, target_path)


def get_resource(resource_path, base_url=None):
    if base_url is None:
        base_url = utils.get_manager_file_server_url()
    try:
        url = '{0}/{1}'.format(base_url, resource_path)
        response = urllib2.urlopen(url)
        return response.read()
    except urllib2.HTTPError as e:
        raise HttpException(e.url, e.code, e.msg)


def get_blueprint_resource(blueprint_id, resource_path):
    base_url = "{0}/{1}".format(utils
                                .get_manager_file_server_blueprints_root_url(),
                                blueprint_id)
    return get_resource(resource_path, base_url=base_url)


def get_node_state(node_id):
    client = get_manager_rest_client()
    node_state = client.get_node_state(node_id)
    if 'runtimeInfo' not in node_state:
        raise KeyError('runtimeInfo not found in get_node_state response')
    if 'stateVersion' not in node_state:
        raise KeyError('stateVersion not found in get_node_state response')
    return NodeState(
        node_id, node_state['runtimeInfo'], node_state['stateVersion'])


def update_node_state(node_state):
    client = get_manager_rest_client()
    client.update_node_state(node_state.id, node_state.runtime_properties,
                             node_state.state_version)


class DirtyTrackingDict(dict):

    def __init__(self, *args, **kwargs):
        super(DirtyTrackingDict, self).__init__(*args, **kwargs)
        self.dirty = False

    def __setitem__(self, key, value):
        super(DirtyTrackingDict, self).__setitem__(key, value)
        self.dirty = True
