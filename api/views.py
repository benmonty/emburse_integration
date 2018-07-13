from django.http import JsonResponse, HttpResponse
from oauth.EmburseApi import EmburseApi
from oauth.AuthStateStore import get_auth_state_for_user
from oauth.OAuth import PostAuthState

# Create your views here.


def index(request, proxy_path):

    auth_state = get_auth_state_for_user(request.session.session_key)

    if isinstance(auth_state, PostAuthState):
        emburse = EmburseApi();
        response = emburse.request(auth_state.access_token, request.method, proxy_path, request.META['QUERY_STRING'])
        return JsonResponse(response)
    else:
        return HttpResponse('Unauthorized', status=401)
