# Python 3.9 버전을 베이스 이미지로 사용
FROM python:3.9

# 작업 디렉토리를 /usr/src/app으로 설정
WORKDIR /usr/src/app

# 필요한 패키지들을 설치
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# 애플리케이션 소스 코드를 복사
COPY . .

# 애플리케이션이 사용할 포트를 지정
EXPOSE 8080

# 애플리케이션 실행
CMD [ "python", "./run.py" ]

