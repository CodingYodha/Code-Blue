from fastapi import FastAPI, HTTPException, Request, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import pymysql
import tensorflow as tf
import numpy as np
import os
from PIL import Image
import shutil
from ultralytics import YOLO  # Import YOLO for pollution detection

app = FastAPI()
# Allow your frontend URL here instead of "*"
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # e.g., ["http://localhost:8000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MySQL connection config
def get_db_connection():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="",
        database="projectblue",
        cursorclass=pymysql.cursors.DictCursor
    )

# Pydantic model for request data
class FormData1(BaseModel):
    email: str
    password: str

class FormData2(BaseModel):
    zap_id: str
    event_type: str
    event_photo: str
    person_contact: str
    person_name: str
    event_location: str
    person_message: str

class FormData3(BaseModel):
    event_type: str
    event_photo: str
    event_location: str

class SupportData(BaseModel):
    sup_subject: str
    sup_message: str

class UpdateGovVerified(BaseModel):
    uq_id: int
    isGovVerified: int


@app.post("/login")
async def login_form(data: FormData1):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            query = "SELECT * FROM gov_auth WHERE username = %s AND password = %s"
            cursor.execute(query, (data.email, data.password))
            user = cursor.fetchone()

            if user:
                return {"message": "Login successful", "user": user["username"], "password": user["password"]}
            else:
                raise HTTPException(status_code=401, detail="Invalid credentials")
    finally:
        connection.close()


def get_oil_image(new_file_name: str) -> bool:
    # Path to the image
    image_path = os.path.join("uploads",new_file_name)
    
    if os.path.exists(image_path):
        # Preprocess the image
        img = Image.open(image_path)
        img = img.resize((150, 150))  # Resize to 150x150
        img_array = np.array(img) / 255.0  # Normalize pixel values
        img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
        
        # Load the TensorFlow model
        model_path = os.path.join("models", "oil_spill_detector_model.h5")  # Path to the model
        model = tf.keras.models.load_model(model_path)
        
        # Make a prediction
        prediction = model.predict(img_array)
        predicted_class = (prediction > 0.5).astype("int32")[0][0]  # Binary classification
        
        # Return the prediction as a JSON response
        return bool(predicted_class)


def get_pollution_image(new_file_name: str) -> bool:
    # Path to the image
    image_path = os.path.join("uploads", new_file_name)

    # Load the YOLOv8 model
    model_path = os.path.join("models", "pollution.pt")  # Path to the YOLOv8 model
    model = YOLO(model_path)

    # Make a prediction
    results = model.predict(source=image_path, save=False, conf=0.5)  # Run inference on the image

    # Check if any objects were detected
    detected = len(results[0].boxes) > 0  # If boxes are detected, pollution is present

    # Return the detection result
    return bool(detected)



@app.post("/issue_report")
async def issue_report_form(
    zap_id: str = Form(...),
    event_type: str = Form(...),
    person_contact: str = Form(...),
    person_name: str = Form(...),
    event_location: str = Form(...),
    person_message: str = Form(...),
    event_photo: UploadFile = File(...)
):
    try:
        # Read the current number from num_count.txt
        num_file_path = "num_count.txt"
        if not os.path.exists(num_file_path):
            with open(num_file_path, "w") as num_file:
                num_file.write("1")  # Initialize with 1 if the file doesn't exist

        with open(num_file_path, "r") as num_file:
            current_num = int(num_file.read().strip())

        # Generate the new file name
        file_extension = os.path.splitext(event_photo.filename)[1]  # Get the file extension
        new_file_name = f"{current_num}{file_extension}"

        # Save the uploaded file with the new name
        upload_dir = "uploads"
        os.makedirs(upload_dir, exist_ok=True)
        file_path = os.path.join(upload_dir, new_file_name)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(event_photo.file, buffer)

        if(event_type == "oilspill"):
            if(get_oil_image(new_file_name)):
                # Increment the number and save it back to num_count.txt
                with open(num_file_path, "w") as num_file:
                    num_file.write(str(current_num + 1))

                # Save the data to the database
                connection = get_db_connection()
                try:
                    with connection.cursor() as cursor:
                        sql = """
                        INSERT INTO ai_report (zap_id, event_type, event_photo, person_contact, person_name, event_location, person_message)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                        """
                        cursor.execute(sql, (zap_id, "Oil Spill", new_file_name, person_contact, person_name, event_location, person_message))
                    connection.commit()
                finally:
                    connection.close()
                return {"message": f"Report submitted successfully by {person_name}"}
            else:
                os.remove(file_path)
                return {"message": f"Please upload image which actually has oil spill."}
        
        elif(event_type == "pollution"):
            if(get_pollution_image(new_file_name)):
                # Increment the number and save it back to num_count.txt
                with open(num_file_path, "w") as num_file:
                    num_file.write(str(current_num + 1))

                # Save the data to the database
                connection = get_db_connection()
                try:
                    with connection.cursor() as cursor:
                        sql = """
                        INSERT INTO ai_report (zap_id, event_type, event_photo, person_contact, person_name, event_location, person_message)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                        """
                        cursor.execute(sql, (zap_id, "Pollution", new_file_name, person_contact, person_name, event_location, person_message))
                    connection.commit()
                finally:
                    connection.close()
                return {"message": f"Report submitted successfully by {person_name}"}
            else:
                os.remove(file_path)
                return {"message": f"Please upload image which actually has pollution."}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@app.post("/support_form")
async def support_form(data: SupportData):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO support (subject, message) VALUES (%s, %s)"
            cursor.execute(sql, (data.sup_subject, data.sup_message))
        connection.commit()
    finally:
        connection.close()
    
    return {"message": f"Your message has been sent successfully!"}


@app.get("/get_ai_report")
async def get_ai_report():
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            query = "SELECT * FROM ai_report"
            cursor.execute(query,)
            ai_report = cursor.fetchall()
        return ai_report
    finally:
        connection.close()


@app.get("/public_ai_report")
async def public_ai_report():
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            # Fetch only event_type, event_photo, and event_location where isGovVerified is 1
            query = "SELECT event_type, event_photo, event_location FROM ai_report WHERE isGovVerified = %s"
            cursor.execute(query, ("1",))
            public_ai_report_data = cursor.fetchall()
        return public_ai_report_data
    finally:
        connection.close()


@app.post("/update_gov_verified")
async def update_gov_verified(data: UpdateGovVerified):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            # Update the isGovVerified column for the given U id
            sql = "UPDATE ai_report SET isGovVerified = %s WHERE uq_id = %s"
            cursor.execute(sql, (data.isGovVerified, data.uq_id))
        connection.commit()
        return {"message": f"Gov Verified status updated for U ID {data.uq_id}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        connection.close()


@app.post("/signup")
async def signup_form(data: FormData1):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            # 🔍 Check if email already exists
            check_sql = "SELECT * FROM gov_auth WHERE username = %s"
            cursor.execute(check_sql, (data.email,))
            result = cursor.fetchone()

            if result:
                return {"message": "Email already exists. Please log in or use another email."}

            # ✅ Insert new record
            insert_sql = "INSERT INTO gov_auth (username, password) VALUES (%s, %s)"
            cursor.execute(insert_sql, (data.email, data.password))
            connection.commit()

        return {"message": f"Data saved for {data.email, data.password}"}
    finally:
        connection.close()

@app.get("/")
async def root():
    return {"message": "Hello Bro!"}