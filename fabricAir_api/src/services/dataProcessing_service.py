import datetime
import io
from typing import Optional

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from fastapi import HTTPException
from requests import Session

from src.db.session import get_db_session
from src.repositories.storeFile_repository import StoreFileRepository
from src.schemas.storeFIle_schema import TransformPayload
from src.utils.utilities import Utilities


def getDataProcessingInstance():
    return DataProcessingService(fileRepository=StoreFileRepository())


class DataProcessingService:

    def __init__(self, fileRepository: StoreFileRepository):
        self.df = None
        self.readableFileId = None
        self.fileRepository = fileRepository

    def readAndSetFileData(self, fileBlob, fileId):
        # reading the file and store ot to data frame
        self.readableFileId = fileId
        try:
            self.df = pd.read_csv(io.BytesIO(fileBlob), encoding='utf-8')
        except UnicodeDecodeError:
            self.df = pd.read_csv(io.BytesIO(fileBlob), encoding='latin1')

    def getFileData(self):
        # get df data
        return self.df

    def getSummaryData(self):
        # it will fetch summary of each column
        summary = {}
        for column in self.df.columns:
            # if column type is numeric then only it will calculate mean, median and std_dev
            summary[column] = {
                "mean": self.df[column].mean() if self.df[column].dtype.kind in 'iufc' else None,
                "median": self.df[column].median() if self.df[column].dtype.kind in 'iufc' else None,
                "std_dev": self.df[column].std() if self.df[column].dtype.kind in 'iufc' else None,
                "data_type": str(self.df[column].dtype)
            }
        return {"summary": summary}

    @get_db_session
    async def transformData(self, transform_payload: TransformPayload, fileId: str, db: Optional[Session] = None):
        global dataObj
        if self.readableFileId != fileId:
            # if fileId not read earlier then it will fetch from db and store in df
            file = await self.fileRepository.getFileById(db=db, fileId=fileId)
            if not file:
                raise HTTPException(status_code=404, detail=f"File not found")
            fileId = file.ID
            self.readAndSetFileData(fileBlob=file.FileBlob, fileId=fileId)

        try:
            transformed_df = await normalizeData(self.getFileData(), transform_payload.transformations)
            fileblob = df_to_binary(transformed_df)
            dataObj = data_to_store_db(fileBlob=fileblob, fileId=fileId)
        except Exception as e:
            print("Failed to normalize the file, exceptions: ", str(e))

        if dataObj:
            storeFileId = await self.fileRepository.create_data(db=db, obj_in=dataObj)
            return {"message": "Transformations applied successfully", "file_id": storeFileId}
        else:
            raise HTTPException(status_code=404, detail=f"File not found")

    @get_db_session
    async def getVisualizeData(self, fileId: str, chart_type: str, columns: list, db: Optional[Session] = None):
        # fetching the file based on file Id
        file = await self.fileRepository.getFileById(db=db, fileId=fileId)
        if not file:
            raise HTTPException(status_code=404, detail=f"File not found")
        self.readAndSetFileData(fileBlob=file.FileBlob, fileId=file.ID)
        # plotting the chart based on char_type
        if chart_type == 'Histogram':
            return await plot_chart(df=self.getFileData(), columns=columns, isHistogram=True)
        elif chart_type == 'Scatter':
            return await plot_chart(df=self.getFileData(), columns=columns)
        else:
            return "Invalid Chart Type"


async def normalizeData(df, payload):
    # Applying normalization method for the numerical columns only
    for column in df.columns:
        if df[column].dtype.kind in 'iufc' and column in payload.normalize:
            df[column] = (df[column] - df[column].min()) / (df[column].max() - df[column].min()) # normalization formula

    # Filling missing values
    for column, value in payload.file_missing.items():
        df[column].fillna(value, inplace=True)

    return df


def df_to_binary(df):
    # converting the data frame into a blob to store in db
    output = io.BytesIO()
    df.to_csv(output, index=False)
    return output.getvalue()


def data_to_store_db(fileBlob, fileId):
    # preparing data to store in StoreFile table
    return {
        "ID": Utilities.generateUUID(),
        "FileName": "transformed-file-" + str(Utilities.generateTimestampId()),
        "FileBlob": fileBlob,
        "CreatedAt": datetime.datetime.utcnow(),
        "IsProcessed": True,
        "OriginalFileID": fileId
    }


# generating plots based on isHistogram flag
async def plot_chart(df: pd.DataFrame, columns: list, isHistogram: Optional[bool] = None):
    output = io.BytesIO()
    fig, ax = plt.subplots(figsize=(8, 6))

    if isHistogram:
        if len(columns) == 1:
            if columns[0] not in df.columns:
                raise HTTPException(status_code=404, detail=f"Column 'invalid_column' not found")
            # Plotting a basic histogram
            plt.hist(df[columns[0]], bins=30, color='skyblue', edgecolor='black')

            # Adding labels and title
            plt.xlabel(columns[0])
            plt.ylabel('Frequency')
            plt.title(f'Histogram of {columns[0]}')
        else:
            raise HTTPException(status_code=404, detail=f"Histogram plot requires exactly 1 columns")

    else:
        if len(columns) == 2:
            for column in columns:
                if column not in df.columns:
                    raise HTTPException(status_code=404, detail=f"Column 'invalid_column' not found")

            colors = np.random.rand(len(df))
            sizes = 100 * np.random.rand(len(df))
            # Plotting a basic scatter plot
            plt.scatter(df[columns[0]], df[columns[1]], c=colors, s=sizes, alpha=0.7, cmap='viridis')

            # Add title and axis labels
            plt.title(f"{columns} Scatter Plot")
            plt.xlabel(columns[0])
            plt.ylabel(columns[1])

            # Display color intensity scale
            plt.colorbar(label='Color Intensity')

        else:
            raise HTTPException(status_code=404, detail=f"Scatter plot requires exactly 2 columns")

    plt.savefig(output, format='png')
    plt.close(fig)
    output.seek(0)
    return output
