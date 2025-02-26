import logging
import pandas as pd
from backend.database.db_manager import DatabaseManager

logging.basicConfig(level=logging.INFO)


class DataHandler:
    def __init__(self):
        """
        Initialize the DataHandler class.
        """
        self.logger = logging.getLogger(__name__)
        self.data_manager = DatabaseManager()

    def excel_to_dataframe(self, file_path: str):
        """
        Convert Excel content to a Pandas DataFrame.

        :param file_path: Path to the Excel file.
        :return: DataFrame containing the Excel data.
        """
        try:
            data_frame = pd.read_excel(file_path)
            self.logger.info("Excel content successfully converted to DataFrame.")
            return data_frame
        except Exception as e:
            self.logger.error(f"Error converting Excel content to DataFrame: {e}")

    def update_data(self, file_path: str, table_name: str):
        """
        Convert Excel content to a Pandas DataFrame.

        :param file_path: Path to the Excel file.
        :return: DataFrame containing the Excel data.
        """
        try:
            data_frame = self.excel_to_dataframe(file_path)
            self.data_manager.insert_dataframe_into_table(table_name, data_frame)
        except Exception as e:
            self.logger.error(f"Error converting Excel content to DataFrame: {e}")
