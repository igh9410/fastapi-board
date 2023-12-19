# fastapi_board


## 실행 방법

로컬 환경: git clone 이후 루트 디렉토리에서


pip install poetry -> poetry install ->  
docker compose -f docker-compose-local.yml up -d   
poetry run uvicorn app.main:app --reload  


도커 환경:

chmod +x run-docker.sh  
./run-docker.sh (리눅스 or 맥)  
