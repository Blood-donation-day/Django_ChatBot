from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiResponse, OpenApiRequest
from rest_framework.generics import CreateAPIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from core.permissions import GetToken
from jwt.exceptions import ExpiredSignatureError
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from ChatBot.settings import SECRET_KEY
from chatting.models import Ticket
from .serializers import *
from dotenv import load_dotenv
import jwt, datetime, os
load_dotenv()


class RefreshAPIView(APIView):
    @extend_schema(
    summary="엑세스토큰 갱신",
    request= OpenApiRequest,
    examples=[
        OpenApiExample(name='토큰 갱신', status_codes='200', value={
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcwMTI0MDcxNCwiaWF0IjoxNzAxMjMzNTE0LCJqdGkiOiJmZDJiM2RiNDg4Yzg0Y2E5OWQwOWZhZWRmZDY3ODc4MiIsInVzZXJfaWQiOjJ9.R777i-0_AaqRrk22iXoPV09b7PuLrDjSkJFu7XfXYf4"
    }),
    ],
    responses={
        200: OpenApiResponse(description='토큰 갱신에 성공했을 때 반환되는 응답입니다.', 
            examples=[OpenApiExample(name="ok", value={
                
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzAxMjM1MzUwLCJpYXQiOjE3MDEyMzM1MTQsImp0aSI6Ijc4YzQ2YmNlYzY3MzQ5ZGY4MmNlM2I5YzY4Y2MxOTRmIiwidXNlcl9pZCI6Mn0.236HGNmxvbMu-XwTMPTclJrua1bTNJR7cGvlQ6f7Txs"

            })], 
            
            response=OpenApiResponse),
        500: OpenApiResponse(description='기간만료 또는 리프레쉬 토큰이 유효하지 않다면 반환되는 오류 응답입니다.')
    }
)
    def post(self, request):
        '''
        리프레쉬 토큰으로 엑세스 토큰을 갱신합니다.
        
        이 뷰는 엑세스 토큰이 만료되어 401 응답이 올 경우 호출됩니다.
        
        제공된 리프레쉬 토큰을 사용하여 새로운 엑세스 토큰을 생성하고 응답에 반환합니다.

        반환값:
        
            - 200 OK: 새로운 엑세스 토큰이 포함된 응답
            - 500 error: 리프레쉬 토큰값이 유효하지 않은 경우의 응답
        '''

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
    
    @extend_schema(
    summary="회원가입",
    request=UserSerializer,
    examples=[
        OpenApiExample(name='회원가입 예제', status_codes='201', value={"email": 'test1234@test1234.com', "password": 'mypwd1234'}),
        OpenApiExample(name='비밀번호 규칙 오류', status_codes='400', value={"email": 'test1234@test1234.com', "password": '1q2w3e4r'})
    ],
    responses={
        201: OpenApiResponse(description='정상적으로 회원가입이 성공했을 때 응답코드입니다.', 
            examples=[OpenApiExample(name="ok", value={
                "user": "test1234@test1234.com",
                "message": "회원가입에 성공했습니다.",
                "lastupdate": "2023-11-29T13:40:06.066202",
                "token": {
                    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzAxMjM0NjA2LCJpYXQiOjE3MDEyMzI4MDYsImp0aSI6IjJhNmQxZjJmMTlmZDRkYWNhMmYyOTA5YmJmZDQ0YjQ0IiwidXNlcl9pZCI6N30.uIPj9Z25IbKsPsteQHDt33HyDqrIEAlLwO-79rh_gsw",
                    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcwMTI0MDAwNiwiaWF0IjoxNzAxMjMyODA2LCJqdGkiOiJjZjlmNWMzY2JlZWU0MGU4YTEyMzUyZWExYjI4ZDAwYiIsInVzZXJfaWQiOjd9.BaRtaLAEzLhh5_GLzghpbK-GbLvXrxDgaGFUu_qeL9I"
                },
                "ticket": "5"
            })], 
            
            response=UserSerializer),
        400: OpenApiResponse(description='회원가입에서 오류가 발생하면 오류메세지를 반환합니다.', 
            examples=[OpenApiExample(name="error", value={ 
                "email": ["user의 email은/는 이미 존재합니다."],
                "password": ["비밀번호가 너무 일상적인 단어입니다."]
            })], response='400')
    }
)
    def post(self, request):
        '''
        회원가입 요청을 처리합니다.
        
        email과 password를 받으면 데이터를 검증 후 새로운 유저(User)를 생성합니다.
        Profile과 Ticket모델도 같이 생성 후 토큰값과 응답을 반환합니다.
        
        반환값:
        
            - 201 Created: 회원가입이 성공하면 유저 정보, 토큰 및 티켓 정보를 포함한 응답
            - 400 Bad Request: 입력 데이터가 올바르지 않은 경우의 응답
    
        '''
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

    @extend_schema(
    summary="로그인 확인",
    request=OpenApiRequest,
    responses={
        200: OpenApiResponse(description='조회를 성공했을 때 반환되는 응답입니다.', 
            examples=[OpenApiExample(name="ok", value={
                "username": "",
                "email": "test1234@test1234.com",
                "lastlogin": "2023-11-29T11:26:36.834278"
            })], 
            response=OpenApiResponse),
        
        401: OpenApiResponse(description='토큰이 만료된 경우 반환되는 응답입니다.', 
            examples=[
                OpenApiExample(name="토큰만료", value={
                    "detail": "이 토큰은 모든 타입의 토큰에 대해 유효하지 않습니다",
                    "code": "token_not_valid",
                    "messages": [
                        {
                            "token_class": "AccessToken",
                            "token_type": "access",
                            "message": "유효하지 않거나 만료된 토큰"
                        }
                    ]
                }),
                OpenApiExample(name="토큰값을 보내지않음", value={
                    "message": "로그인이 필요한 서비스입니다."
                }),
            ], 
            response=OpenApiResponse
        ),
    }
)
    def get(self, request):
        '''
        토큰값을 확인하는 엔드포인트입니다. 엑세스 토큰을 검증하여 사용자 정보를 반환합니다.
        
        
        반환값:
        
        
            - 200 OK: 회원가입이 성공하면 유저 정보, 토큰 및 티켓 정보를 포함한 응답
            - 401 Unauthorized: 엑세스 토큰이 만료되거나 데이터가 올바르지 않은 경우의 응답
        '''
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
    
    @extend_schema(
    summary="로그인",
    request=OpenApiRequest,
    examples=[
        OpenApiExample(name='로그인 예제', status_codes='200', value={"email": 'test1234@test1234.com', "password": 'mypwd1234'}),
        OpenApiExample(name='이메일 혹은 비밀번호가 다른 경우', status_codes='400', value={"email": 'tset1234@test1234.com', "password": 'anotherpassword'}),
        OpenApiExample(name='유효하지 않은 문자를 입력', status_codes='400', value={"email": 'tset1234@test1234.com', "password": 'mypwd1234\\'}),
    ],
    responses={
        200: OpenApiResponse(description='로그인이 성공했을 때 반환되는 응답입니다.', 
            examples=[OpenApiExample(name="ok", value={
            "message": "로그인 성공",
            "user": "test1234@test1234.com",
            "lastupdate": "2023-11-29T11:26:36.839536",
            "token": {
                "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzAxMjM2Mzk0LCJpYXQiOjE3MDEyMzQ1OTQsImp0aSI6IjQ3ZDc5ZmYzZGE3MzQzMjQ5NGMzZDg4MGYwNzk5OWY3IiwidXNlcl9pZCI6Nn0.TW1ZE5AyYHX-EhBCTkZ9htFZJJaaVIETUL5G7ZpDg40",
                "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcwMTI0MTc5NCwiaWF0IjoxNzAxMjM0NTk0LCJqdGkiOiI4MzYxM2YxN2I5NTc0MTkxOWFjYjc2MGEyMTFjMWZkYiIsInVzZXJfaWQiOjZ9.CrEqk2ColVqzhAKmClFc_EBbk92CgJoFGblsH5zKEKk"
            },
            "today_limit": 5
            })], 
            response=OpenApiResponse),
        
            400: OpenApiResponse(description='아이디 혹은 비밀번호가 다를 때 오류 응답을 반환합니다.', 
            examples=[
                OpenApiExample(name="ID or Password error", value={ 
                    "message": "이메일 혹은 비밀번호가 잘못되었습니다."
                }),
                OpenApiExample(name="type error", value={ 
                    "detail": "JSON parse error - Invalid control character at: line 3 column 33 (char 70)"
                })], response=OpenApiResponse
            ),
    }
)
    def post(self, request):
        '''
        로그인 요청을 처리합니다.
        
        email과 password를 사용하여 유저를 인증합니다. 인증이 성공하면 엑세트토큰, 리프레시 토큰을 생성하고,
        
        유저의 티켓 정보를 업데이트합니다. 유저 정보, 토큰, 티켓값을 반환합니다.
        
        반환값:
        
            - 200 OK: 유저 정보 및 토큰이 포함된 로그인 성공 응답
            - 400 Bad Request: 올바르지 않은 이메일 또는 비밀번호 입력 시 응답
        '''
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
            
            
            if ticket.updated_at.date() != datetime.date.today() and ticket.today_limit < int(os.environ.get('TODAY_LIMIT')):
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
            
    @extend_schema(
    summary="로그아웃",
    request=OpenApiRequest,
    responses={
        202: OpenApiResponse(description='로그아웃 요청 응답입니다.', 
            examples=[OpenApiExample(name="ACCEPTED", value={
            "message": "로그아웃 되었습니다."
            })], 
            response=OpenApiResponse)},
        )
    def delete(self, request):
        '''
        로그아웃 요청을 처리합니다. 브라우저에서 쿠키를 삭제할 수 있습니다.
        
        반환값:
        
            - 202 ACCEPTED: 유저 정보 및 토큰을 브라우저에서 삭제합니다.
        '''
        response = Response({
            'message': '로그아웃 되었습니다.'
            }, status=status.HTTP_202_ACCEPTED)
        response.delete_cookie('access')
        response.delete_cookie('refresh')
        return response
    
    
