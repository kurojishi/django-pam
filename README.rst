django-pam
==========
A simple PAM authentication backend for Django.  Add the folder ``dpam``
somewhere on your python path and add 'dpam.backends.PAMBackend' to your
``settings.py``::

  AUTHENTICATION_BACKENDS = (
      ...
      'dpam.backends.PAMBackend',
      ...
  )

Now you can login via the system-login credentials.  If the user is
successfully authenticated but has never logged-in before, a new ``User``
object is created.  By default this new ``User`` has both ``is_staff`` and
``is_superuser`` set to ``False``.  You can change this behavior by adding
``PAM_IS_STAFF=True`` and ``PAM_IS_SUPERUSER`` in your ``settings.py`` file.

If you do not want a ``User`` record to be created automatically, use
``PAM_CREATE_USER=False`` in ``settings.py``.  This is useful in situations
where you want to use PAM for authentication but not for authorization.

If you want your new users in a specific group use the setting ``PAM_USERS_GROUP="<group_name>"``,
this will automatically add them to the group.
