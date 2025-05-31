# from fastapi import APIRouter, HTTPException
# from pydantic import BaseModel
# from database import get_db_connection  # your DB connection func

# router = APIRouter()

# class OTPVerifyRequest(BaseModel):
#     employee_id: str
#     otp: str

# @router.post("/verify-otp")
# async def verify_otp(data: OTPVerifyRequest):
#     conn = get_db_connection()
#     if not conn:
#         raise HTTPException(status_code=500, detail="Database connection failed")

#     try:
#         cursor = conn.cursor()
#         cursor.execute(
#             "SELECT otp FROM OTPVerifications WHERE employee_id = ? ORDER BY created_at DESC LIMIT 1",
#             (data.employee_id,)
#         )
#         row = cursor.fetchone()
#         if row is None:
#             raise HTTPException(status_code=404, detail="No OTP found for this employee")

#         stored_otp = row[0]
#         if stored_otp == data.otp:
#             return {"message": "OTP verified successfully"}
#         else:
#             raise HTTPException(status_code=401, detail="Invalid OTP")
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
#     finally:
#         conn.close()
