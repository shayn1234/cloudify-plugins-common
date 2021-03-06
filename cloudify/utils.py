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
import random
import string
import tempfile

__author__ = 'idanmo'

import os

from cloudify.constants import LOCAL_IP_KEY, MANAGER_IP_KEY, \
    MANAGER_REST_PORT_KEY, MANAGER_FILE_SERVER_BLUEPRINTS_ROOT_URL_KEY, \
    MANAGER_FILE_SERVER_URL_KEY


def get_local_ip():
    return os.environ[LOCAL_IP_KEY]


def get_manager_ip():
    return os.environ[MANAGER_IP_KEY]


def get_manager_file_server_blueprints_root_url():
    return os.environ[MANAGER_FILE_SERVER_BLUEPRINTS_ROOT_URL_KEY]


def get_manager_file_server_url():
    return os.environ[MANAGER_FILE_SERVER_URL_KEY]


def get_manager_rest_service_port():
    return int(os.environ[MANAGER_REST_PORT_KEY])


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))


def create_temp_folder():
    path_join = os.path.join(tempfile.gettempdir(), id_generator(5))
    os.makedirs(path_join)
    return path_join


def get_cosmo_properties():
    return {
        "management_ip": get_manager_ip(),
        "ip": get_local_ip()
    }
