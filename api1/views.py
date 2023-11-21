from rest_framework.generics import GenericAPIView, ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView \
    
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from .serializers import *
import jwt
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from ChatBot.settings import SECRET_KEY


class SignUpAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def post(self, request):
        serializer = UserSerializer(data = request.data)
        if serializer.is_valid():
            user = serializer.save()
            
            token = TokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)
            response = Response(
                {
                    'user': serializer.data['email'],
                    'message': '회원가입에 성공했습니다.',
                    'token': {
                        'access_token': access_token,
                        'refresh_token': refresh_token,
                    },
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
            
            access = request.COOKIES.get('access', None)
            if access is not None:
                payload = jwt.decode(access, SECRET_KEY, algorithms=['HS256'])
                pk = payload.get('user_id')
                #user
                user = get_object_or_404(User, pk=pk)
                # user >> profile.username
                try:
                    username = user.profile.username
                except:
                    username = None
                serializer = UserSerializer(instance=user)
                return Response(
                    {
                    'username': username,
                    'email': serializer.data['email'], 
                    },
                    status=status.HTTP_200_OK
                    )
            return Response(
                {
                    'message': '로그인이 필요한 서비스입니다.'
                },
                status = status.HTTP_401_UNAUTHORIZED
            )

        except(jwt.exceptions.ExpiredSignatureError):
            # 토큰 만료 시 토큰 갱신
            refresh_token = request.COOKIES.get('refresh', None)
            
            if refresh_token:
                print(f'리프레쉬 토큰:{refresh_token}')
                data = {'refresh':refresh_token}
                # serializer = TokenRefreshSerializer(data=data)
                refresh = RefreshToken(refresh_token)
                print(f'새로운 어세스 토큰:{refresh.access_token}')
                access = str(refresh.access_token)

                res = Response({"acess_token": access}, status=status.HTTP_200_OK)
                res.set_cookie('access', access)
                    
                return res
            raise jwt.exceptions.InvalidTokenError

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
            res = Response(
                {
                    'user': serializer.data['email'],
                    'message': 'login success',
                    'token': {
                        'access': access_token,
                        'refresh': refresh_token,
                    },
                },
                status=status.HTTP_200_OK,
            )
            
            res.set_cookie('access', access_token)
            res.set_cookie('refresh', refresh_token)
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
    def post(self, request):
        '''
        access토큰에서 user_id값을 가져와 프로필을 변경합니다.
        프로필이 없는 경우 새로운 프로필을 생성(1:1 관계), 있는경우 기존 프로필을 변경.
        로그인하지않은 사용자가 요청 시 "로그인이 필요한 서비스입니다." 를 출력합니다.
        '''
        access = request.COOKIES.get('access', None)
        if access is not None:
            payload = jwt.decode(access, SECRET_KEY, algorithms=['HS256'])
            pk = payload.get('user_id')
            #user
            try:
                # 사용자가 있는 경우
                user = User.objects.get(pk=pk)
                
                # 프로필이 있는 경우 기존 프로필을 업데이트
                if hasattr(user, 'profile'):
                    profile_serializer = ProfileSerializer(user.profile, data=request.data, partial=True)
                else:
                    # 프로필이 없는 경우 새로운 프로필 생성
                    profile_serializer = ProfileSerializer(data=request.data)
            except User.DoesNotExist:
                return Response({"message": "해당하는 사용자가 없습니다."}, status=status.HTTP_404_NOT_FOUND)
            
            if profile_serializer.is_valid():
                profile_serializer.save(user=user)
                
                res = profile_serializer.data
                return Response({
                    "message": "프로필을 수정했습니다.",
                    "Profile": res
                                 }, 
                    status=status.HTTP_200_OK)
            
            return Response(profile_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({"message": "로그인이 필요한 서비스입니다."}, status=status.HTTP_401_UNAUTHORIZED)
    
    # 프로필 확인
    def get(self, request):
        # 프로필 보여주기
        
        access = request.COOKIES.get('access', None)
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