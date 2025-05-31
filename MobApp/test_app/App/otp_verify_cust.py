# from fastapi import APIRouter, HTTPException
# from pydantic import BaseModel
# from database import get_db_connection

# router = APIRouter()

# class OTPVerifyRequest(BaseModel):
#     customer_id: str
#     otp_code: str

# @router.post("/customer/verify-otp")
# def verify_customer_otp(data: OTPVerifyRequest):
#     conn = get_db_connection()
#     if not conn:
#         raise HTTPException(status_code=500, detail="Database connection failed")

#     try:
#         cursor = conn.cursor()

#         # Clean expired OTPs
#         cursor.execute("DELETE FROM OTPs WHERE expires_at < GETDATE()")

#         # Get the most recent valid OTP for this customer
#         cursor.execute("""
#             SELECT TOP 1 id, otp_code FROM OTPs
#             WHERE user_id = ? AND user_type = 'customer' AND expires_at > GETDATE()
#             ORDER BY created_at DESC
#         """, (data.customer_id,))
#         row = cursor.fetchone()

#         if row and row[1] == data.otp_code:
#             # OTP is valid – delete it
#             cursor.execute("DELETE FROM OTPs WHERE id = ?", (row[0],))
#             conn.commit()
#             return {
#                 "message": "OTP verified successfully",
#                 "status": "verified"
#             }

#         raise HTTPException(status_code=401, detail="Invalid or expired OTP")

#     finally:
#         cursor.close()
#         conn.close()
