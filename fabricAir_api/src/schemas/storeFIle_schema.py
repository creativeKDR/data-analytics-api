from datetime import datetime
from typing import Union, List, Dict
from uuid import UUID

from pydantic import BaseModel, Field


class StoreFileCreate(BaseModel):
    id: Union[str, UUID] = Field(None, alias='ID')
    fileName: str = Field(None, alias='FileName')
    fileBlob: bytes = Field(None, alias='FileBlob')
    createdAt: datetime = Field(None, alias='CreatedAt')
    isProcessed: bool = Field(None, alias='IsProcessed')
    originalFileId: Union[str, UUID] = Field(None, alias='OriginalFileID')

    class Config:
        orm_mode = True
        name = "StoreFile"
        allow_population_by_field_name = True


class SummaryResponse(BaseModel):
    summary: dict

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class Transform(BaseModel):
    normalize: List[str] = []
    file_missing: Dict[str, Union[int, float, str]] = {}


class TransformPayload(BaseModel):
    transformations: Transform

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
