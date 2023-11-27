from rest_framework.permissions import BasePermission
import re

class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):

        if request.method in ['HEAD', 'OPTIONS']:
            return True
        
        return obj.user == request.user
    

def GetToken(request):
    token = request.META.get('HTTP_AUTHORIZATION', None)
    match = re.search(r'Bearer (.+)', token)
    if match:
        token = match.group(1)
    return token