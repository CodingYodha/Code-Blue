from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pymysql

app = FastAPI()

# Allow your frontend URL here instead of "*"
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # e.g., ["http://localhost:5500"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MySQL connection config
def get_db_connection():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="",  # 🔐 Use env vars in real projects
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
    zap_id: str
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


@app.post("/issue_report")
async def issue_report_form(data: FormData2):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO issue_report (zap_id, event_type, event_photo, person_contact, person_name, event_location, person_message) VALUES (%s, %s, %s, %s, %s, %s, %s)"  # Fixed %d to %s for person_contact
            cursor.execute(sql, (data.zap_id, data.event_type, data.event_photo, data.person_contact, data.person_name, data.event_location, data.person_message))
        connection.commit()
    finally:
        connection.close()
    
    return {"message": f"Data saved for {data.person_name}"}



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
            # Update the isGovVerified column for the given zap_id
            sql = "UPDATE ai_report SET isGovVerified = %s WHERE zap_id = %s"
            cursor.execute(sql, (data.isGovVerified, data.zap_id))
        connection.commit()
        return {"message": f"Gov Verified status updated for Zap ID {data.zap_id}"}
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
