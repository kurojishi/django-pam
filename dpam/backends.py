""" Django PAM Authentication Backend"""

import syslog
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.contrib.auth.backends import ModelBackend

import dpam.pam as pam


class PAMBackend(ModelBackend):
    """PAM Auth Backend"""

    def authenticate(self, username=None, password=None):
        syslog.syslog('django pam realyy')
        service = getattr(settings, 'PAM_SERVICE', 'login')
        if not pam.authenticate(username, password, service=service):
            return None

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            if not getattr(settings, "PAM_CREATE_USER", True):
                return None
            user = User(username=username, password='not stored here')
            user.set_unusable_password()

            if getattr(settings, 'PAM_IS_SUPERUSER', False):
                user.is_superuser = True

            if getattr(settings, 'PAM_IS_STAFF', user.is_superuser):
                user.is_staff = True

            user.save()

            if getattr(settings, 'PAM_USERS_GROUP', False):
                group = Group.objects.get(name=settings.PAM_USERS_GROUP)
                group.user_set.add(user)
                group.save()

        return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
