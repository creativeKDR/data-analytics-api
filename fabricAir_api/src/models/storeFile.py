from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Unicode, Column, LargeBinary
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER, DATETIME2, BIT, VARBINARY

Base = declarative_base()
metadata = Base.metadata


class StoreFile(Base):
    __tablename__ = 'StoreFile'

    ID = Column(UNIQUEIDENTIFIER, primary_key=True)
    FileName = Column(Unicode(100), nullable=False)
    FileBlob = Column(VARBINARY, nullable=False)
    CreatedAt = Column(DATETIME2)
    IsProcessed = Column(BIT, nullable=True)
    OriginalFileID = Column(UNIQUEIDENTIFIER, nullable=True)

