import os
from fastapi import APIRouter, File, UploadFile, Query, HTTPException
from typing import List
import logging

from backend.data_handler import DataHandler
from fastapi.responses import JSONResponse

logging.basicConfig(level=logging.INFO)


def write_to_file(data, file_path):
    """
    Write the given data to a file at the specified file path.

    :param data: The data to be written to the file.
    :param file_path: The path where the file will be saved.
    """
    with open(file_path, "wb") as f:
        f.write(data)


class ApiEndpoints:
    def __init__(self):
        """
        Initialize the ApiEndpoints class with an APIRouter instance and register endpoints.
        """
        self.router = APIRouter()
        self.router.post("/uploadfile/")(self.upload_file)
        self.router.get("/downloadfile/")(self.download_file)
        self.router.get("/get-fg-data/")(self.get_fg_data)
        self.router.get("/get-rm-data/")(self.get_rm_data)
        self.router.get("/get-machine-data/")(self.get_machine_data)
        self.logger = logging.getLogger(__name__)
        self.data_handler = DataHandler()

    async def upload_file(self, file: UploadFile = File(...), table_name: str = ''):
        """
        Handle file upload from the client. Save the uploaded file to the server.

        :param file: The uploaded file.
        :param table_name: The name of the table for which the file is being uploaded.
        :return: JSON response with the filename, file path, and table name.
        """
        try:
            upload_dir = "uploaded_files"
            os.makedirs(upload_dir, exist_ok=True)  # Create the directory if it doesn't exist
            file_path = os.path.join(upload_dir, file.filename)
            self.logger.info("the file path is :%s", file_path)
            file_contents = await file.read()
            self.logger.info("type of data is :%s", type(file_contents))
            write_to_file(file_contents, file_path)
            self.data_handler.update_data(file_path, table_name)

            # Placeholder for processing file and storing content based on table_name
            return {
                "filename": file.filename,
                "file_path": file_path,
                "table_name": table_name
            }
        except FileNotFoundError:
            raise HTTPException(status_code=404, detail="CSV file not found")
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def download_file(self, table_name: str = ''):
        """
        Handle file download request from the client. Return file content based on the table name.

        :param table_name: The name of the table for which the file is being requested.
        :return: JSON response with a placeholder filename and content.
        """
        # Placeholder for retrieving file content based on table_name
        try:
            return {
                "filename": "example.txt",
                "content": "Example file content based on table_name",
                "table_name": table_name
            }
        except FileNotFoundError:
            raise HTTPException(status_code=404, detail="CSV file not found")
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def get_machine_data(self, plant_code: int = 1, rm: List[str] = Query([]), machine: List[str] = Query([])):
        """
        Handle data retrieval request. Return a DataFrame or Excel data as JSON response.

        :param plant_code: The plant code for which data is being requested.
        :param rm: List of raw material codes.
        :param machine: List of machine codes.
        :return: JSON response with the data in a tabular form.
        """
        try:
            # Read data from CSV or Excel file
            file_path = r'C:\Satish\tmp_data\people-100.csv'  # Update this path to your actual file
            data_frame = self.data_handler.excel_to_dataframe(file_path)

            # Return DataFrame as JSON response
            return JSONResponse(content=data_frame.to_dict(orient="records"))
        except FileNotFoundError:
            raise HTTPException(status_code=404, detail="CSV file not found")
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def get_fg_data(self, plant_code: int = 1, FG: List[str] = Query([]), machine: List[str] = Query([])):
        """
        Handle data retrieval request for finished goods. Return a DataFrame or Excel data as JSON response.

        :param plant_code: The plant code for which data is being requested.
        :param FG: List of finished goods codes.
        :param machine: List of machine codes.
        :return: JSON response with the data in a tabular form.
        """
        try:
            # Read data from CSV or Excel file
            file_path = r'C:\Satish\tmp_data\people-100.csv'  # Update this path to your actual file
            data_frame = self.data_handler.excel_to_dataframe(file_path)

            # Return DataFrame as JSON response
            return JSONResponse(content=data_frame.to_dict(orient="records"))
        except FileNotFoundError:
            raise HTTPException(status_code=404, detail="CSV file not found")
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def get_rm_data(self, plant_code: int = 1, FG: List[str] = Query([]), rm: List[str] = Query([])):
        """
        Handle data retrieval request for finished goods. Return a DataFrame or Excel data as JSON response.

        :param plant_code: The plant code for which data is being requested.
        :param FG: List of finished goods codes.
        :param RM: List of machine codes.
        :return: JSON response with the data in a tabular form.
        """
        try:
            # Read data from CSV or Excel file
            file_path = r'C:\Satish\tmp_data\people-100.csv'  # Update this path to your actual file
            data_frame = self.data_handler.excel_to_dataframe(file_path)

            # Return DataFrame as JSON response
            return JSONResponse(content=data_frame.to_dict(orient="records"))
        except FileNotFoundError:
            raise HTTPException(status_code=404, detail="CSV file not found")
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

api_endpoints = ApiEndpoints()
router = api_endpoints.router
