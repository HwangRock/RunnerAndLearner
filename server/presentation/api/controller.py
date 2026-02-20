from server.application.service import RunningService
from fastapi import APIRouter

router = APIRouter()
service = RunningService()

@router.get("/dashboard")
def get_dashboard():
    return service.preprocess_response_data()
