import pandas as pd
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
from models import VendorInwardingMaster, StockMaster, VendorMaster, ProductionPlanTemplate, SkuMaster, BomTemplate

DATABASE_URL = "postgresql://postgres:799799@localhost:5432/postgres"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class DataUpdater:
    def __init__(self, db_url):
        self.engine = create_engine(db_url)
        self.session = SessionLocal()

    def read_excel(self, file_path):
        """Read Excel file and return DataFrame"""
        df = pd.read_excel(file_path)
        print(f"Read {len(df)} rows from {file_path}")
        return df

    def get_table_string(self, file_name):
        # Split the string by the period '.'
        base_string = file_name.split('.')[0]

        # Split the base string by '_'
        segments = base_string.split('_')

        # Capitalize the first letter of each segment
        modified_segments = [segment.capitalize() for segment in segments]

        # Join the segments back together
        table_name = ''.join(modified_segments)

        return table_name

    def update_table(self, df, model):
        """Update any table based on the provided DataFrame and model"""
        for index, row in df.iterrows():
            record = model(**row.to_dict())
            self.session.merge(record)
        self.session.commit()
        print(f"{model.__tablename__} table updated.")

    def close(self):
        self.session.close()

# Example Usage
if __name__ == "__main__":
    updater = DataUpdater(DATABASE_URL)

    # Define file paths and models
    file_model_mapping = {
        "path_to_vendor_inwarding_master.xlsx": VendorInwardingMaster,
        "path_to_stock_master.xlsx": StockMaster,
        "path_to_vendor_master.xlsx": VendorMaster,
        "path_to_production_plan_template.xlsx": ProductionPlanTemplate,
        "path_to_sku_master.xlsx": SkuMaster,
        "path_to_bom_template.xlsx": BomTemplate
    }

    # Update each table based on the mapping
    for file_path, model in file_model_mapping.items():
        df = updater.read_excel(file_path)
        updater.update_table(df, model)

    # Close the session
    updater.close()


