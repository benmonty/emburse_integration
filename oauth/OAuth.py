from typing import List
from furl import furl
from abc import ABC, abstractmethod
from uuid import uuid1


REQUEST_AUTH_RESPONSE_TYPE = "code"


class StateProvider(ABC):

    @abstractmethod
    def get(self):
        pass


class StaticStateProvider(StateProvider):

    def __init__(self, state):
        self._state: str = state

    def get(self):
        return self._state


class RandomStateProvider(StateProvider):

    def __init__(self):
        self._state: str = uuid1()

    def get(self):
        return self._state


class Scope():
    @abstractmethod
    def to_string(self):
        pass


class AccountantScope(Scope):
    def to_string(self):
        return 'accountant'


class AdminScope(Scope):
    def to_string(self):
        return 'admin'


class IamScope(Scope):
    def to_string(self):
        return 'iam'


class OAuthInitDetails:

    def __init__(self, auth_server_url, client_id, redirect_uri, scopes, state_provider: StateProvider):
        self._auth_server_url: furl = furl(auth_server_url)
        self._response_type: str = REQUEST_AUTH_RESPONSE_TYPE
        self._client_id: str = client_id
        self._scopes: List[Scope] = scopes
        self._redirect_uri: furl = furl(redirect_uri)
        self._state: str = state_provider.get()

    def _scope_value(self):
        scopes = map(lambda s: s.to_string(), self._scopes)
        uniq_scopes = sorted(list(set(scopes)))
        return ' '.join(uniq_scopes)

    def to_url(self) -> str:
        url = self._auth_server_url.copy()
        url.args['response_type'] = self._response_type
        url.args['client_id'] = self._client_id
        url.args['scope'] = self._scope_value()
        url.args['redirect_uri'] = self._redirect_uri.url
        url.args['state'] = self._state
        return url.url

