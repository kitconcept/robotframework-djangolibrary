from django.contrib.auth import authenticate as django_authenticate
from django.contrib.auth import login
from django.contrib.auth.middleware import AuthenticationMiddleware


class MyBackend(object):

    def authenticate(self, username=None, password=None):
        username = 'admin'
        password = 'password'
        user = django_authenticate(username=username, password=password)
        return user


class AutologinAuthenticationMiddleware(AuthenticationMiddleware):

    def process_request(self, request):
        import sys
        import pdb
        for attr in ('stdin', 'stdout', 'stderr'):
            setattr(sys, attr, getattr(sys, '__%s__' % attr))
        pdb.set_trace()
        super(AuthenticationMiddleware, self).process_request()
        if False:
            username = 'admin'
            password = 'password'
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)


from django.contrib.auth.middleware import RemoteUserMiddleware


class CustomHeaderMiddleware(RemoteUserMiddleware):

    def authenticate(self, remote_user):
        import sys
        import pdb
        for attr in ('stdin', 'stdout', 'stderr'):
            setattr(sys, attr, getattr(sys, '__%s__' % attr))
        pdb.set_trace()
        if False:
            username = 'admin'
            password = 'password'
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)

    def configure_user(self, user):
        import sys
        import pdb
        for attr in ('stdin', 'stdout', 'stderr'):
            setattr(sys, attr, getattr(sys, '__%s__' % attr))
        pdb.set_trace()
