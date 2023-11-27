from rest_framework.generics import CreateAPIView
    
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from core.permissions import GetToken
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from jwt.exceptions import ExpiredSignatureError
from .serializers import *
import jwt, datetime, os
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from ChatBot.settings import SECRET_KEY
from chatting.models import Ticket
from dotenv import load_dotenv
load_dotenv()



class RefreshAPIView(APIView):
    
    def post(self, request):
    # 토큰 만료 시 토큰 갱신

        refresh_token = request.data.get('refresh', None)
        print(refresh_token)
        
        if refresh_token:

            refresh = RefreshToken(refresh_token)
            access = str(refresh.access_token)
            res = Response({"access": access}, status=status.HTTP_200_OK)
            res.set_cookie('access', access)
                
            return res
        raise jwt.exceptions.InvalidTokenError


class SignUpAPIView(CreateAPIView):
    
    
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def post(self, request):
        serializer = UserSerializer(data = request.data)
        if serializer.is_valid():
            user = serializer.save()
            profile = Profile.objects.create(user=user)
            #ticket생성
            ticket = Ticket.objects.create(user=user)
            # ticket = Ticket.objects.get(user=user)
            today_limit = ticket.today_limit
            
            token = TokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)
            response = Response(
                {
                    'user': serializer.data['email'],
                    'message': '회원가입에 성공했습니다.',
                    'lastupdate': user.profile.updated_at,
                    'token': {
                        'access_token': access_token,
                        'refresh_token': refresh_token,
                    },
                    'ticket': today_limit,
                },
                status = status.HTTP_201_CREATED
            )
        
            response.set_cookie('access', access_token)
            response.set_cookie('refresh', refresh_token)
            
            return response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class LoginAPIView(APIView):
    #내 정보 확인, 토큰 리프레쉬
    def get(self, request):
        try:        
            access = GetToken(request)
            
            if access is not None:
                payload = jwt.decode(access, SECRET_KEY, algorithms=['HS256'])
                pk = payload.get('user_id')
                #user
                user = get_object_or_404(User, pk=pk)
                
                # user >> profile.username
                try:
                    username = user.profile.username
                    lastlogin = user.updated_at
                except:
                    username = None
                serializer = UserSerializer(instance=user)
                return Response(
                    {
                    'username': username,
                    'email': serializer.data['email'], 
                    'lastlogin': lastlogin
                    },
                    status=status.HTTP_200_OK
                    )
            return Response(
                {
                    'message': '로그인이 필요한 서비스입니다.'
                },
                status = status.HTTP_401_UNAUTHORIZED
            )
        except(jwt.exceptions.InvalidTokenError):

            return Response(
                {
                    'message': '다시 로그인해주세요.'
                },
                status=status.HTTP_400_BAD_REQUEST
                )
    
    #로그인
    def post(self, request):
        
        user = authenticate(
            email = request.data.get('email'),
            password = request.data.get('password')
        )
        
        if user is not None:
            serializer = UserSerializer(user)
            
            token = TokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)
            ticket = Ticket.objects.get(user_id=user.pk)
            
            
            if ticket.updated_at.date() != datetime.date.today():
                ticket.today_limit = os.environ.get('TODAY_LIMIT')
                ticket.save()
            
            res = Response(
                {
                    'message': '로그인 성공',
                    'user': serializer.data['email'],
                    'lastupdate': user.profile.updated_at,
                    'token': {
                        'access': access_token,
                        'refresh': refresh_token,
                    },
                    'today_limit':ticket.today_limit,
                },
                status=status.HTTP_200_OK,
            )
            
            res.set_cookie('access', access_token, samesite='None', secure=False)
            res.set_cookie('refresh', refresh_token, samesite='None', secure=False)
            return res
        else:
            return Response(
                {'message':'이메일 혹은 비밀번호가 잘못되었습니다.'},
                status=status.HTTP_400_BAD_REQUEST
                )
            
    #로그아웃
    def delete(self, request):
    
        response = Response({
            'message': '로그아웃 되었습니다.'
            }, status=status.HTTP_202_ACCEPTED)
        response.delete_cookie('access')
        response.delete_cookie('refresh')
        return response
    
    
class ProfileAPIView(APIView):
    # 프로필 변경
    
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        
        access = GetToken(request)
        
        try:
            if access is not None:
                payload = jwt.decode(access, SECRET_KEY, algorithms=['HS256'])
                pk = payload.get('user_id')
                # 사용자가 있는 경우
                user = User.objects.get(pk=pk)
                lastupdate = user.profile.updated_at
                # 프로필이 있는 경우 기존 프로필을 업데이트
                if hasattr(user, 'profile'):
                    profile_serializer = ProfileSerializer(user.profile, data=request.data, partial=True)
                else:
                    # 프로필이 없는 경우 새로운 프로필 생성
                    profile_serializer = ProfileSerializer(data=request.data)
            else:
                return Response({"message": "로그인이 필요한 서비스입니다."}, status=status.HTTP_401_UNAUTHORIZED)
        except jwt.exceptions.ExpiredSignatureError:
            return Response({"message": "토큰이 만료되었습니다. 다시 로그인해주세요."}, status=status.HTTP_401_UNAUTHORIZED)
        except User.DoesNotExist:
            return Response({"message": "해당하는 사용자가 없습니다."}, status=status.HTTP_404_NOT_FOUND)
        
        if profile_serializer.is_valid():
            profile_serializer.save(user=user)
            
            res = profile_serializer.data
            return Response({
                "message": "프로필을 수정했습니다.",
                'lastupdate': lastupdate,
                "Profile": res
                                }, 
                status=status.HTTP_200_OK)
        
        return Response(profile_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # 프로필 확인
    def get(self, request):
        # 프로필 보여주기
        
        try:
            access = GetToken(request)
            
            if access is not None:
                payload = jwt.decode(access, SECRET_KEY, algorithms=['HS256'])
                pk = payload.get('user_id')
                
                try:
                    user = User.objects.get(pk=pk)
                    
                    if hasattr(user, 'profile'):
                        profile = user.profile
                        serializer = ProfileSerializer(profile)
                        
                        res = serializer.data
                    else:
                        res = {"message": "프로필이 존재하지 않습니다."}
                        
                    return Response(res, status=status.HTTP_200_OK)
                    
                except User.DoesNotExist:
                    return Response({"message": "해당하는 사용자가 없습니다."}, status=status.HTTP_404_NOT_FOUND)
            
            else:
                return Response({"message": "로그인이 필요한 서비스입니다."}, status=status.HTTP_401_UNAUTHORIZED)
                
        except ExpiredSignatureError:
            return Response({"message": "토큰이 만료되었습니다. 다시 로그인해주세요."}, status=status.HTTP_401_UNAUTHORIZED)
        
