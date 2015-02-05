#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import logging
import random

import httpretty
import pytest

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

# For integration tests with novaclient
import novaclient
from novaclient import shell
from novaclient import auth_plugin

import rackspace_auth_openstack.plugin

class TestNovaclientIntegration(object):
    '''Integration test with python-novaclient'''

    @httpretty.activate
    def test_shell(self):
        '''Test to make sure this plugin integrates with novaclient'''

        fake_tenant_id = "123456"
        fake_token = format(random.randint(0,2**(32*4)), 'x')

        import os
        shell.os.environ.update({
                "OS_USERNAME": "mockuser",
                "OS_TENANT_NAME": "mock_id",
                "OS_AUTH_URL": "https://identity.api.rackspacecloud.com/v2.0/",
                "OS_PASSWORD": "c0ffee"
        })

        def identity_callback(request, uri, headers):
            '''
            This callback mocks the identity response with total success
            '''
            identity_response_dict = {
                "access":
                    # Randomly pick a token for authentication
                    {'token': {'id': fake_token,
                               'RAX-AUTH:authenticatedBy': ['APIKEY'],
                               'expires': '2014-01-08T18:07:22.007Z',
                               'tenant': {'id': fake_tenant_id, 'name': fake_tenant_id}},

                    "serviceCatalog": [
                                        {u'endpoints': [{u'publicURL':
                                            u'https://dfw.mock.api.rackspacecloud.com/v2/' + fake_tenant_id,
                                           u'region': u'DFW',
                                           u'tenantId': fake_tenant_id,
                                           u'versionId': u'2',
                                           u'versionInfo': u'https://dfw.mock.api.rackspacecloud.com/v2',
                                           u'versionList': u'https://dfw.mock.api.rackspacecloud.com/'},
                                             ],
                                         u'name': u'mockCompute',
                                         u'type': u'compute'},
                    ],

                    # Data not being used for these little tests
                    "user": {}
                }
            }

            identity_response = json.dumps(identity_response_dict)

            return (200, headers, identity_response)

        httpretty.register_uri(httpretty.POST,
                   "https://identity.api.rackspacecloud.com/v2.0/tokens",
                   body=identity_callback,
                   content_type="application/json")

        oscs = shell.OpenStackComputeShell()
        oscs.main(["endpoints"])

class TestPlugin(object):

    @httpretty.activate
    def test_entry_points(self):
        from rackspace_auth_openstack import plugin

        plugin.auth_url_us
        plugin.auth_url_uk
        plugin._authenticate
        plugin.authenticate_us
        plugin.authenticate_uk


    @httpretty.activate
    def test_endpoints(self):
        us_auth = "https://identity.api.rackspacecloud.com/v2.0/"
        uk_auth = "https://lon.identity.api.rackspacecloud.com/v2.0/"

        assert rackspace_auth_openstack.plugin.auth_url_us() == us_auth
        assert rackspace_auth_openstack.plugin.auth_url_uk() == uk_auth

    @httpretty.activate
    def test_plugin(self):

        # Discover auth plugins
        auth_plugin.discover_auth_systems()

        # Make sure rackspace auth was found
        assert 'rackspace' in auth_plugin._discovered_plugins

        # Get a copy
        rackspace_auth_plugin = auth_plugin.load_plugin('rackspace')

        # Make sure the fallback didn't occur
        assert not isinstance(rackspace_auth_plugin, auth_plugin.DeprecatedAuthPlugin)

    def test_authenticate(self):

        def make_dummy(expected_auth):
            class dummy(object):
                user = "dummy"
                password = "filler"

                def _authenticate(cls, auth_url, body):
                    assert auth_url == expected_auth

                    # Strict enforcement for tests in case additional changes
                    # are made to the format without updating tests
                    assert body.keys() == ["auth"]

                    auth_keys = body["auth"].keys()
                    assert auth_keys == ["RAX-KSKEY:apiKeyCredentials"]

                    rax_cred_keys = body["auth"]["RAX-KSKEY:apiKeyCredentials"]
                    assert set(rax_cred_keys) == set(["username", "apiKey"])

            return dummy

        dummy_us = make_dummy("https://identity.api.rackspacecloud.com/v2.0/")
        dummy_uk = make_dummy("https://lon.identity.api.rackspacecloud.com/v2.0/")

        rackspace_auth_openstack.plugin.authenticate_us(dummy_us())
        rackspace_auth_openstack.plugin.authenticate_uk(dummy_uk())




