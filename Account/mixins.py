from django.shortcuts import redirect
from django.contrib.auth.mixins import AccessMixin, UserPassesTestMixin

class NoLoginRequireMixin(UserPassesTestMixin):
    def test_func(self):
        return not self.request.user.is_authenticated
    