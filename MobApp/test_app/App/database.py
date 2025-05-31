import pyodbc
import os
from dotenv import load_dotenv
import hashlib

load_dotenv()


# print("DB_SERVER:", os.getenv('DB_SERVER'))
# print("DB_DATABASE:", os.getenv('DB_DATABASE'))
# print("DB_UID:", os.getenv('DB_UID'))
# print("DB_PWD:", os.getenv('DB_PWD'))

def get_db_connection():
    try:
        conn = pyodbc.connect(
            # "DRIVER={ODBC Driver 17 for SQL Server};"
            # f"SERVER={os.getenv('DB_SERVER')};"
            # f"DATABASE={os.getenv('DB_DATABASE')};"
            # f"UID={os.getenv('DB_UID')};"
            # f"PWD={os.getenv('DB_PWD')};"

            f"DRIVER={os.getenv('DB_DRIVER')};"
            f"SERVER={os.getenv('DB_SERVER')};"
            f"DATABASE={os.getenv('DB_DATABASE')};"
            f"Trusted_Connection={os.getenv('DB_TRUSTED_CONNECTION')}"

        )
        print("✅ Database connected successfully")
        return conn
    except Exception as e:
        print("❌ Database connection failed:", e)
        return None

def get_employee_by_id_password(employee_id: str, password: str):
    conn = get_db_connection()
    if not conn:
        print("No connection available")
        return None

    try:
        cursor = conn.cursor()
        print(f"Trying to authenticate employee_id={employee_id}")

        # passwor = "password123"
        # password_has = hashlib.sha256(passwor.encode()).hexdigest()
        # print(password_has)

        password_hash = hashlib.sha256(password.encode()).hexdigest()

        print(password_hash)
        cursor.execute(
            "SELECT employee_id, phone_number FROM Employees WHERE employee_id = ? AND password_hash = ?",
            (employee_id, password_hash)
        )
        row = cursor.fetchone()
        if row:
            print("[INFO] Employee authenticated successfully")
            return {"employee_id": row[0], "phone_number": row[1]}
        else:
            print("[WARN] Invalid credentials")
            return None
    except Exception as e:
        print("Database query error:", e)
        return None
    finally:
        cursor.close()
        conn.close()