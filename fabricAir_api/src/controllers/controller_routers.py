from fastapi import APIRouter

from src.controllers import file_controller, dataProcessing_controller

api_router = APIRouter()

api_router.include_router(file_controller.router)
api_router.include_router(dataProcessing_controller.router)
