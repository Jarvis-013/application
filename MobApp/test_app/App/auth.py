from fastapi import APIRouter, HTTPException
from models import LoginRequest, OTPRequest
from database import get_db_connection
from otp import send_otp, verify_otp_code
from database import get_employee_by_id_password


router = APIRouter()

# @router.post("/login")
# async def login(data: LoginRequest):
#     # print(data.employee_id, data.password)
#     employee = get_employee_by_id_password(data.employee_id, data.password)
#     if not employee:
#         raise HTTPException(status_code=401, detail="Invalid employee ID or password")

#     phone_number = employee["phone_number"]  # <-- here fix

#     # Send OTP
#     otp_sent = send_otp(data.employee_id, phone_number)
#     if not otp_sent:
#         raise HTTPException(status_code=500, detail="Failed to send OTP")

#     return {
#         "message": "OTP sent to your phone",
#         "phone_number": phone_number
#     }

@router.post("/login")
async def login(data: LoginRequest):
    employee = get_employee_by_id_password(data.employee_id, data.password)
    if not employee:
        raise HTTPException(status_code=401, detail="Invalid employee ID or password")

    phone_number = employee["phone_number"]
    # otp = send_otp(data.employee_id, phone_number,"employee")

    # if otp is None:
    #     raise HTTPException(status_code=500, detail="Failed to generate OTP")

    return {
        # "message": "OTP sent to your phone",
        "phone_number": phone_number,
        # "otp": otp,  # ✅ Return OTP in response (only for development)
        "emp_id": data.employee_id,
        "user_type":"employee"
    }

@router.post("/verify-otp")
def verify_otp(data: OTPRequest):
    print(f"[DEBUG] Verifying OTP for user_type={data.user_type}, user_id={data.user_id}")

    if verify_otp_code(data.user_id, data.otp, data.user_type):
        return {"message": f"{data.user_type.capitalize()} login successful {data.user_id}" }

    raise HTTPException(status_code=401, detail="Invalid or expired OTP")
