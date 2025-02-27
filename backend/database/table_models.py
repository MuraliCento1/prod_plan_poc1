from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Date, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class VendorInwardingMaster(Base):
    __tablename__ = "vendor_inwarding_master"

    plant_code = Column(String, nullable=False, primary_key=True, index=True)
    vendor_code = Column(String, nullable=False, primary_key=True, index=True)
    inwarding_date = Column(Date, nullable=False, primary_key=True, index=True)
    sku_code = Column(String, nullable=False, primary_key=True, index=True)
    qty = Column(Integer, nullable=False)

class StockMaster(Base):
    __tablename__ = "stock_master"

    plant_code = Column(String, nullable=False, primary_key=True, index=True)
    sku_code = Column(String, nullable=False, primary_key=True, index=True)
    status_date = Column(Date, nullable=False, primary_key=True)
    stock_qty = Column(Integer, nullable=False)

class VendorMaster(Base):
    __tablename__ = "vendor_master"

    vendor_code = Column(String, nullable=False, primary_key=True, index=True)
    vendor_description = Column(String, nullable=False)
    sku_code = Column(String, nullable=False, primary_key=True, index=True)
    capacity = Column(Integer, nullable=False)
    is_active = Column(Boolean, nullable=False)
    lead_time = Column(Integer, nullable=False)

class ProductionPlan(Base):
    __tablename__ = "production_plan"

    plant_code = Column(String, nullable=False, primary_key=True, index=True)
    date = Column(Date, nullable=False, primary_key=True, index=True)
    sku_code = Column(String, nullable=False, primary_key=True, index=True)
    planned_qty = Column(Integer, nullable=False)

class SkuMaster(Base):
    __tablename__ = "sku_master"

    sku_code = Column(String, nullable=False, primary_key=True, index=True)
    sku_description = Column(String, nullable=False)
    uom = Column(String, nullable=False, primary_key=True)
    sku_type = Column(String, nullable=False)

class Bom(Base):
    __tablename__ = "bom"

    plant_code = Column(String, nullable=False, primary_key=True, index=True)
    parent_code = Column(String, nullable=False, primary_key=True, index=True)
    child_code = Column(String, nullable=False, primary_key=True, index=True)
    bom_qty = Column(Integer, nullable=False )