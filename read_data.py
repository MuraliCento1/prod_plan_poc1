# from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, Column, String, DateTime, MetaData, Table
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func
from pandas import read_excel
import logging
from datetime import datetime

# app = FastAPI()

# Configure Logging
logging.basicConfig(filename='app.log', level=logging.INFO)

# Setup Database Connection
DATABASE_URL = "postgresql://postgres:799799@localhost:5432/postgres"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
metadata = MetaData()


# Create a dynamic table with 'updated_at' column
def get_table(table_name, column_names):
    columns = [Column(column_name, String) for column_name in column_names]
    if 'updated_at' not in column_names:
        columns.append(Column('updated_at', DateTime, server_default=func.now(), onupdate=func.now()))
    return Table(
        table_name, metadata,
        *columns
    )



def process_excel():
    try:
        # Specify the location of the Excel file
        excel_file_path = "uploads/BOM1.xlsx"

        # Read the Excel file
        df = read_excel(excel_file_path)

        # Add 'updated_at' column to DataFrame if not already present
        if 'updated_at' not in df.columns:
            df['updated_at'] = datetime.utcnow()

        # Log the data
        logging.info(df.to_string())
        print("DataFrame before update:")
        print(df)

        table_name = "your_table_name"
        table = get_table(table_name, df.columns)

        # Print DB connection established
        logging.info("Database connection established")
        print("Database connection established")

        with engine.begin() as connection:
            table.create(bind=engine, checkfirst=True)
            df.to_sql(table_name, con=connection, if_exists='replace', index=False)

        # Query the updated data
        with engine.connect() as connection:
            result = connection.execute(table.select().order_by(table.c.updated_at.desc()))
            columns = result.keys()
            updated_data = [dict(zip(columns, row)) for row in result.fetchall()]
            logging.info(f"Latest updated data: {updated_data}")
            print(f"Latest updated data: {updated_data}")

        return {"status": "success", "message": "Excel data processed and updated in the database",
                "data": updated_data}

    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        print(f"An error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail="An error occurred while processing the Excel file")