class ProfileAPIView(APIView):
    
    permission_classes = [IsAuthenticated]
    
    @extend_schema(
    summary="프로필 변경",
    request=OpenApiRequest,
    examples=[
        OpenApiExample(name='프로필 변경 1', status_codes='200', value={"username": "테스트계정","introduce": "테스트용 자기소개입니다."}),
        OpenApiExample(name='프로필 변경 2', status_codes='200', value={"username": "테스트계정"}),
    ],
    responses={
        200: OpenApiResponse(description='프로필 변경을 성공했을 때 반환되는 응답입니다.', 
            examples=[OpenApiExample(name="ok", value={
        "message": "프로필을 수정했습니다.",
        "lastupdate": "2023-11-29T11:26:36.839536",
        "Profile": {
            "username": "테스트계정",
            "profile_img": 'null',
            "introduce": "테스트용 자기소개입니다."
        }
        })], 
            response=OpenApiResponse),
        
        401: OpenApiResponse(description='토큰이 만료된 경우 반환되는 응답입니다.', 
            examples=[
                OpenApiExample(name="토큰만료", value={
                    "detail": "이 토큰은 모든 타입의 토큰에 대해 유효하지 않습니다",
                    "code": "token_not_valid",
                    "messages": [
                        {
                            "token_class": "AccessToken",
                            "token_type": "access",
                            "message": "유효하지 않거나 만료된 토큰"
                        }
                    ]
                }),
                OpenApiExample(name="토큰값을 보내지않음", value={
                    "message": "로그인이 필요한 서비스입니다."
                }),
            ], 
            response=OpenApiResponse
        ),
    }
)
    def post(self, request):
        '''
        사용자 프로필을 업데이트합니다.
        
        반환값:
        
            - 200 OK: 프로필변경에 성공하면 유저 정보, 업데이트 시간을 포함한 응답
            - 401 Unauthorized: 엑세스 토큰이 만료되거나 데이터가 올바르지 않은 경우의 응답
        '''
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
    
    @extend_schema(
    summary="프로필 확인",
    request=OpenApiRequest,
    responses={
        200: OpenApiResponse(description='정상요청 시 반환되는 응답입니다.', 
            examples=[OpenApiExample(name="ok", value={
            "username": "테스트계정",
            "profile_img": 'null',
            "introduce": "테스트용 자기소개입니다."
            })], 
            response=OpenApiResponse),
        
        401: OpenApiResponse(description='토큰이 만료된 경우 반환되는 응답입니다.', 
            examples=[
                OpenApiExample(name="토큰만료", value={
                    "detail": "이 토큰은 모든 타입의 토큰에 대해 유효하지 않습니다",
                    "code": "token_not_valid",
                    "messages": [
                        {
                            "token_class": "AccessToken",
                            "token_type": "access",
                            "message": "유효하지 않거나 만료된 토큰"
                        }
                    ]
                }),
                OpenApiExample(name="토큰값을 보내지않음", value={
                    "message": "로그인이 필요한 서비스입니다."
                }),
            ], 
            response=OpenApiResponse
        ),
    }
)
    def get(self, request):
        '''
        사용자의 프로필을 확인하는 엔드포인트입니다.
        
        반환값:
        
            - 200 OK: 사용자를 확인하면 Profile모델의 정보를 응답합니다.
            - 401 Unauthorized: 엑세스 토큰이 만료되거나 데이터가 올바르지 않은 경우의 응답
        '''
        
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