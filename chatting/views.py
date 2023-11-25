
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from ChatBot.settings import SECRET_KEY
from chatting.models import Ticket, FoodContainer
from accounts.models import User
from .prompt import GPTPrompt
import jwt, json



class ChatbotView(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def post(self, request):
        '''
        acess토큰으로 유저를 검증하고 해당유저의 Ticket 모델을 불러옵니다.
        요청을 보내면 유저의 today_limit > 0 를 확인하고 크다면 today_limit -= 1 후
        GPTPrompt를 불러와 요청을 보냅니다. 응답이 정상이라면받은 메세지를,
        에러가 발생했으면 에러메세지를 반환합니다. 
        '''

        access = request.COOKIES.get('access', None)
        prompt = request.data.get('prompt', None)
        
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
        
        # 모델 생성.
        res_dict = json.loads(res)
        foodname = res_dict.get("추천메뉴", "")
        intro = res_dict.get("소개", "")
        ingredients = res_dict.get("재료", "")
        recipe = res_dict.get("레시피", "")

        try:       
            food = FoodContainer.objects.create(
                    user=request.user,
                    filter=prompt,
                    foodname=foodname,
                    intro=intro,
                    ingredients=ingredients,
                    recipe=recipe,
                )

        except:
            ticket.today_limit += 1
            ticket.total_used_count -= 1
            ticket.save()
            return Response({'error':'모델생성에 실패했습니다. 다음에 다시 시도해주세요.'}, status=status.HTTP_400_BAD_REQUEST)
            
        return Response({
            'Food': res,
            "today_limit": ticket.today_limit,
            }, status=status.HTTP_200_OK)
