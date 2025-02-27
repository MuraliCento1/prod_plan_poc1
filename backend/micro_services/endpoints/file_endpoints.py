import os
from fastapi import APIRouter, File, UploadFile
import logging
from backend.data_handler import DataHandler

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
        self.logger = logging.getLogger(__name__)
        self.data_handler = DataHandler()


    async def upload_file(self, file: UploadFile = File(...), table_name: str = ''):
        """
        Handle file upload from the client. Save the uploaded file to the server.

        :param file: The uploaded file.
        :param table_name: The name of the table for which the file is being uploaded.
        :return: JSON response with the filename, file path, and table name.
        """
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

    async def download_file(self, table_name: str = ''):
        """
        Handle file download request from the client. Return file content based on the table name.

        :param table_name: The name of the table for which the file is being requested.
        :return: JSON response with a placeholder filename and content.
        """
        # Placeholder for retrieving file content based on table_name
        return {
            "filename": "example.txt",
            "content": "Example file content based on table_name",
            "table_name": table_name
        }


api_endpoints = ApiEndpoints()
router = api_endpoints.router
