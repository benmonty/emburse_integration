from typing import Union, NewType
import os
import requests
from furl import furl

OauthCode = NewType('OauthCode', str)
AppClientId = NewType('AppClientId', str)
AppClientSecret = NewType('AppClientId', str)
AccessToken = NewType('AccessToken', str)
CompanyId = NewType('CompanyId', str)
TokenCreateError = NewType('TokenCreateError', str)


class CreateTokenReq:

    def __init__(self, code: OauthCode, client_id: AppClientId, client_secret: AppClientSecret, redirect_uri: furl):
        self._grant_type = 'authorization_code'
        self._code = code
        self._client_id = client_id
        self._client_secret = client_secret
        self._redirect_uri = redirect_uri

    def as_params(self):
        return {
            'grant_type': self._grant_type,
            'code': self._code,
            'client_id': self._client_id,
            'client_secret': self._client_secret,
            'redirect_uri': self._redirect_uri.url,
        }


class EmburseApi:

    def __init__(self):
        pass

    def api_url(self):
        return os.environ.get('EMBURSE_API_URL')

    def oauth_init_url(self):
        return os.environ.get('OAUTH_SERVER_INIT_AUTH_URL')

    def oauth_token_create_url(self):
        return os.environ.get('OAUTH_SERVER_TOKEN_CREATE_URL')

    def app_client_id(self):
        return AppClientId(os.environ.get('OAUTH_CLIENT_ID'))

    def app_client_secret(self):
        return AppClientSecret(os.environ.get('OAUTH_CLIENT_SECRET'))

    def create_token(self, redirect_uri:furl, code) -> AccessToken:
        req = CreateTokenReq(code, self.app_client_id(), self.app_client_secret(), redirect_uri)
        r = requests.post(self.oauth_token_create_url(), json=req.as_params())
        if r.status_code == 201:
            return AccessToken(r.json()['access_token'])
        else:
            r.raise_for_status()

    def revoke_token(self, to_revoke: Union[AccessToken, CompanyId]):
        pass

    def request(self, access_token, http_method, path, query_string):
        url = self.api_url + path + '?' + query_string
        auth_value = 'Bearer ' + access_token
        headers = {'Authorization': auth_value}

        r = requests.request(http_method, url, headers=headers)


        return r.json()
