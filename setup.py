# Copyright 2011 OpenStack, LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import setuptools
import sys


def read_file(file_name):
    return open(os.path.join(os.path.dirname(__file__), file_name)).read()


setuptools.setup(
    name="rackspace-auth-neutronclientext",
    version="1.0",
    author="OpenStack",
    author_email="openstack-dev@lists.openstack.org",
    description="Rackspace Auth Plugin for OpenStack Neutron Clients.",
    long_description=read_file("README.rst"),
    license="Apache License, Version 2.0",
    url="https://github.com/rackerlabs/rackspace-auth-neutronclientext",
    install_requires=['python-neutronclient'],
    packages=setuptools.find_packages(exclude=['tests', 'tests.*', 'test_*']),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Environment :: OpenStack",
        "Programming Language :: Python"
    ],
    entry_points={
        "openstack.client.auth_url": [
            "rackspace_us = rackspace_auth_neutronclientext.plugin:auth_url_us",
            "rackspace_uk = rackspace_auth_neutronclientext.plugin:auth_url_uk",
            "rackspace = rackspace_auth_neutronclientext.plugin:auth_url_us"
        ],
        "openstack.client.authenticate": [
            "rackspace_us = rackspace_auth_neutronclientext.plugin:authenticate_us",
            "rackspace_uk = rackspace_auth_neutronclientext.plugin:authenticate_uk",
            "rackspace = rackspace_auth_neutronclientext.plugin:authenticate_us"
        ],
        "openstack.client.auth_plugin": [
            "rackspace = rackspace_auth_neutronclientext.plugin:RackspaceAuthPlugin"
        ]
    }
)
