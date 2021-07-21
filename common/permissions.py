from rest_framework import permissions

class ReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.method in permissions.SAFE_METHODS

class IsAuthenticated(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated

class IsConsumer(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_consumer

class IsPartner(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_partner

class IsSalesman(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_salesman

class IsSupport(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_support

class IsSubAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_sub_admin

class IsStoreOwner(permissions.BasePermission):
    """
    Allows access only if the Partner is owner of the Store.
    """
    def has_object_permission(self, request, view, obj):
        print(obj, request.user.partner)
        return obj.owner == request.user.partner

class HasABooking(permissions.BasePermission):
    """
    Allows access if Consumer has a booking.
    """