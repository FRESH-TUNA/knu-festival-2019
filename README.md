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

## 2. 작동 환경
* Python : 3.6.4
* Django : 2.2.4


## 3. 웹서비스 주요기능
1. 라인업, 타임테이블, 이벤트 정보를 제공한다.
2. 푸드트럭 및 부스 정보를 제공한다.
3. 술친구 찾기 및 분실물 찾기 게시판 기능을 제공한다.
4. 푸드트럭 사장님들을 위한 admin 페이지를 제공한다.

## 4. 주요 소스 코드
### 1. 도커를 활용한 개발, 배포 환경
```/web/docker/dev/Dockerfile``` [<a href="/web/docker/dev/Dockerfile">이동</a>] 개발 환경을 위한 이미지<br/>
```/web/dev/docker-compose.yml``` [<a href="/web/dev/docker-compose.yml">이동</a>] 개발 환경 작동 파일<br/>
```/web/festival/settings/development.py``` [<a href="/web/festival/settings/development.py">이동</a>] 개발 settings
<br/><br/>
```/docker-compose/prod/docker-compose.yml``` [<a href="/docker-compose/prod/docker-compose.yml">이동</a>] 배포 환경 작동파일<br/>
```/web/festival/settings/development.py``` [<a href="/web/festival/settings/development.py">이동</a>] 배포 settings
<br/><br/>
```/pipeline_open.sh``` [<a href="/pipeline_open.sh">이동</a>] 배포 파이프라인

<br/><br/>
```/pipeline_open.sh``` [<a href="/deploy.sh">이동</a>] blue, green 배포 스크립트

## 5. 파이프라인
1. master 브랜치에 푸시한다.
2. github가 docker hub로 hook을 보낸다.
3. docker hub에서 이미지를 빌드한후 jenkins로 hook을 보낸다.
4. jenkins에서 /pipeline_open.sh을 실행한다.
5. deploy.sh를 실행하여 blue, green 배포를 실행한다.