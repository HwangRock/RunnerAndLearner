from server.service import RunningService
from fastapi import APIRouter

router = APIRouter()
service = RunningService()


@router.get("/running")
def get_running():
    return service.preprocess_running_data()


@router.get("/exrunning")
def get_ex_running():
    return service.preprocess_ex_running_data()
