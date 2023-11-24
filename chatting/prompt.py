import openai, jwt, os
from dotenv import load_dotenv
load_dotenv()


client =openai.OpenAI(
    api_key=os.environ.get('OPENAI_API_KEY')
)

class GPTPrompt:
    
    def __init__(self):
        self.model = 'gpt-3.5-turbo'
        self.messages = []
        self.max_tokens = 2048
        self.stop = None
        self.temperature = 0.3

        self.message_setting()
        
    def message_setting(self):

        self.messages.append({"role": "system", "content": "너는 음식 메뉴를 추천해주고 레시피와 재료를 알려주는 훌륭한 요리사야. 사용자가 요구한 옵션에 맞춰 추천 메뉴와 재료, 레시피를 알려줘. 특히 재료는 반드시 1인분을 기준으로 정확한 계량값을 포함해서 소개해줘"})
        self.messages.append({"role": "system", "content": "필터가 없으면 자동으로 메뉴와 레시피를 추천해줘. 필터는 난이도, 테마, 타입, 재료, 레시피 그리고 사용자가 직접 입력한 항목이야."})
        self.messages.append({"role": "system", "content": "답변은 반드시 JSON 형식으로 줘. 추천메뉴: 메뉴, 소개: 간단한 소개, 재료: 재료, 레시피: 레시피 형식으로 줘. 재료는 반드시 1인분 기준 정확한 계량값, 숫자를 포함해줘 알려줘."})
        self.messages.append({"role": "system", "content": "{난이도: None, 테마: 간식, 타입: None, 재료: None, 레시피: None, 직접 입력: 간식 추천해줘.} 등 필터에 None이 들어가면 해당 부분은 고려하지 않고 추천 메뉴를 만들어줘, 재료는 반드시 1인분을 기준으로 정확한 계량값, 수치를 포함해서 알려줘."})
        # self.messages.append({"role": "user", "content": "{난이도: None, 테마: 메인요리, 타입: 중식, 재료: None, 레시피: None, 직접 입력: None}"})
        # self.messages.append({"role": "assistant", "content": "{\n  \"추천메뉴\": \"짜장면\",\n  \"소개\": \"짜장면은 중식 요리 중 가장 유명한 메뉴 중 하나로, 면과 매운 간장 소스가 특징입니다.\",\n  \"재료\": [\n    \"면\",\n    \"돼지고기\",\n    \"양파\",\n    \"당근\",\n    \"양배추\",\n    \"식용유\",\n    \"간장\",\n    \"설탕\",\n    \"식초\",\n    \"소금\",\n    \"후추\"\n  ],\n  \"레시피\": [\n    \"1. 돼지고기를 잘게 썬 후 식용유에 볶아주세요.\",\n    \"2. 양파, 당근, 양배추를 채 썰어주세요.\",\n    \"3. 냄비에 식용유를 두르고 양파, 당근, 양배추를 볶아주세요.\",\n    \"4. 면을 삶아주세요.\",\n    \"5. 볶은 돼지고기와 볶은 야채를 넣고 간장, 설탕, 식초, 소금, 후추로 간을 맞춰주세요.\",\n    \"6. 삶은 면을 넣고 잘 섞어주세요.\",\n    \"7. 완성된 짜장면을 그릇에 담아 즐겨주세요.\"\n  ]\n}"})
        
        
        
        # # self.messages.append({"role": "user", "content":"{난이도: None, 테마: 메인요리, 타입: 중식, 재료: None, 레시피: None, 직접 입력: 짜지않은 중식 추천해줘}")
        # self.messages.append({"role": "user", "content":"{난이도: None, 테마: 메인요리, 타입: 중식, 재료: None, 레시피: None, 직접 입력: 짜지않은 중식 추천해줘}")
        

        
    def add_prompt(self, prompt):
        self.messages.append({"role": "user", "content": prompt})
        
    def message_check(self):
        print(self.messages)
    
    def get_response(self):
        completions = client.chat.completions.create(
            model = self.model,
            messages = self.messages,
            max_tokens= self.max_tokens,
            stop= self.stop,
            temperature= self.temperature,
        )
        if 'error' in completions:
            self.error = completions.error
            return self.error.message
        response = completions.choices[0].message.content.strip()
        return response