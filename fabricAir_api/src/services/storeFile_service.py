import datetime
from typing import Any, Optional

from fastapi import UploadFile, File, HTTPException
from requests import Session

from src.db.session import get_db_session
from src.repositories.storeFile_repository import StoreFileRepository
from src.services.dataProcessing_service import getDataProcessingInstance
from src.utils.utilities import Utilities


def getStoreFileInstance():
    return StoreFileService(repository=StoreFileRepository(), dataService=getDataProcessingInstance())


class StoreFileService:

    def __init__(self, repository: StoreFileRepository, dataService: getDataProcessingInstance):
        self.repository = repository
        self.dataService = dataService

    @get_db_session
    async def getFileByID(self, fileId: str, db: Optional[Session] = None) -> Any:
        # fetching the file based on fileId
        file = await self.repository.getFileById(db=db, fileId=fileId)
        if not file:
            raise HTTPException(status_code=404, detail=f"File not found")
        self.dataService.readAndSetFileData(fileBlob=file.FileBlob, fileId=fileId)
        # calculate the summary
        response = self.dataService.getSummaryData()
        return response

    @get_db_session
    async def saveStoreFile(self, fileData: UploadFile = File(...), db: Optional[Session] = None) -> Any:
        # reading the blob data
        content = await fileData.read()
        # preparing the data to store in StoreFile table
        obj_in = {
            "ID": Utilities.generateUUID(),  # generating unique identifier
            "FileName": fileData.filename,
            "FileBlob": content,
            "CreatedAt": datetime.datetime.utcnow(),
            "IsProcessed": False
        }
        response = await self.repository.create_data(db=db, obj_in=obj_in)
        return {"message": "File uploaded successfully", "file_id": response}
