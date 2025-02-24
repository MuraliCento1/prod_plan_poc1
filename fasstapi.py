from fastapi import FastAPI, File, UploadFile, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import SessionLocal, engine, ExcelData, Base
import pandas as pd
import os
import logging


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    logging.info("calling get")
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


upload_folder = "uploads"
os.makedirs(upload_folder, exist_ok=True)

# Configure logging to write to a file
logging.basicConfig(filename='app.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


@app.post("/upload")
async def upload_file(file: UploadFile = File(...), db: Session = Depends(get_db)):
    logging.info("upload_file function called")
    file_location = f"{upload_folder}/{file.filename}"

    with open(file_location, "wb") as f:
        f.write(await file.read())

    logging.info(f"File downloaded to: {file_location}")

    # Read the Excel file using pandas
    df = pd.read_excel(file_location)

    # Print the Excel content to the log
    logging.info(f"Excel content:\n{df}")

    # Insert data into PostgreSQL using SQLAlchemy
    for index, row in df.iterrows():
        db_record = ExcelData(column1=row['Column1'], column2=row['Column2'])
        # Add more columns as per your Excel data structure
        db.add(db_record)

    db.commit()

    logging.info(f"Data from '{file.filename}' uploaded to the database")

    return {"message": f"File '{file.filename}' uploaded and data saved to the database successfully.",
            "file_path": file_location}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)





#
#
# from fastapi import FastAPI, UploadFile, File, HTTPException
# from fastapi.responses import StreamingResponse
# from pandas import read_excel, ExcelWriter
# import logging
# from io import BytesIO
# from datetime import datetime
# import uvicorn
#
# app = FastAPI()
#
# # Configure Logging
# logging.basicConfig(filename='app.log', level=logging.DEBUG)
#
# @app.on_event("startup")
# async def startup_event():
#     logging.debug("API has started running.")
#
# @app.on_event("shutdown")
# async def shutdown_event():
#     logging.debug("API is shutting down.")
#
# @app.on_event("/uploadfile/")
# async def upload_file(file: UploadFile = File(...)):
#     logging.debug("API endpoint /uploadfile/ triggered.")
#     try:
#         contents = await file.read()
#         df = read_excel(BytesIO(contents))
#
#         # Add 'updated_at' column to DataFrame if not already present
#         if 'updated_at' not in df.columns:
#             df['updated_at'] = datetime.utcnow()
#
#         # Log the data
#         logging.info("DataFrame before update:")
#         logging.info(df.to_string())
#         print("DataFrame before update:")
#         print(df)
#
#         # Create a BytesIO stream for the processed file
#         output = BytesIO()
#         with ExcelWriter(output, engine='xlsxwriter') as writer:
#             df.to_excel(writer, index=False)
#         output.seek(0)
#
#         logging.debug("File processing completed. Ready to download.")
#         return StreamingResponse(output, media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', headers={"Content-Disposition": "attachment; filename=processed_file.xlsx"})
#
#     except Exception as e:
#         logging.error(f"An error occurred: {str(e)}")
#         print(f"An error occurred: {str(e)}")
#         raise HTTPException(status_code=500, detail="An error occurred while processing the Excel file")
#
#
# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)






