from fastapi import FastAPI
from auth import router as auth_router
from customer_login import router as customer_login_router
from policies import router as pol_route

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello Guys!"}

app.include_router(auth_router)
app.include_router(customer_login_router)
app.include_router(pol_route)