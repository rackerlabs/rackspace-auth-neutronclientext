# Copyright 2012 Hewlett-Packard Development Company, L.P.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import json

import neutronclient.common.auth_plugin
from neutronclient.common import exceptions


class RackspaceAuthPlugin(neutronclient.common.auth_plugin.BaseAuthPlugin):
    '''The RackspaceAuthPlugin simply provides authenticate, no extra
    options.
    '''
    def authenticate(self, cls, auth_url):
        return _authenticate(cls, auth_url)

    def pre_hook(self, endpoint_url, url, method, **kwargs):
        '''Fixes the .../v2.0/v2.0/... bug.'''
        if endpoint_url.endswith(url[:5]):
            endpoint_url = endpoint_url[:-5]
        return endpoint_url, url, method, kwargs


def auth_url_us():
    """Return the Rackspace Cloud US Auth URL"""
    return "https://identity.api.rackspacecloud.com/v2.0/"


def auth_url_uk():
    """Return the Rackspace Cloud UK Auth URL"""
    return "https://lon.identity.api.rackspacecloud.com/v2.0/"


def auth_url_noauth():
    """Noauth by definition doesn't need an auth url"""
    return "noauth"


def _authenticate(cls, auth_url):
    """Authenticate against noauth or the Rackspace auth service."""
    if cls.auth_strategy == 'noauth':
        if not cls.endpoint_url:
            message = ('For "noauth" authentication strategy, the endpoint '
                       'must be specified either in the constructor or '
                       'using --os-url')
            raise exceptions.Unauthorized(message=message)
        else:
            return None
    if not auth_url:
        raise exceptions.NoAuthURLProvided()

    body = {"auth": {
            "RAX-KSKEY:apiKeyCredentials": {
                "username": cls.username,
                "apiKey": cls.password},
            }}
    token_url = cls.auth_url + "/tokens"

    resp, resp_body = cls._cs_request(token_url, "POST",
                                      body=json.dumps(body),
                                      content_type="application/json",
                                      allow_redirects=True)
    if resp_body:
        try:
            resp_body = json.loads(resp_body)
        except ValueError:
            pass
    else:
        resp_body = None
    return resp_body


def authenticate_noauth(cls,
                        auth_url=auth_url_noauth()):
    """Do not authenticate, but do ensure there is an endpoint_url"""
    return _authenticate(cls, auth_url)


def authenticate_us(cls,
                    auth_url=auth_url_us()):
    """Authenticate against the Rackspace US auth service."""
    return _authenticate(cls, auth_url)


def authenticate_uk(cls,
                    auth_url=auth_url_uk()):
    """Authenticate against the Rackspace UK auth service."""
    return _authenticate(cls, auth_url)
