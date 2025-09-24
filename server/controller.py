from server.service import RunningService
from fastapi import APIRouter

router = APIRouter()
service = RunningService()


@router.get("/running")
def get_running():
    return service.preprocess_data()
