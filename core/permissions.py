from rest_framework.permissions import BasePermission
import jwt, re
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from jwt.exceptions import ExpiredSignatureError
from ChatBot.settings import SECRET_KEY
from dotenv import load_dotenv
load_dotenv()

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