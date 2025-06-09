from fastapi import FastAPI
from auth import router as auth_router
from customer_login import router as customer_login_router
from policies import router as pol_route
from quotation import router as quotation_router
app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello Guys!"}

app.include_router(auth_router)
app.include_router(customer_login_router)
app.include_router(pol_route)
app.include_router(quotation_router)

# python -m uvicorn main:app --reload --port 9000

