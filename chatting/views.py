
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from ChatBot.settings import SECRET_KEY
from chatting.models import Ticket
from accounts.models import User
import openai, jwt, os
from dotenv import load_dotenv
load_dotenv()


client =openai.OpenAI(
    api_key=os.environ.get('OPENAI_API_KEY')
)


class ChatbotView(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def post(self, request):
        '''
        acess토큰으로 유저를 검증하고 해당유저의 Ticket 모델을 불러옵니다.
        만약 updated_at 필드가 오늘과 다르면 today_limit를 5로 설정합니다.
        요청을 보내면 유저의 today_limit > 0 를 확인하고 크다면 today_limit -= 1 후 
        로직을 진행합니다. 
        다음은 뭐해야되냐 .... 아직 수정중 
        '''
        
        access = request.COOKIES.get('access', None)
        if access is not None:
            payload = jwt.decode(access, SECRET_KEY, algorithms=['HS256'])
            pk = payload.get('user_id')
            
            ticket = Ticket.objects.get(user_id=pk)
            
            # api에러 났을때 티켓갯수 수정필요
            if ticket.today_limit > 0:
                ticket.today_limit -= 1
                ticket.save()
            else:
                return Response({"error": "남은 무료제공 횟수가 모두 소진되었습니다. 내일 다시 시도해주세요."})
            
        # prompt = request.data.get('prompt', '테스트')
        # completions = client.chat.completions.create(
        #     model="gpt-3.5-turbo",
        #     # messages=[
        #     #     {"role": "system", "content": "You are a helpful assistant."},
        #     #     {"role": "user", "content": "What are some famous astronomical observatories?"}
        #     #     {"role": "assistant", "content": "What are some famous astronomical observatories?"}
        #     # ]

        #     messages=[
        #         {"role": "system", "content": "너는 요리를 추천해주고 레시피와 재료를 알려주는 훌륭한 요리사야. 사용자가 요구한 옵션에 맞춰 추천 요리와 재료, 레시피를 알려줘"},
        #         {"role": "user", "content": "What are some famous astronomical observatories?"},
        #         {
        #             "role": "user",
        #             "content": prompt,
        #         },
        #     ],
        #     max_tokens=1024,
        #     stop=None,
        #     temperature=0.5,
        # )
        # response = completions.choices[0].message.content.strip()
        

        # conversation = {'prompt': prompt, 'response': response}
        
        '''
        filter: {
            diffculty:{초급, 중급, 고급}
            theme:{메인요리, 간식, 간단요리, 초대요리, 향토음식, 겨울음식, 여름음식, 유아식},
            type:{한식, 중식, 일식, 양식},
            ingredients:{소고기, 돼지고기, 닭고기, 육류, 채소류, 쌀, 밀가루, 버섯류, 과일류, 콩/견과류, 곡류}
            recipes:{볶음, 끓이기, 찜, 무침, 굽기, 회, 절임}
            etc:{직접입력: 최대 50글자.}
        }
        '''
        
        
        
        return Response({
            'conversation':"테스트용",
            "today_limit": ticket.today_limit,
            }, status=status.HTTP_200_OK)
