# http://stackoverflow.com/questions/22494583/login-with-code-when-using-liveservertestcase-with-django

from django.conf import settings
from django.contrib.auth import (
    SESSION_KEY, BACKEND_SESSION_KEY, HASH_SESSION_KEY,
    get_user_model,
    authenticate)
from django.contrib.sessions.backends.db import SessionStore

def create_session_cookie(username, password):

    # First, create a new test user
    User = get_user_model()
    user = User.objects.create_user(username=username, password=password)
    user = authenticate(username=username, password=password)

    # Then create the authenticated session using the new user credentials
    session = SessionStore()
    session[SESSION_KEY] = user.pk
    session[BACKEND_SESSION_KEY] = settings.AUTHENTICATION_BACKENDS[0]
    session[HASH_SESSION_KEY] = user.get_session_auth_hash()
    session.save()

    # Finally, create the cookie dictionary
    cookie = {
        'name': settings.SESSION_COOKIE_NAME,
        'value': session.session_key,
        'secure': False,
        'path': '/',
    }
    return cookie
