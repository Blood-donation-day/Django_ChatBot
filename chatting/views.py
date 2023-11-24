
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from ChatBot.settings import SECRET_KEY
from chatting.models import Ticket
from accounts.models import User
from .prompt import GPTPrompt
import jwt



class ChatbotView(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def post(self, request):
        '''
        acess토큰으로 유저를 검증하고 해당유저의 Ticket 모델을 불러옵니다.
        요청을 보내면 유저의 today_limit > 0 를 확인하고 크다면 today_limit -= 1 후
        gpt에게 요청을 보냅니다.
        '''
        
        access = request.COOKIES.get('access', None)
        if access is not None:
            payload = jwt.decode(access, SECRET_KEY, algorithms=['HS256'])
            pk = payload.get('user_id')
            
            ticket = Ticket.objects.get(user_id=pk)
            
            # gpt에서 응답 없을 때 티켓갯수 원복필요 이건 또 어케구현하냐고 
            if ticket.today_limit > 0:
                ticket.today_limit -= 1
                ticket.save()
            else:
                return Response({"error": "남은 무료제공 횟수가 모두 소진되었습니다. 내일 다시 시도해주세요."})

        gpt = GPTPrompt()
        res = gpt.get_response()
        
        return Response({
            '대답': res,
            "today_limit": ticket.today_limit,
            }, status=status.HTTP_200_OK)
