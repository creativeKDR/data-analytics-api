from typing import Any

from fastapi import APIRouter, Depends, Response, status, UploadFile, File

from src.schemas.storeFIle_schema import StoreFileCreate, SummaryResponse
from src.services.storeFile_service import StoreFileService, getStoreFileInstance

router = APIRouter(prefix="/fabricAir/api", tags=["FileHandler"])


@router.get(include_in_schema=True, path="/summary/{fileId}", status_code=200, response_model=SummaryResponse)
async def getSummaryOfFile(fileId: str, file_service: StoreFileService = Depends(getStoreFileInstance)) -> Any:
    response = await file_service.getFileByID(fileId=fileId)
    if not response:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    return response


@router.post(include_in_schema=True, path="/upload", status_code=200)
async def uploadFile(fileData: UploadFile = File(...), file_service: StoreFileService = Depends(getStoreFileInstance)) -> Any:
    response = await file_service.saveStoreFile(fileData=fileData)
    if not response:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    return response
