from django.contrib.auth import login
from django.contrib.auth import authenticate
from django.contrib.auth.middleware import AuthenticationMiddleware


class AutologinAuthenticationMiddleware(AuthenticationMiddleware):

    def process_request(self, request):
        username = 'test-user-2'
        password = 'password'
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
