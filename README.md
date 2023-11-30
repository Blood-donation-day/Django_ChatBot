# ChatBot with Django_DRF

## 요구사항에 맞게 음식을 추천해주는 AI음식추천 서비스

FE repo: https://github.com/Blood-donation-day/Django_Chat-FE

## 목차

[1. 목표와 기능](#1-목표와-기능)<br>
[2. 개발 환경 및 배포 URL](#2-개발-환경-및-배포-url)<br>
[3. 개발 일정](#3-프로젝트-구조와-개발-일정)<br>
[4. 데이터베이스 모델링(ERD)](#4-데이터베이스-모델링erd)<br>
[5. URL 구조](#5-url-구조)<br>
[6. UI](#6-ui)<br>
[7. 기능 요구사항 목록](#7-기능-요구사항-목록)<br>
[8. 개발하면서 느낀 점](#8-개발과정과-느낀점)<br>

## 1. 목표와 기능

### 1-1. 목표

- GPT API를 활용하여 사용자의 요구사항을 기반으로 한 음식 추천 서비스 개발
- Django REST framework를 활용하여 백엔드 설계
- JWT(JSON Web Token)를 사용하여 사용자 인증 및 보안 강화
- 각 사용자에 대한 일일 API 요청 횟수 제한 설정 (최대 5회)

### 1-2. 기능

- 사용자 인증 및 권한 부여를 위한 엑세스 토큰 및 리프레시 토큰 기능
- GPT API를 활용하여 음식 추천 요청에 대한 응답 처리
- 자동으로 추천메뉴와 알맞는 사진을 제공하는 기능
- 검색을 통해 키워드가 포함된 음식만 볼 수 있는 기능

## 2. 개발 환경 및 배포 URL

#### [FrontEnd]

<div>
    <img src="https://img.shields.io/badge/html5-E34F26?style=for-the-badge&logo=html5&logoColor=white">
    <img src="https://img.shields.io/badge/css3-1572B6?style=for-the-badge&logo=css3&logoColor=white">
    <img src="https://img.shields.io/badge/javascript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=white">
    <img src="https://img.shields.io/badge/Tailwind-06B6D4?style=for-the-badge&logo=tailwindcss&logoColor=white">
    
</div>

#### [BackEnd]

<div>
    <img src="https://img.shields.io/badge/python-3776AB?style=for-the-badge&logo=python&logoColor=white">
    <img src="https://img.shields.io/badge/django-092E20?style=for-the-badge&logo=django&logoColor=white">
</div>

#### [DataBase]

<img src="https://img.shields.io/badge/sqlite3-003B57?style=for-the-badge&logo=sqlite&logoColor=white">

### 2-2. 배포 URL

프론트엔드 페이지
https://blood-donation-day.github.io/Django_Chat-FE/

백엔드
https://blood-donation-day.com

Swagger문서
https://blood-donation-day.com/api/swagger/

## 3. 프로젝트 구조와 개발 일정

### 3.1프로젝트 구조

```
📦Django_ChatBot
 ┣ 📂accounts
 ┃ ┣ 📂migrations
 ┃ ┣ 📜admin.py
 ┃ ┣ 📜apps.py
 ┃ ┣ 📜models.py
 ┃ ┣ 📜serializers.py
 ┃ ┣ 📜tests.py
 ┃ ┣ 📜urls.py
 ┃ ┣ 📜views.py
 ┃ ┗ 📜__init__.py
 ┣ 📂ChatBot
 ┃ ┣ 📜asgi.py
 ┃ ┣ 📜settings.py
 ┃ ┣ 📜urls.py
 ┃ ┣ 📜wsgi.py
 ┃ ┗ 📜__init__.py
 ┣ 📂chatting
 ┃ ┣ 📂migrations
 ┃ ┣ 📜admin.py
 ┃ ┣ 📜apps.py
 ┃ ┣ 📜models.py
 ┃ ┣ 📜prompt.py
 ┃ ┣ 📜serializers.py
 ┃ ┣ 📜tests.py
 ┃ ┣ 📜urls.py
 ┃ ┣ 📜views.py
 ┃ ┗ 📜__init__.py
 ┣ 📂core
 ┃ ┣ 📜models.py
 ┃ ┗ 📜permissions.py
 ┣ 📂media
 ┃ ┣ 📂accounts
 ┃ ┃ ┗ 📂profile_imgs
 ┃ ┗ 📂chatting
 ┃ ┃ ┗ 📂thumbnail
 ┣ 📂static
 ┣ 📜.env
 ┣ 📜.gitignore
 ┣ 📜db.sqlite3
 ┣ 📜manage.py
 ┣ 📜README.md
 ┗ 📜requirements.txt
```

### 구성도

<img src=readme/architecture.png>

### 3.2 개발 일정

<img src=readme/WBS.png>

## 4. 데이터베이스 모델링(ERD)

<img src=readme/ERD.png>

## 5. URL 구조

#### Swagger문서

https://blood-donation-day.com/api/swagger/

|     `account`      |         URL         |  method  |
| :----------------: | :-----------------: | :------: |
|     `회원가입`     | `accounts/signup/`  |  `POST`  |
|      `로그인`      |  `accounts/login/`  |  `POST`  |
| `로그인 정보 확인` |  `accounts/login/`  |  `GET`   |
|     `로그아웃`     |  `accounts/login/`  | `DELETE` |
|     `내 정보`      | `accounts/profile/` |  `GET`   |
|  `회원정보 변경`   | `accounts/profile/` |  `POST`  |
| `엑세스토큰 갱신`  | `accounts/refresh/` |  `POST`  |

|    `chatting`    |         URL          | method |
| :--------------: | :------------------: | :----: |
|    `음식추천`    |     `chatting/`      | `POST` |
| `요청 기록 조회` | `chatting/{q}{page}` | `GET`  |
| `요청 기록 상세` |   `chatting/<pk>`    | `GET`  |

## 6. UI

#### 회원가입 / 로그인

<img src=/readme/signup.png>

#### 메인페이지

<img src=/readme/mainpage.png>

#### 요리추천 페이지

<img src=/readme/create.png>

#### 결과 페이지

<img src=/readme/gptresult.png>

#### 마이페이지

<img src=/readme/mypage.png>

#### 내 프로필

<img src=/readme/profile.png>

## 7. 기능 요구사항 목록

#### 회원가입 / 로그인

<img src='/readme/signup.gif'>

```
회원가입 및 로그인 시 엑세스토큰, 리프레시토큰을 로컬스토리지에 저장합니다.
```

#### 요리추천

<img src='/readme/create.gif'>

```
요리추천 옵션들을 선택해 요청을 보내면 AI가 추천하는 요리를 응답해줍니다.
```

#### 프로필 변경

<img src='/readme/profile.gif'>

```
프로필 변경페이지에서 닉네임, 자기소개를 변경할 수 있습니다.
```

#### 마이페이지 / 검색

<img src='/readme/search.gif'>

```
마이페이지에서 내 기록을 볼 수 있고, 검색을 통해 원하는 요리를 필터링할 수 있습니다.
```

## 8. 개발과정과 느낀점

### 8-1 개발과정

### JWT토큰으로 사용자 인증과정

jwt토큰으로 사용자 인증방식을 구현하고자 했습니다.
로그인 요청을 보내면 엑세스토큰과 리프레쉬 토큰이 쿠키에 저장되고, 다음 요청 시 쿠키에 있는 토큰값을 가져와
헤더에 싣어 보내고자 하였습니다.

```javascript
async function GetProfile() {
const response = await fetch(profileurl, {
  method: "GET",
  headers: {
    "Content-Type": "application/json",
    Authorization: "Bearer " + getCookie("access"),
  },
  credentials: "include",
});

if (response.ok) {
  const serverProfile = await response.json();
  console.log("프로필: ", serverProfile);
  Updateprofile(serverProfile);

  localStorage.setItem("Localprofiledata", JSON.stringify(serverProfile));
} else if (response.status === 401) {
  // 토큰 만료시 리프레시 토큰을 사용하여 엑세스 토큰 재발급 후 다시 요청
  await RefreshAccessToken().then(() => GetProfile());
}}
...
```

예시로 사용자 프로필을 불러오는 요청입니다.

내 쿠키에 저장되있는 엑세스토큰 값을 가져와 헤더에 포함시켜 요청을 보내고 서버에서 정상응답을 받으면 프로필을 업데이트하고, 401 토큰만료 응답이 온다면 토큰을 갱신하는 함수로 보냈습니다.

로컬 환경에서 테스트할 때는 정상적으로 작동했지만, 깃허브 페이지에서 로컬 서버로 요청을 보낼 때 에러가 발생했습니다.
<a href=https://github.com/codestates/B-log/issues/134>참고</a>

<p align="center"><img src="/readme/cookie-1.png" align="center" width="45%">
    <img src="/readme/cookie-2.png" align="center" width="45%">
   </p>

서버에서 다양한 쿠키 설정 옵션을 변경해도 문제가 해결되지 않았습니다.

문제의 주 원인은 깃허브 페이지와 로컬 서버의 도메인 차이와 HTTPS와 HTTP 프로토콜의 Mixed content 문제였습니다. 쿠키를 불러오지 못해 토큰 값이 비어있어 토큰 갱신 요청이 실패하고, 만료된 토큰으로 프로필을 불러오는 요청이 반복되었습니다.

해당 문제를 해결하기 위해 로그인 시 응답에 토큰을 포함해서 보내주고 로컬스토리지에 값을 저장하는것으로 변경하였습니다.

<details>
    <summary>Django</summary>

```python
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
            return res
        else:
            return Response(
                {'message':'이메일 혹은 비밀번호가 잘못되었습니다.'},
                status=status.HTTP_400_BAD_REQUEST
                )

```

</details>

<details>
    <summary>Javascript</summary>

```javascript
async function GetProfile() {
  try {
    // 로컬스토리지에 데이터가 있다면 먼저 화면에 불러옴
    const localProfileData = localStorage.getItem("Localprofiledata");

    if (localProfileData) {
      const localProfile = JSON.parse(localProfileData);
      Updateprofile(localProfile);
    } else {
      const profile = await getfetchUrl(profileurl);
      console.log("프로필: ", profile);

      Updateprofile(profile);
      // 받은 데이터를 로컬스토리지에 저장
      localStorage.setItem("Localprofiledata", JSON.stringify(profile));
    }
  } catch (error) {
    console.error("요청 에러:", error);
  }
}
```

</details>

#### 메서드 변경

엑세스토큰 만료 시 갱신 요청을 보내는 기존 로직입니다.

<details>
    <summary>기존로직</summary>

```python
class LoginAPIView(APIView):

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

        except(jwt.exceptions.ExpiredSignatureError):
            # 토큰 만료 시 토큰 갱신
            refresh_token = request.COOKIES.get('refresh', None)

            if refresh_token:

                refresh = RefreshToken(refresh_token)
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
```

</details>

기존에는 accounts/login 엔드포인트의 GET 메서드를 사용하여 로그인 확인과 토큰 갱신을 모두 처리했습니다.

로그인 확인 요청 시에는 엑세스 토큰의 만료 여부를 확인하고, 토큰이 만료되었다면 서버에서 새로운 엑세스 토큰을 받아와 쿠키에 저장하는 방식이었습니다.그러나 로컬 스토리지에 토큰 값을 저장하도록 변경한 후, 리프레시 토큰 값을 포함하여 서버에 요청을 보내야 했기 때문에, 이전의 GET 메서드를 POST 메서드로 변경하였습니다.

```python
class RefreshAPIView(APIView):

    def post(self, request):

        refresh_token = request.data.get('refresh', None)
        print(refresh_token)

        if refresh_token:

            refresh = RefreshToken(refresh_token)

            access = str(refresh.access_token)
            res = Response({"access": access}, status=status.HTTP_200_OK)
            res.set_cookie('access', access)

            return res
        raise jwt.exceptions.InvalidTokenError
```

<details>
    <summary>JavaScript</summary>

```javascript
async function RefreshAccessToken() {
  try {
    const response = await fetch(refreshurl, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ refresh: getToken("refresh") }),
      credentials: "include",
    });

    //리프레쉬 토큰이 만료되었다면 로그인 페이지로 이동
    if (response.status === 500) {
      return (window.location.href = loginpage);
    }

    //리프레쉬 토큰이 만료되지 않고 엑세스 토큰을 재발급하는 경우
    if (response.ok) {
      const refreshData = await response.json();
      console.log("토큰 재발급 완료", refreshData);
      const token = {
        access: refreshData.access,
        refresh: getToken("refresh"),
      };
      localStorage.setItem("token", JSON.stringify(token));

      //기타 에러 처리
    } else {
      const errorData = await response.json();
      console.error("재발급 실패", errorData.message);
    }
  } catch (error) {
    console.error("토큰 갱신 에러", error);
  }
}
```

</details>

### GPT-API 요청

요리 추천 서비스에서 각 사용자는 하루에 5개의 추천된 요리를 받을 수 있도록 서비스를 제한하고자 위 Ticket이라는 새로운 모델을 만들었습니다. User 모델과 1:1 관계를 형성하며, 각 사용자의 요청 횟수를 저장합니다.

```python
class Ticket(TimestampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ticket')
    today_limit = models.IntegerField(default=os.environ.get('TODAY_LIMIT'))
    total_used_count = models.IntegerField(default=0)

    def __str__(self):
        return f'Ticket - 남은 횟수: {self.today_limit}'
```

API 요청을 보낼 때 Ticket 모델의 updated_at 시간과 현재 날짜를 비교하여, today_limit 값을 감소시키고, 만약 0이 되면 무료 제공 횟수가 소진되었다는 에러를 발생시켰습니다. 그러나 이 방식은 한번 이상 요청을 보내면 updated_at이 업데이트되고 다음 요청에 다시 확인하는건 의미가 없어 자원의 자원의 낭비라고 생각했습니다.

```python
class LoginAPIView(APIView):

    def post(self, request):

        user = authenticate(
            email = request.data.get('email'),
            password = request.data.get('password')
        )
        ...
            if ticket.updated_at.date() != datetime.date.today() and ticket.today_limit < int(os.environ.get('TODAY_LIMIT')):
                ticket.today_limit = os.environ.get('TODAY_LIMIT')
                ticket.save()

            res = Response({
                    ...

                    'today_limit':ticket.today_limit,
                },status=status.HTTP_200_OK,)
            return res
        ...
```

방식을 변경하여 사용자가 로그인할 때 모델의 updated_at 날짜를 확인하여 today_limit 필드를 관리하도록 수정했습니다

#### 답변 저장

API에서 받은 응답을 나누어 이름, 설명, 재료, 레시피 로 db에 저장되도록 하고싶었습니다.
이를 위해 답변내용을 검증하고 각 필드로 나누도록 하였습니다.

<details>
    <summary>GPTPrompt</summary>

```python
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

    def add_prompt(self, prompt):
        self.messages.append({"role": "user", "content": str(prompt)})

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

```

</details>

```python
class ChatbotAPIView(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def post(self, request):

        access = GetToken(request)
        prompt = request.data.get('prompt', None)

        gpt = GPTPrompt()
        gpt.add_prompt(prompt)
        res = gpt.get_response()
        ...

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

        ...

        return Response({
            'Food': res,
            "today_limit": ticket.today_limit,
            }, status=status.HTTP_200_OK)

```

엑세스토큰을 받아 사용자를 검증하고, GPT-API로 promt요청을 보냅니다.
응답을 받으면 받은 응답을 메뉴, 소개, 재료, 레시피로 나누고 FoodContainer모델에 저장하였습니다.

<img src=/readme/foodcontainer.png>

#### 이미지 저장

그후 이름을 기준으로 이미지를 검색하고 저장하여 어울리는 이미지를 같이 제공하고자 하였습니다.

```python
def image_search_save(foodname, foodmodel):
    #파라미터 설정
    params = {
            "q": foodname,
            "tbm": "isch",   # 이미지 검색
    }
    html = requests.get("https://www.google.com/search", params=params,  timeout=10)

    soup = BeautifulSoup(html.content, 'html.parser')
    images = soup.select('div img')

    # 대표 이미지
    image_url = images[1]['src']

    response = requests.get(image_url)
    image_data = response.content

    #이미지 uuid로 저장
    uuid = str(uuid4())

    save_directory = os.path.join('media', 'chatting', 'thumbnail')

    # 이미지 저장
    with open(os.path.join(save_directory, f'{uuid}.png'), 'wb') as img_file:
        img_file.write(image_data)

    # 모델에 이미지 경로 저장

    foodmodel.thumbnail = os.path.join('chatting', 'thumbnail', f'{uuid}.png')
    foodmodel.save()

```

이름을 기반으로 Google 이미지 검색을 수행하고, 받아온 HTML 페이지를 BeautifulSoup로 파싱하여 이미지의 URL을 가져온 후, 해당 URL로 다시 요청을 보내 이미지를 받아옵니다. 그후 이미지를 UUID로 저장하고 DB에 해당 경로를 저장합니다.

마지막으로 GPT 응답이 올바르지 않거나 모델 생성에 실패한 경우에 대한 에러 처리를 해주었습니다.

<details>
    <summary>전체 요청 코드</summary>

```python

class ChatbotAPIView(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def post(self, request):

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

```

</details>

<img src=/readme/imagesearch.png>

### 마치며

DRF에 대해 많은 경험을 쌓게되었습니다. 한 서비스에 대해 어떻게 만들지 고민하고, 기능을 어떻게 구현할 것인지에 대한 고민이 많았습니다. 과정에서 APIView를 주로 활용했는데, 이유는 내가 생각한 기능을 직접 코드로 구현할 수 있어서 선택했습니다. 그래서 이 매서드가 어떤 역할을 하는지 쉽게 알 수 있었습니다.

직접 APIView를 주로 사용하여 구현하면서 왜 상속받은 View클래스들을 쓰는지 좀 더 이해가 갔습니다. 기존 반복되는 코드가 많았고 각 모델에데한 검증과 저장을 serialier에서 처리해줘 오류를 줄이고 간단하게 코드를 작성할 수 있는 장점이 있었습니다. 반복되는 과정을 겪으면서 왜 DRF에서 해당기능들을 제공하는지 이해할 수 있었던 기회였습니다.

아쉬운점으로 설계 단계에서 발생한 에러 때문에 해당 부분을 구현하지 못했다는 점입니다. 처음에 설계할 때 좀 더 자원을 넣었다면 원하는 기능을 구현할 수 있었을 것이라는 아쉬움이 남습니다. 이를 통해 초기 설계의 중요성을 다시 한번 깨달았습니다.

뿌듯함과 아쉬움이 남는 프로젝트였습니다. 해당 경험을 바탕으로 더 속이 알찬 프로젝트를 진행해보고 싶습니다. 끝까지 읽어주셔서 감사합니다.
