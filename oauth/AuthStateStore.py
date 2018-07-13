import os
from .EmburseApi import EmburseApi
from .OAuth import RandomStateProvider, OAuthInitDetails, PreAuthState, AuthState
import pickle
import codecs

# time is extremely limited here, so I'm just pickling the states
# obvious bad practice, saving state in the db would be preferable
oauth_state_map = {}

AUTH_STATE_KEY = 'auth_state'

def get_auth_state_for_user(session) -> AuthState:
    if AUTH_STATE_KEY in session:
        pickled = session[AUTH_STATE_KEY]
        return pickle.loads(codecs.decode(pickled.encode(), 'base64'))
    else:
        emburse = EmburseApi()

        state_provider = RandomStateProvider()
        redirect_uri = os.environ.get('OAUTH_REDIRECT_URL')
        scopes = []

        details = OAuthInitDetails(emburse.oauth_init_url(), emburse.app_client_id(), redirect_uri, scopes, state_provider)

        auth_state = PreAuthState(details)

        set_auth_state_for_user(session, auth_state)

        return auth_state


def set_auth_state_for_user(session, new_state):
    session[AUTH_STATE_KEY] = codecs.encode(pickle.dumps(new_state), 'base64').decode()


def clear_auth_state_for_user(session):
    session.pop(AUTH_STATE_KEY, None)

