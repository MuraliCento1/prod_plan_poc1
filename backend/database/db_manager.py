from sqlalchemy import MetaData, Table, inspect, text
import logging
from backend.database.database import Database
from typing import List, Dict, Any
import pandas as pd
from backend.database.table_models import (
    VendorInwardingMaster, StockMaster, VendorMaster, ProductionPlan, SkuMaster, Bom
)


logging.basicConfig(level=logging.INFO)


DATABASE_URL = "postgresql://postgres:799799@localhost:5432/postgres"
db = Database(DATABASE_URL)


class DatabaseManager:
    def __init__(self):
        self.db = db
        self.session = None
        self.logger = logging.getLogger(__name__)
        self.models_mapping = {
            'vendor_inwarding_master': VendorInwardingMaster,
            'stock_master': StockMaster,
            'vendor_master': VendorMaster,
            'production_plan': ProductionPlan,
            'sku_master': SkuMaster,
            'bom': Bom
        }

    def connect(self):
        self.db.connect()
        self.session = self.db.get_session()

    def disconnect(self):
        if self.session:
            self.session.close()
        self.db.disconnect()

    def get_model_table_data_with_columns(self, model, columns: list):
        """
        Get data from the specified table with only the specified columns.

        :param db: Database instance for connection.
        :param model: SQLAlchemy model representing the table.
        :param columns: List of column names to retrieve.
        :return: List of dictionaries with the retrieved columns.
        """
        self.connect()
        try:
            # Construct the columns to retrieve using the model attributes
            selected_columns = [getattr(model, col) for col in columns]
            query =  self.session.query(*selected_columns)
            results = query.all()

            # Convert results to a list of dictionaries
            results_dict = [dict(zip(columns, result)) for result in results]
            return results_dict
        except Exception as e:
            self.logger.error(f"Error retrieving table data with columns: {e}")
            raise
        finally:
            self.disconnect()

    def get_table_data_with_columns(self, table_name: str, columns: list):
        """
        Get data from the specified table with only the specified columns.

        :param db: Database instance for connection.
        :param table_name: Name of the table.
        :param columns: List of column names to retrieve.
        :return: List of dictionaries with the retrieved columns.
        """
        self.connect()
        metadata = MetaData()
        table = Table(table_name, metadata, autoload_with=db.engine)

        try:
            # Construct the columns to retrieve using the table columns
            selected_columns = [getattr(table.c, col) for col in columns]
            self.logger.info("columns: %s", selected_columns)
            query =  self.session.query(*selected_columns)
            results = query.all()

            # Convert results to a list of dictionaries
            results_dict = [dict(zip(columns, result)) for result in results]
            return results_dict
        except Exception as e:
            self.logger.error(f"Error retrieving table data with columns: {e}")
            raise
        finally:
            self.disconnect()

    def check_table_exists(self, table_name: str) -> bool:
        """
        Check if a table exists in the database.

        :param table_name: Name of the table to check.
        :return: True if the table exists, False otherwise.
        """
        self.connect()
        inspector = inspect(self.db.engine)
        tables = inspector.get_table_names()
        self.disconnect()
        return table_name in tables

    def get_all_tables(self) -> List[str]:
        """
        Get a list of all tables in the database.

        :return: List of table names.
        """
        self.connect()
        inspector = inspect(self.db.engine)
        tables = inspector.get_table_names()
        self.disconnect()
        return tables

    def read_table_data(self, table_name: str) -> List[Dict[str, Any]]:
        """
        Read data from the specified table.
        """
        self.connect()
        metadata = MetaData()
        table = Table(table_name, metadata, autoload_with=self.db.engine)

        try:
            query = self.session.query(table)
            results = query.all()

            # Correctly convert result rows to dictionaries
            result_dicts = []
            for row in results:
                row_dict = {column.name: getattr(row, column.name) for column in table.columns}
                result_dicts.append(row_dict)

            return result_dicts
        except Exception as e:
            self.logger.error(f"Error reading table data: {e}")
            raise
        finally:
            self.disconnect()

    def insert_data_into_table(self, table_name: str, data: Dict[str, Any]) -> None:
        """
        Insert data into the specified table.
        """
        self.connect()
        metadata = MetaData()
        table = Table(table_name, metadata, autoload_with=self.db.engine)

        try:
            insert_stmt = table.insert().values(**data)
            self.session.execute(insert_stmt)
            self.session.commit()
        except Exception as e:
            self.logger.error(f"Error inserting data into table: {e}")
            self.session.rollback()
            raise
        finally:
            self.disconnect()

    def update_table_data(self, table_name: str, data: Dict[str, Any], condition: Dict[str, Any]) -> None:
        """
        Update data in the specified table.
        """
        self.connect()
        metadata = MetaData()
        table = Table(table_name, metadata, autoload_with=self.db.engine)

        try:
            update_stmt = table.update().where(
                getattr(table.c, list(condition.keys())[0]) == list(condition.values())[0]
            ).values(**data)
            self.session.execute(update_stmt)
            self.session.commit()
        except Exception as e:
            self.logger.error(f"Error updating table data: {e}")
            self.session.rollback()
            raise
        finally:
            self.disconnect()

    def delete_table_data(self, table_name: str, condition: Dict[str, Any]) -> None:
        """
        Delete data from the specified table based on a condition.
        """
        self.connect()
        metadata = MetaData()
        table = Table(table_name, metadata, autoload_with=self.db.engine)

        try:
            delete_stmt = table.delete().where(
                getattr(table.c, list(condition.keys())[0]) == list(condition.values())[0]
            )
            self.session.execute(delete_stmt)
            self.session.commit()
        except Exception as e:
            self.logger.error(f"Error deleting table data: {e}")
            self.session.rollback()
            raise
        finally:
            self.disconnect()

    def get_table_columns(self, table_name: str, columns: List[str]) -> List[Dict[str, Any]]:
        """
        Retrieve data for specific columns from the specified table.
        """
        self.connect()
        metadata = MetaData()
        table = Table(table_name, metadata, autoload_with=self.db.engine)

        try:
            selected_columns = [getattr(table.c, col) for col in columns]
            query = self.session.query(*selected_columns)
            results = query.all()
            return [dict(zip(columns, result)) for result in results]
        except Exception as e:
            self.logger.error(f"Error retrieving table columns: {e}")
            raise
        finally:
            self.disconnect()

    def insert_dataframe_into_table(self, table_name: str, dataframe: pd.DataFrame,
                                    if_exists: str = 'append') -> None:
        """
        Insert a DataFrame into the specified table.

        :param table_name: Name of the table.
        :param dataframe: DataFrame to be inserted.
        :param if_exists: Behavior when the table already exists ('fail', 'replace', 'append').
        """
        self.connect()
        try:
            dataframe.to_sql(table_name, con=self.db.engine, if_exists=if_exists, index=False)
        except Exception as e:
            self.logger.error(f"Error inserting DataFrame into table: {e}")
            raise
        finally:
            self.disconnect()

    def create_tables_structures(self) -> None:
        """
        Create tables if they don't exist.

        :param models_mapping: Mapping of table names to SQLAlchemy models.
        """
        self.connect()
        inspector = inspect(self.db.engine)
        tables = inspector.get_table_names()

        try:
            for table_name, model in self.models_mapping.items():
                if table_name not in tables:
                    model.__table__.create(bind=self.db.engine)
                    print(f"Table '{table_name}' created.")
                else:
                    print(f"Table '{table_name}' already exists.")
        except Exception as e:
            self.logger.error(f"Error creating tables: {e}")
            raise
        finally:
            self.disconnect()

    def delete_column(self, table_name: str, column_name: str) -> None:
        """
        Delete a column from a table in the database.
        """
        self.connect()
        try:
            self.session.execute(text(f"ALTER TABLE {table_name} DROP COLUMN IF EXISTS {column_name}"))
            self.session.commit()
            print(f"Column '{column_name}' deleted from table '{table_name}'.")
        except Exception as e:
            self.logger.error(f"Error deleting column: {e}")
            self.session.rollback()
            raise
        finally:
            self.disconnect()

    def delete_table(self, table_name: str) -> None:
        """
        Delete a table from the database.
        """
        self.connect()
        try:
            self.session.execute(text(f"DROP TABLE IF EXISTS {table_name}"))
            self.session.commit()
            print(f"Table '{table_name}' deleted.")
        except Exception as e:
            self.logger.error(f"Error deleting table: {e}")
            self.session.rollback()
            raise
        finally:
            self.disconnect()

    def get_database_name(self) -> str:
        """
        Get the name of the connected database.
        """
        self.connect()
        try:
            database_name = self.session.execute(text("SELECT current_database()")).scalar()
            return database_name
        except Exception as e:
            self.logger.error(f"Error getting database name: {e}")
            raise
        finally:
            self.disconnect()

    def get_db_server_name(self) -> str:
        """
        Get the name of the database server.
        """
        self.connect()
        try:
            # For PostgreSQL, you can get the server version or server properties
            server_name = self.session.execute(text("SELECT inet_server_addr()")).scalar()
            return server_name
        except Exception as e:
            self.logger.error(f"Error getting database server name: {e}")
            raise
        finally:
            self.disconnect()


