from rest_framework.permissions import BasePermission
from . import models


class IsAuthenticatedOrAuthAccountWrite(BasePermission):
    def has_permission(self, request, view):
        try:
            if request.headers.get('Token-Student') != None:
                models.Account.objects.get(token=request.headers.get('Token-Student'))
                token = True
            else:
                token = False
        except models.Account.DoesNotExist:
            token = False
        
        return bool(
            request.method in ('POST') and 
            token or
            request.user and
            request.user.is_authenticated 
        )


class IsAuthenticatedOrAuthAccountUpdate(BasePermission):
    def has_permission(self, request, view):
        try:
            if request.headers.get('Token-Student') != None:
                models.Account.objects.get(
                    id=view.kwargs['pk'],
                    token=request.headers.get('Token-Student')
                )
                token = True
            else:
                token = False
        except models.Account.DoesNotExist:
            token = False
        
        return bool(
            token or
            request.user and
            request.user.is_authenticated 
        )