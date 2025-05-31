from pydantic import BaseModel

class LoginRequest(BaseModel):
    employee_id: str
    password: str

class OTPRequest(BaseModel):
    user_id: str
    otp: str
    user_type: str 

class CustomerLoginRequest(BaseModel):
    name: str
    email: str
