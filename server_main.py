from fastapi import FastAPI
from server.controller import router

# 서버 실행 명령어
# v

app = FastAPI()
app.include_router(router)
