from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework.generics import RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from ChatBot.settings import SECRET_KEY
from chatting.models import Ticket, FoodContainer
from core.permissions import IsOwner, GetToken
from .serializers import FoodContainerSerializer
from .prompt import GPTPrompt, image_search_save
import jwt
import json
from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiResponse, OpenApiRequest, OpenApiParameter

class ChatbotAPIView(APIView):
    
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    
    @extend_schema(
    summary="음식추천",
    request=OpenApiRequest,
    examples=[
        OpenApiExample(name='음식추천 메인요리', status_codes='200', value={"prompt": "{난이도: None, 테마: 메인요리, 타입: None, 재료: None, 레시피: None, 직접 입력: None}"}),
        OpenApiExample(name='음식추천 세우튀김', status_codes='200', value={"prompt": "{난이도: None, 테마: None, 타입: None, 재료: None, 레시피: 튀김, 직접 입력: '세우튀김 추천해줘'}"}),
        OpenApiExample(name='음식추천 Custom', status_codes='200', value={"prompt": "{난이도: 상, 테마: 초대요리, 타입: 한식, 재료: 돼지고기, 레시피: 끓이기, 직접 입력: None}"}),
    ],
    responses={
        200: OpenApiResponse(description='요청을 성공했을 때 반환되는 응답입니다.', 
            examples=[OpenApiExample(name="ok", value={
  "Food": "{\n  \"추천메뉴\": \"토마토 파스타\",\n  \"소개\": \"신선한 토마토와 향긋한 양파, 그리고 고소한 파마산 치즈가 어우러진 맛있는 파스타입니다.\",\n  \"재료\": {\n    \"스파게티면\": \"100g\",\n    \"토마토\": \"2개\",\n    \"양파\": \"1개\",\n    \"올리브 오일\": \"2큰술\",\n    \"마늘\": \"2쪽\",\n    \"파마산 치즈\": \"약간\",\n    \"소금\": \"약간\",\n    \"후추\": \"약간\"\n  },\n  \"레시피\": [\n    \"1. 끓는 물에 소금을 넣고 스파게티면을 삶아주세요. 삶은 후 찬물에 헹궈 식혀둡니다.\",\n    \"2. 토마토는 껍질을 벗기고 잘게 썰어주세요. 양파와 마늘도 잘게 다져주세요.\",\n    \"3. 팬에 올리브 오일을 두르고 양파와 마늘을 볶아주세요. 향이 올라오면 토마토를 넣고 중간 불에서 10분간 볶아주세요.\",\n    \"4. 토마토 소스에 소금과 후추를 넣고 잘 섞어주세요.\",\n    \"5. 삶은 스파게티면을 토마토 소스에 넣고 잘 섞어주세요.\",\n    \"6. 그릇에 파마산 치즈를 뿌려주세요.\",\n    \"7. 맛있게 즐겨주세요!\"\n  ]\n}",
  "today_limit": 4
})], 
            response=OpenApiResponse),
        
        400: OpenApiResponse(description='형식에 맞지않는 응답으로 모델생성에 실패했을 때 반환되는 응답입니다. 오늘 남은 사용량을 되돌려줍니다.', 
            examples=[OpenApiExample(name="모델생성 실패", value={
                'error':'모델생성에 실패했습니다. 다음에 다시 시도해주세요.'
            }),
            OpenApiExample(name="GPT응답에러", value={
                    'error': 'ChatGPT응답에러:  + res(api에러메세지)'
                }),
            ], 
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
        GPT API에 요청을 보냅니다. 
        
        엑세스 토큰으로 사용자를 검증하고 해당 사용자의 Ticket 모델을 불러옵니다.
        요청을 보내면 사용자의 today_limit > 0 를 확인하고 크다면 today_limit -= 1 후
        GPT API 요청을 보냅니다. 
        
        API 응답을 받으면 조건, 음식이름, 소개, 재료, 조리법으로 텍스트를 나누어 FoodContainer 모델을 생성 후 모델과, 남은 요청 횟수를 반환합니다.
        
        API응답이 없거나, 모델 생성 중 에러가 발생했으면 에러메시지를 반환합니다. 
        
        반환값:
        
            - 200 OK: API응답을 받고 FoodContainer모델 생성에 성공하면 추천 음식, 남은 요청을 포함한 응답
            - 400 BAD_REQUEST: API응답 또는, 모델생성과정에서 오류가 발생했을 때 응답.
            - 401 Unauthorized: 엑세스 토큰이 만료되거나 데이터가 올바르지 않은 경우의 응답
        '''

        access = GetToken(request)
        
        prompt = request.data.get('prompt', None)
        print('받은요청:', prompt)
        if prompt is None:
            return Response({'error': '올바른 요청이 아닙니다. '}, status=status.HTTP_204_NO_CONTENT)
        
        if access is not None:
            payload = jwt.decode(access, SECRET_KEY, algorithms=['HS256'])
            pk = payload.get('user_id')
            
            ticket = Ticket.objects.get(user_id=pk)
            
            if ticket.today_limit > 0:
                ticket.today_limit -= 1
                ticket.total_used_count += 1
                ticket.save()
            else:
                return Response({"error": "남은 무료제공 횟수가 모두 소진되었습니다. 내일 다시 시도해주세요."},status=status.HTTP_403_FORBIDDEN)
        gpt = GPTPrompt()
        gpt.add_prompt(prompt)
        res = gpt.get_response()
        
        # GPT응답 에러
        if 'error' in res:
            ticket.today_limit += 1
            ticket.total_used_count -= 1
            ticket.save()
            return Response({'error': 'ChatGPT응답에러: ' + res}, status=status.HTTP_400_BAD_REQUEST)
        
        try:       
            # 모델 생성.
            res_dict = json.loads(res)
            foodname = res_dict.get("추천메뉴")
            intro = res_dict.get("소개")
            ingredients = res_dict.get("재료")
            recipe = res_dict.get("레시피")

            food = FoodContainer.objects.create(
                    user=request.user,
                    filter=prompt,
                    foodname=foodname,
                    intro=intro,
                    ingredients=ingredients,
                    recipe=recipe,
                )
            print('food모델 생성됨: ', food.foodname)
            
        except:
            ticket.today_limit += 1
            ticket.total_used_count -= 1
            ticket.save()
            return Response({'error':'모델생성에 실패했습니다. 다음에 다시 시도해주세요.'}, status=status.HTTP_400_BAD_REQUEST)
            
        image_search_save(foodname, food)
        
        return Response({
            'Food': res,
            "today_limit": ticket.today_limit,
            }, status=status.HTTP_200_OK)


    @extend_schema(
    summary="요청 기록 조회",
    request=OpenApiRequest,
    parameters= [OpenApiParameter(
                name="q",
                type=str,
                description="검색어",
                required=False,
            ),
                 OpenApiParameter(
                name="page",
                type= int,
                description="페이지 (공백인 경우 1)",
                required=False,
            ),],
    examples=[
        OpenApiExample(name='음식추천 메인요리', status_codes='200', value={"prompt": "{난이도: None, 테마: 메인요리, 타입: None, 재료: None, 레시피: None, 직접 입력: None}"}),
        OpenApiExample(name='음식추천 세우튀김', status_codes='200', value={"prompt": "{난이도: None, 테마: None, 타입: None, 재료: None, 레시피: 튀김, 직접 입력: '세우튀김 추천해줘'}"}),
        OpenApiExample(name='음식추천 Custom', status_codes='200', value={"prompt": "{난이도: 상, 테마: 초대요리, 타입: 한식, 재료: 돼지고기, 레시피: 끓이기, 직접 입력: None}"}),
    ],
    responses={
        200: OpenApiResponse(description='조회를 성공했을 때 반환되는 응답입니다.', 
            examples=[OpenApiExample(name="ok", value={
            "pk": 16,
            "thumbnail": "/media/chatting/thumbnail/b8ec4d91-be18-4a1c-bc06-9763bf1feafa.png",
            "foodname": "토마토 파스타",
            "ingredients": "{'스파게티면': '100g', '토마토': '2개', '양파': '1개', '올리브 오일': '2큰술', '마늘': '2쪽', '파마산 치즈': '약간', '소금': '약간', '후추': '약간'}"
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
        
        404: OpenApiResponse(description='페이지가 비어있거나 마지막 페이지인 경우 반환되는 응답입니다.', 
            examples=[OpenApiExample(name="Not Found", value={
            "error": "마지막 페이지 입니다."
            })], 
            response=OpenApiResponse),
        
        500: OpenApiResponse(description='FoodContainer에 사용자 id가 없는경우 조회 시 발생하는 에러', 
            examples=[OpenApiExample(name="Error: Internal Server Error"),
            ], 
            ),
    }
)
    def get(self, request):
        '''
        각 사용자의 요청 기록을 불러옵니다.
        
        acess토큰으로 사용자를 검증하고 해당유저의 FoodContainer 모델을 불러옵니다.
        페이지 단위로 모델 정보를 반환합니다. 
        
        Parameters:
        
            - page (int): 요청한 페이지 번호 (기본값: 1)
            - q (str): 검색 필터로 사용할 키워드 (기본값: 빈 문자열)
        
        반환값:
        
            - 200 OK: 조회에 성공하였을 때 반환하는 응답.
            - 404 Not Found: 페이지가 비어있거나 마지막 페이지인 경우의 응답.
            - 401 Unauthorized: 엑세스 토큰이 만료되거나 데이터가 올바르지 않은 경우의 응답
            - 500 Internal Server Error: FoodContainer에 사용자 id가 없는경우 조회 시 발생하는 에러.
        '''
        access = GetToken(request)
        
        page_number = request.GET.get('page', 1)
        search_filter = request.GET.get('q', '') 
        
        if access is not None:
            payload = jwt.decode(access, SECRET_KEY, algorithms=['HS256'])
            pk = payload.get('user_id')
            
            foodcontainers = FoodContainer.objects.filter(user_id=pk, foodname__icontains=search_filter)
            paginator = Paginator(foodcontainers, 3) 

            try:
                # 해당 페이지 가져오기
                current_page = paginator.page(page_number) 
            except PageNotAnInteger:
                # 페이지가 정수가 아닌 경우, 첫 페이지 가져오기
                current_page = paginator.page(1)
            except EmptyPage:
                return Response({'error': '마지막 페이지 입니다.'}, status=status.HTTP_404_NOT_FOUND)

            # 쿼리셋을 순회하면서 정보 추출
            # 리스트: 이름, 재료
            food_list = [{
                'pk': foodcontainer.pk,
                'thumbnail': foodcontainer.thumbnail.url,
                'foodname': foodcontainer.foodname,
                'ingredients': foodcontainer.ingredients,
            } for foodcontainer in current_page]

        return JsonResponse(food_list, safe=False,  status=status.HTTP_200_OK)
    
    
@extend_schema(
    summary="요청 기록 디테일",
    request=FoodContainerSerializer,
    responses={
                200: OpenApiResponse(description='FoodContainer모델에 연결된 user의 pk값이랑 일치하는 경우, 항목을 보여줍니다', 
                examples=[OpenApiExample(name="정상요청", value={
                "pk": 16,
                "foodname": "토마토 파스타",
                "intro": "신선한 토마토와 향긋한 양파, 그리고 고소한 파마산 치즈가 어우러진 맛있는 파스타입니다.",
                "ingredients": "{'스파게티면': '100g', '토마토': '2개', '양파': '1개', '올리브 오일': '2큰술', '마늘': '2쪽', '파마산 치즈': '약간', '소금': '약간', '후추': '약간'}",
                "recipe": "['1. 끓는 물에 소금을 넣고 스파게티면을 삶아주세요. 삶은 후 찬물에 헹궈 식혀둡니다.', '2. 토마토는 껍질을 벗기고 잘게 썰어주세요. 양파와 마늘도 잘게 다져주세요.', '3. 팬에 올리브 오일을 두르고 양파와 마늘을 볶아주세요. 향이 올라오면 토마토를 넣고 중간 불에서 10분간 볶아주세요.', '4. 토마토 소스에 소금과 후추를 넣고 잘 섞어주세요.', '5. 삶은 스파게티면을 토마토 소스에 넣고 잘 섞어주세요.', '6. 그릇에盛り付けて 파마산 치즈를 뿌려주세요.', '7. 맛있게 즐겨주세요!']",
                "thumbnail": "http://127.0.0.1:8000/media/chatting/thumbnail/b8ec4d91-be18-4a1c-bc06-9763bf1feafa.png",
                "created_at": "2023-11-29T16:54:30.518933"
                })], 
                response=OpenApiResponse),
                
                403: OpenApiResponse(description='FoodContainer모델에 연결된 user의 pk값이랑 다른 경우, 메세지를 응답합니다', 
                examples=[OpenApiExample(name="권한없음", value={
                "detail": "이 작업을 수행할 권한(permission)이 없습니다."
                })], 
                response=OpenApiResponse),
                
                404: OpenApiResponse(description='FoodContainer모델에 없는 pk인 경우 반환되는 응답입니다.', 
                examples=[OpenApiExample(name="Not Found", value={
                "detail": "찾을 수 없습니다."
                })], 
                response=OpenApiResponse),
                # 200: FoodContainerSerializer
    },
)
class ChatDetailAPIView(RetrieveAPIView):
    '''
    요청 기록 상세내용을 불러옵니다. 
    
    음식의 상세정보를 불러옵니다. 썸네일, 이름, 소개, 재료, 레시피, 생성시간을 반환합니다. 
        
        Parameters:
        
            - id (int): 요청한 음식의 pk값
        
        반환값:
        
            - 200 OK: 조회에 성공하였을 때 반환하는 응답.
            - 401 Unauthorized: 엑세스 토큰이 만료되거나 데이터가 올바르지 않은 경우의 응답
            - 403 Forbidden: 해당 요청에 대한 권한이 없을 경우의 응답.
    '''
    permission_classes = [IsOwner]
    
    queryset = FoodContainer.objects.all()
    serializer_class = FoodContainerSerializer

