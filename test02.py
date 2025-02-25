from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
from test01 import Base, VendorInwardingMaster, StockMaster, VendorMaster, ProductionPlanTemplate, SkuMaster, BomTemplate
import logging

logging.basicConfig(filename='app.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
DATABASE_URL = "postgresql://postgres:799799@localhost:5432/postgres"
#
# engine = create_engine(DATABASE_URL)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#
# def create_tables():
#     inspector = inspect(engine)
#     tables = inspector.get_table_names()
#     tables_list = ['vendor_inwarding_master', 'stock_master', 'vendor_master', 'production_plan_template', 'production_plan_template', 'sku_master']
#     # Check and create VendorInwardingMaster table
#     for table_name in tables_list:
#         if table_name not in tables:
#             VendorInwardingMaster.__table__.create(bind=engine)
#             print("Table %s created.", table_name)
#         else:
#             print("Table %s already exists.", table_name)
#
#
#
# if __name__ == "__main__":
#     create_tables()
#
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
