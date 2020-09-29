# deployment
배포를 위해 필요한 쿠버네티스 관련 yaml 파일들이 정리되어 있다. 테스트환경은 staging 폴더에, 배포환경은 production 폴더에 작성하고 현재는 production 만 운영하고 있다.

## 1. 간단한 배포과정
### 1. 만약 처음 배포를 진행하는것이라면 각각의 레이어에 필요한 환경변수 (secret) 들을 먼저 세팅해준다.
```sh
# secret 생성 예제
sudo kubectl create secret generic was-production-env --from-env-file=production.env --dry-run=client -o yaml | sudo kubectl apply -f - -n knufesta2019
```

### 2. 개발이 끝난 버전의 이미지를 빌드한다.
```sh
# 예제
docker build -t your_image:${TAG} .
```

### 3. 쿠버네티스 yaml의 파일들의 apply를 진행한다.
```sh
# apply 예제
export TAG=your_version
envsubst < ./was.yaml | sudo kubectl apply -f - -n knufesta2019
```

### 3-1. 필요에 따라 마이그레이션이나 정적파일 패포를 위한 job을 apply 한다.
```sh
# apply 예제
export TAG=your_version
envsubst < ./YOUR_VERSION/jobs.yaml | sudo kubectl apply -f - -n knufesta2019
```

## 2. kubernetes yaml 파일 예시
```production/database.yaml``` [<a href="production/database.yaml">이동</a>] 데이터베이스 관련 yaml<br/>

```production/was.yaml``` [<a href="production/was.yaml">이동</a>] 웹 어플리케이션 관련 yaml<br/>

```production/2.0.4/jobs.yaml``` [<a href="production/2.0.4/jobs.yaml">이동</a>] 2.0.4 버전 Jobs 예시<br/>