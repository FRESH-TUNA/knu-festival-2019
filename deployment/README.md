# deployment
배포를 위해 필요한 docker-compose 파일들이 버전별로 정리되어있는 폴더이다.

## 1. 간단한 배포과정
만약 처음 배포를 진행하는것이라면 데이터베이스를 위한 볼륨을 생성해줘야하고 환경에 따라  다음명령어를 입력하여 볼륨을 생성할수 있다.
```sh
# 테스트환경 볼륨
docker volume create database.staging.knufesta2019

# 실제 환경 볼륨
docker volume create database.production.knufesta2019
```

버전과 환경에 맞는 docker-compose.yaml파일을 찾아서 이미지를 빌드한다. 혹은 이미 레지스트리에 있다면 풀을 받아준다.
```sh
# 이미지 빌드
docker-compose -f deployment/production/1.0.0/docker-compose.yaml build

# 이미지 풀받기
docker-compose -f deployment/production/1.0.0/docker-compose.yaml pull
```

배포되는 컨테이너에 필요한 환경변수 파일도 생성해줘야한다. 환경변수 파일의 이름은 위에서 사용했던 docker-compose.yaml 파일의 env_file을 통해 알수 있다 (일반적으로 *.env의 형식을 가진다). 프로젝트 루트 폴더 기준으로 다음위치에 환경변수 파일을 작성하거나 관리자로부터 받아서 복사해준다.
이미 환경변수가 있다면 이과정은 넘어가도 좋다.
```sh
# 테스트 환경변수
touch database/env/.staging/[환경변수 파일이름]

# 실제 환경변수
touch database/env/.production/[환경변수 파일이름]
```

모든과정이 끝났다면 다음명령어를 통해 운영환경을 시작할수 있다.
```sh
# 예제
docker-compose -f deployment/production/1.0.0/docker-compose.yaml up -d
```
## 2. docker-compose 파일 예시
```/deployment/staging/1.0.0/docker-compose.yaml``` [<a href="/deployment/staging/1.0.0/docker-compose.yaml">이동</a>] 테스트 환경 구동을 위한 docker-compose<br/>

```/deployment/production/1.0.0/docker-compose.yaml``` [<a href="/deployment/production/1.0.0/docker-compose.yaml">이동</a>] 배포 환경 구동을 위한 docker-compose<br/>