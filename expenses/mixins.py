from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied

# Mixin to ensure that only the owner of an object can access or modify it.
class OwnerRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        obj = self.get_object()
        return obj.user == self.request.user

    def handle_no_permission(self):
        raise PermissionDenied("You do not have permission to access this object.")

# Mixin to ensure that only admin users can access or modify an object.
class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        # A user is considered an admin if their custom role is 'admin'
        # OR if they are a Django superuser (is_superuser=True).
        # This provides flexibility for both custom roles and default Django superusers.
        return self.request.user.is_authenticated and \
               (self.request.user.role == 'admin' or self.request.user.is_superuser)

    def handle_no_permission(self):
        raise PermissionDenied("You do not have admin permission to access this page.")