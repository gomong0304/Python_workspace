from urllib.request import Request

from fastapi import FastAPI
from pydantic import BaseModel
# 데이터 유효성 검사와 설정 관리에 사용되는 라이브러리 (모델링이 쉽고 강력함)
from starlette.middleware.base import BaseHTTPMiddleware
# 요청과 응답 사이에 특정 작업 수행
# 미들웨어는 모든 요청에 대해 실행되며, 요청을 처리하기 전에 응답을 반환하기 전에 특정 작업을 수행할 수 있음
# 예를 들어 로깅, 인증, cors처리, 압축 등...
import logging # 로깅 처리용 메서드

app = FastAPI( # java -> new Fast();
    title = "MBC AI Study",
    description = "MBC AI Study",
    version = "0.0.1",
    docs_url=None, # http://localhost:8000/docs 보안상 None 처리
    redoc_url=None # http://localhost:8000/redoc 보안상 None 처리
)

class LoggingMiddleware(BaseHTTPMiddleware): # 로그를 콘솔에 출력하는 용도
    logging.basicConfig(level=logging.INFO) # 로그 출력 추가
    async def dispatch(self, request: Request, call_next):
        logging.info(f"Req: {request.method}-{request.url}")
        response = await call_next(request)
        logging.info(f"Status Code: {response.status_code}")
        return response
app.add_middleware(LoggingMiddleware) # 모든 요청에 대해 로그를 남기는 미들웨어 클래스를 사용함

class Item(BaseModel): # item 객체 생성 (BaseModel : 객체연결 -> 상속)
    name : str # 상품명 : 문자열
    description : str = None # 상품설명 : 문자열 (Null)
    price: float # 가격 : 실수형
    tax: float = None # 세금 : 실수형 (null)

@app.post("/items") # post 메서드용 요청 (create)
async def create_item(item: Item):
    # BaseModel 은 데이터 모델링을 쉽게 도와주고 유효성 검사도 수행
    # 잘못된 데이터가 들어오면 422 오류코드를 반환
    return item

@app.get("/") # get 엔드포인트
async def read_root():
    return {"Hello": "World"}


@app.post("/items/{item_id}")
async def read_item(item_id: int, q: str=None):
    return {"item_id": item_id, "q": q}