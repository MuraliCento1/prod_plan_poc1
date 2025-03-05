import logging
import pandas as pd
from backend.database.db_manager import DatabaseManager
from backend.config import Config
logging.basicConfig(level=logging.INFO)


class DataHandler:
    def __init__(self):
        """
        Initialize the DataHandler class.
        """
        self.logger = logging.getLogger(__name__)
        self.data_manager = DatabaseManager()
        self.file_paths = Config.file_paths

    def excel_to_dataframe(self, file_path: str):
        """
        Convert Excel content to a Pandas DataFrame.

        :param file_path: Path to the Excel file.
        :return: DataFrame containing the Excel data.
        """
        try:
            self.file_paths['upload_dir'] = file_path
            if file_path.endswith('.csv'):
                data_frame = pd.read_csv(file_path)
            else:
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
            update_status = self.data_manager.insert_dataframe_into_table(table_name, data_frame)
            # if "does not exist" in update_status:
            #     self.data_manager.create_tables_structures()
            #     self.data_manager.insert_dataframe_into_table(table_name, data_frame)
        except Exception as e:
            self.logger.error(f"Error converting Excel content to DataFrame: {e}")
