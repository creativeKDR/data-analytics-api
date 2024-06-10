from sqlalchemy.orm import Session

from src.models.storeFile import StoreFile
from src.repositories.base import CRUDBase


class StoreFileRepository(CRUDBase):
    def __init__(self):
        super().__init__(StoreFile)

    async def getFileById(self, db: Session, fileId: str):
        # Fetching file by using fileId
        return await self.get(db=db, id=fileId)

    async def create_data(self, db: Session, obj_in) -> StoreFile:
        # Creating record on StoreFile Table
        dbObj = StoreFile(**obj_in)
        db.add(dbObj)
        db.commit()
        return dbObj.ID

