import os
from .EmburseApi import EmburseApi
from .OAuth import RandomStateProvider, OAuthInitDetails, PreAuthState, AuthState

# time is extremely limited here, so I'm just storing the oauth state in an in-mem map
# since it is not serializable and cannot be put in the session
# obvious bad practice
oauth_state_map = {}


def get_auth_state_for_user(user_id) -> AuthState:
    if user_id in oauth_state_map:
        return oauth_state_map.get(user_id)
    else:
        emburse = EmburseApi()

        state_provider = RandomStateProvider()
        redirect_uri = os.environ.get('OAUTH_REDIRECT_URL')
        scopes = []

        details = OAuthInitDetails(emburse.oauth_init_url(), emburse.app_client_id(), redirect_uri, scopes, state_provider)

        auth_state = PreAuthState(details)

        oauth_state_map[user_id] = auth_state

        return auth_state


def set_auth_state_for_user(user_id, new_state):
    oauth_state_map[user_id] = new_state
