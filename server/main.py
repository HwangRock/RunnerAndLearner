from fastapi import FastAPI
from server.presentation.api.controller import router

# 서버 실행 명령어
# uvicorn server.main:app --reload

app = FastAPI()
app.include_router(router)
