from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime
from .OAuth import PreAuthState, PostAuthState
from .AuthStateStore import get_auth_state_for_user, set_auth_state_for_user, clear_auth_state_for_user

oauth_param_mem_store = []

# Create your views here.


def index(request):

    # using session_key instead of creating concept of users
    auth_state = get_auth_state_for_user(request.session.session_key)

    if isinstance(auth_state, PreAuthState):
        return HttpResponse('<a href="' + auth_state.init_details.to_url() + '">Authorize via Emburse</a><br><a href="/oauth/clear_cache">clear cache</a>')
    else:
        return HttpResponse('app already authorized')


def clear_auth_cache(request):
    user_id = request.session.session_key
    clear_auth_state_for_user(user_id)
    return index(request)


def callback(request):
    user_id = request.session.session_key

    auth_state = get_auth_state_for_user(user_id)

    if isinstance(auth_state, PreAuthState):
        post_auth_state = auth_state.supply_callback_params(request.GET.copy())
        set_auth_state_for_user(user_id, post_auth_state)
        oauth_param_mem_store.append(request.GET.dict())
        oauth_param_mem_store.append({'__TIME__': str(datetime.now())})
        oauth_param_mem_store.append(request.session.session_key)
        oauth_param_mem_store.append('<br>')
    else:
        oauth_param_mem_store.append({'__TIME__': str(datetime.now())})
        oauth_param_mem_store.append({ 'msg': 'app already authorized', 'access_token': auth_state.access_token})
        oauth_param_mem_store.append('<br>')

    return HttpResponse(oauth_param_mem_store)

