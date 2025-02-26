from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
from test01 import Base, VendorInwardingMaster, StockMaster, VendorMaster, ProductionPlanTemplate, SkuMaster, BomTemplate
import logging

logging.basicConfig(filename='app.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
DATABASE_URL = "postgresql://postgres:799799@localhost:5432/postgres"

engine = create_engine(DATABASE_URL)

def create_tables():
    inspector = inspect(engine)
    tables = inspector.get_table_names()

    # Mapping of table names to SQLAlchemy models
    models_mapping = {
        'vendor_inwarding_master': VendorInwardingMaster,
        'stock_master': StockMaster,
        'vendor_master': VendorMaster,
        'production_plan_template': ProductionPlanTemplate,
        'sku_master': SkuMaster,
        'bom_template': BomTemplate
    }

    # Iterate over the mapping and create tables if they don't exist
    for table_name, model in models_mapping.items():
        if table_name not in tables:
            model.__table__.create(bind=engine)
            print(f"Table '{table_name}' created.")
        else:
            print(f"Table '{table_name}' already exists.")

if __name__ == "__main__":
    create_tables()
