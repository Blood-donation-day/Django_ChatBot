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

#### JWT토큰으로 사용자 인증과정

#### GPTAPI 요청

### 마치며

<!--

프론트 필요한것들 시간없으면 밑에있는건 포기

chatroom생성
charroom 저장
마이페이지
로그인버튼 /로그아웃버튼 토글

게시판

비밀번호변경 페이지

회원탈퇴

마이페이지 접속시 무한요청



/ 메뉴 /  내정보 /



오늘의 요리

카테고리

난이도
 초급 중급 고급

테마?
메인요리, 밑반찬, 간식, 간단요리, 초대요리, 향토음식, 겨울음식, 여름음식

음식 분류

한식, 중식, 일식, 양식

4재료

소고기, 돼지고기, 닭고기, 해물, 채소류, 버섯류, 과일류,

5요리방법

볶음, 끓이기, 튀김, 비비기, 굽기, 회, 무침

기록  모두

저장(즐겨찾기)  선택한거만


기존에 장고에서 쿠키값으로 토큰을 지정했는데 깃허브페이지 프론트에서 쿠키값을 가져오지 못하는 문제발생 (도메인 이 깃허브페이지와 달라 쿠키에 접근하지 못함)

백에서 response로 토큰값을 주고 프론트에선 로컬스토리지에 저장하는걸로 변경
깃허브페이지 프론트에서 로컬에 테스트 완료


리프레쉬 토큰으로 재발급하는 과정에서 Authorizatio에 리프레쉬 토큰값을넣어 전송해봄
Authorization 에는 엑세스토큰값만 들어갈 수 있음. 리프레쉬 토큰값 넣으면 에러
리프레쉬 토큰은 post로 빼고 body에 싣어서 보내는 방식으로 변경


그러나 lightsail 서버가 http라서 Mixed content 문제
서버에 https를 적용하기위해 certbot사용해서 ssl인증하려고 시도

>> 생 ip주소는 안돼고 도메인을 입력해야함
>> route53에서 도메인 구매 후 등록
https를 얻게됨

그런데 이렇게 되니 쿠키의 값이 전송되고

 -->
