from typing import Any, List

from fastapi import APIRouter, Depends, Response, status, Query
from starlette.responses import StreamingResponse

from src.schemas.storeFIle_schema import TransformPayload
from src.services.dataProcessing_service import DataProcessingService, getDataProcessingInstance

router = APIRouter(prefix="/fabricAir/api", tags=["DataProcess"])


@router.get(include_in_schema=True, path="/visualize/{fileId}", status_code=200)
async def getVisualizeData(fileId: str, chart_type: str = Query(...), columns: List[str] = Query(...),
                           data_service: DataProcessingService = Depends(getDataProcessingInstance)) -> Any:
    response = await data_service.getVisualizeData(fileId=fileId, chart_type=chart_type, columns=columns)
    if not response:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    return StreamingResponse(response, media_type="image/png")


@router.post(include_in_schema=True, path="/transform/{fileId}", status_code=200)
async def transformFile(transform_payload: TransformPayload, fileId: str,
                        data_service: DataProcessingService = Depends(getDataProcessingInstance)) -> Any:
    response = await data_service.transformData(transform_payload=transform_payload, fileId=fileId)
    if not response:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    return response
