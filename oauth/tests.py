from django.test import TestCase

from .OAuth import OAuthInitDetails
from .OAuth import StaticStateProvider
from .OAuth import AccountantScope, AdminScope, IamScope

# Create your tests here.


class OAuthInitDetailsTests(TestCase):

    def test_init_details_to_url(self):
        state_provider = StaticStateProvider('fake-state')
        auth_server_url = 'https://fake-auth.com/oauth'
        client_id = 123
        redirect_uri = 'https://fake-redir.com/callback'
        scopes = [AccountantScope(), AdminScope(), IamScope()]

        details = OAuthInitDetails(auth_server_url, client_id, redirect_uri, scopes, state_provider)

        expected_url = ''.join((
            'https://fake-auth.com/oauth?',
            'response_type=code',
            '&client_id=123',
            '&scope=accountant+admin+iam',
            '&redirect_uri=https%3A%2F%2Ffake-redir.com%2Fcallback',
            '&state=fake-state',
        ))

        self.assertEqual(details.to_url(), expected_url, 'correctly generate request auth url')

