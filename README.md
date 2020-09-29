# 2019 강원대학교 축제사이트, 머동머동!
![](./knufestival.jpg)
<br/>
<a href="http://www.knufesta2019.de/">http://www.knufesta2019.de/</a>
## 1. 만든사람들
기서연 - 강원대 멋사 7기, 프론트엔드 개발 및 디자인<br/>
김동원 - 강원대 멋사 7기, 풀스택 개발 및 PM<br/>
박도현 - 강원대 멋사 7기, 백엔드 개발<br/>
박지원 - 강원대 멋사 7기, 배포 <br/>
백지연 - 강원대 멋사 7기, 프론트엔드 개발 및 디자인<br/>
손명진 - 강원대 멋사 7기, 프론트엔드 개발<br/>
오정우 - 강원대 멋사 7기, 백엔드 개발<br/>
이인배 - 강원대 멋사 7기, 프론트엔드 개발<br/>
하준혁 - 강원대 멋사 7기, 프론트엔드 개발 및 고문<br/>

## 2. 웹서비스 주요기능
1. 라인업, 타임테이블, 이벤트 정보를 제공한다.
2. 푸드트럭 및 부스 정보를 제공한다.
3. 술친구 찾기 및 분실물 찾기 게시판 기능을 제공한다.
4. 푸드트럭 사장님들을 위한 admin 페이지를 제공한다.

## 3. 개발, 운영 환경
개발, 운영 환경 모두 Docker를 사용하여 이미 만들어진 이미지를 활용하거나 필요한 명령어들을 자동화시켜 환경구축을 빠르게 할수 있도록 했다.
또한 여러 컨테이너를 쉽게 연동할수 있도록 docker-compose를 사용했다.

### 1. 개발환경
postgresql 데이터베이스, Django가 제공하는 개발용 WAS의 2-layer 구성으로 되어있다.

### 2. 운영환경
postgresql 데이터베이스, gunicorn WAS, nginx web server 의 3-layer 구성으로 되어있다.

## 3. 개발환경 시작하기
개발환경을 시작하기전에 docker와 docker-compose의 설치가 필요하다. 다음 공식문서를 참고해 서버나 PC에 설치해준다.
<a href="https://docs.docker.com/engine/install/ubuntu/">https://docs.docker.com/engine/install/ubuntu/</a>
<a href="https://docs.docker.com/compose/install/">https://docs.docker.com/compose/install/</a>

docker와 docker-compose를 설치한후 다음명령어를 시작하면 개발환경이 구축되고 실행된다.

```sh
chmod 700 ./init
./init
```

한번 ./init 을 실행했다면 다시 실행해줄 필요는 없고 다음명령어로 개발환경을 시작할수 있다.
```sh
docker-compose up
```

## 4. 프로젝트 환경 관련 폴더
### 1. config
서비스를 위한 설정값들이 담겨 있다.
<br>
[<a href="/config">config 폴더 이동</a>]

### 2. deployment
배포를 위한 쿠버네티스 설정 파일들이 담겨있다.<br>
[<a href="/deployment">deployment 폴더 이동</a>]

### 3. docker
개발, 배포 환경 구성을 위한 도커 파일들이 담겨있다.<br>
[<a href="/docker">docker 폴더 이동</a>]

### 4. envs
개발 환경에 필요한 환경변수들이 담길 폴더<br>
[<a href="/envs">docker 폴더 이동</a>]

## 5. 프로젝트 기능 관련 폴더
### 1. base 
앱들에 공통적으로 쓰이는 로직, 템플릿이 담겨있다.<br>
[<a href="/base">base 폴더 이동</a>]

### 2. foodtruck
푸드트럭 정보 제공을 위한 앱<br>
[<a href="/foodtruck">foodtruck 폴더 이동</a>]

### 3. friendboard
술친구를 구할수 있는 기능을 제공하는 앱<br>
[<a href="/friendboard">friendboard 폴더 이동</a>]

### 4. index
메인 페이지를 제공하는 앱<br>
[<a href="/index">index 폴더 이동</a>]

### 5. lostboard
분실물을 찾을수 있는 기능을 제공하는 앱<br>
[<a href="/lostboard">lostboard 폴더 이동</a>]
