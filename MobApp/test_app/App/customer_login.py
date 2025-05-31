from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from database import get_db_connection
from models import CustomerLoginRequest
from otp import send_otp  # assuming this is in otp_utils.py
router = APIRouter()


@router.post("/customer/login")
def customer_login(data: CustomerLoginRequest):
    print("[DEBUG] Login request received with data:", data.dict())

    conn = get_db_connection()
    if not conn:
        print("[ERROR] Database connection failed.")
        raise HTTPException(status_code=500, detail="Database connection failed")

    try:
        cursor = conn.cursor()
        print("[DEBUG] Database cursor created.")

        query = """
            SELECT customer_id, phone_number FROM Customers
            WHERE LOWER(full_name) = LOWER(?) AND email = ?
        """
        cursor.execute(query, (data.name.lower(), data.email))
        print("[DEBUG] SQL executed successfully.")

        row = cursor.fetchone()
        print("[DEBUG] Query result fetched:", row)

        if not row:
            raise HTTPException(status_code=404, detail="Customer not found")

        customer_id, phone_number = str(row[0]), row[1]
        print("[DEBUG] Customer ID:", customer_id)
        print("[DEBUG] Phone Number:", phone_number)

        otp = send_otp(user_id=customer_id, phone_number=phone_number, user_type="customer")
        if not otp:
            raise HTTPException(status_code=500, detail="Failed to send OTP")

        return {
            "message": "OTP sent to registered phone number.",
            "customer_id": customer_id,
            "phone_number": phone_number,
            "otp": otp  # in production, do NOT return the OTP!
        }

    except Exception as e:
        print("[ERROR] Exception occurred:", str(e))
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

    finally:
        try:
            cursor.close()
        except Exception as ce:
            print("[ERROR] Failed to close cursor:", ce)
        try:
            conn.close()
        except Exception as coe:
            print("[ERROR] Failed to close connection:", coe)
