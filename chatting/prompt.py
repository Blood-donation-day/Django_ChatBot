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
        self.max_tokens = 1024
        self.stop = None
        self.temperature = 0.5

        self.message_setting()
        
    def message_setting(self):
        self.messages.append({"role": "system", "content": "너는 요리를 추천해주고 레시피와 재료를 알려주는 훌륭한 요리사야. 사용자가 요구한 옵션에 맞춰 추천 요리와 재료, 레시피를 알려줘"})
        self.messages.append({"role": "system", "content": "필터가 없으면 자동으로 메뉴와 레시피를 추천해줘. 필터는 difficulty, theme, type, ingredients, recipes 그리고 사용자가 직접 입력한 항목이야."})
        self.messages.append({"role": "user", "content":"답변은 반드시 추천메뉴:메뉴, 소개:간단한 소개, 재료: 재료, 레시피: 레시피 순서로줘"})
        self.messages.append({"role": "user", "content":"답변은 반드시 JSON형식으로 추천메뉴, 소개, 재료, 레시피 순서대로줘"})
        self.messages.append({"role": "user", "content":"filter:(difficulty: None, theme: 간식, type: None, ingredients: None, recipes: None etc: 간식추천해줘.) 등 필터에 None이 들어간 경우에는 자동으로 응답을 만들어줘"})
        self.messages.append({"role": "user", "content":"filter:(difficulty: 초급, theme: 간식, type: 중식, ingredients: 소고기, recipes: 끓이기, 무침, etc: 간단한 중식 추천해줘.)"})
        self.messages.append({
    "role": "assistant",
    "content": """
    {"추천메뉴": "소고기 무침",
    "소개": "신선한 소고기를 사용한 무침 요리로, 고추장과 함께 양념한 맛이 일품입니다. 초급자도 쉽게 따라 할 수 있는 간식 중식 메뉴입니다.",
    "재료": [
        "300g 소고기 (무침용)",
        "1/2 대 소갈비살 또는 채끝살",
        "1/2 대 당근",
        "1/2 대 오이",
        "2 tbsp 고추장",
        "1 tbsp 간장",
        "1 tbsp 설탕",
        "1 tbsp 다진 마늘",
        "1 tsp 참기름",
        "깨소금"
    ],
    "레시피": [
        "소고기는 얇게 채 썰어주세요.",
        "당근과 오이는 얇게 채 썰어주세요.",
        "팬에 기름을 두르고 다진 마늘을 볶아 향을 내줍니다.",
        "소고기를 넣고 익힌 뒤, 당근과 오이를 넣고 볶아줍니다.",
        "고추장, 간장, 설탕을 넣고 익히면서 맛을 조절합니다.",
        "마지막에 참기름을 넣고 깨소금을 뿌려 간을 맞춰줍니다."
    ]}
    """
})
        # self.messages.append({"role": "user", "content":"filter:(difficulty: None, theme: 간식, type: None, ingredients: None, recipes: None etc: 간식추천해줘.)"})
        
        
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
        response = completions.choices[0].message.content.strip()
        return response