from fastapi import FastAPI, File, UploadFile, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import SessionLocal, engine, ExcelData, Base
import pandas as pd
import os
import logging
from read_data import process_excel

# Configure logging to write to a file
logging.basicConfig(filename='app.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

app = FastAPI()

# Configure Logging
logging.basicConfig(filename='app.log', level=logging.INFO)

# Directory to save uploaded files
UPLOAD_DIR = "uploads"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

@app.on_event("startup")
async def startup_event():
    logging.debug("API has started running.")

@app.on_event("shutdown")
async def shutdown_event():
    logging.debug("API is shutting down.")

@app.post("/uploadfile/")
async def upload_file(file: UploadFile = File(...)):
    logging.debug("API endpoint /uploadfile/ triggered.")
    try:
        # Ensure the uploads directory exists
        if not os.path.exists(UPLOAD_DIR):
            os.makedirs(UPLOAD_DIR)

        # Construct the file path
        file_location = os.path.join(UPLOAD_DIR, file.filename)

        # Save the file
        with open(file_location, "wb") as f:
            contents = await file.read()
            f.write(contents)
        logging.info("the uploaded file_location is %s", file_location)

        process_excel(file_location)

        return {"message": f"File '{file.filename}' uploaded and data saved to the database successfully.",
                "file_path": file_location}
    except Exception as err:
        logging.warning("failed due :%s",err)

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






