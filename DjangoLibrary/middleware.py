from django.contrib import auth
from django.contrib.auth.middleware import AuthenticationMiddleware

import base64


class AutologinAuthenticationMiddleware(AuthenticationMiddleware):

    def process_request(self, request):
        if 'autologin' not in request.COOKIES:
            return
        if request.COOKIES['autologin'] == '':
            auth.logout(request)
            return
        autologin_cookie_value = base64.b64decode(request.COOKIES['autologin'])
        try:
            username = autologin_cookie_value.split(':')[0]
            password = autologin_cookie_value.split(':')[1]
        except TypeError:
            username = autologin_cookie_value.decode('utf8').split(':')[0]
            password = autologin_cookie_value.decode('utf8').split(':')[1]
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                auth.login(request, user)
