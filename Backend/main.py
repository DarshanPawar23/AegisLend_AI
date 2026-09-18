from fastapi import FastAPI
from sqlalchemy import text

from configs.firebase import initialize_firebase
from storage.mysql.connection import engine

from routes.user_routes.user_registration import (
    router as user_registration_router
)

app = FastAPI(
    title="AegisLend AI",
    version="1.0.0"
)

@app.on_event("startup")
def startup():

    try:
        initialize_firebase()
        print("Firebase Initialized Successfully!")

    except Exception as e:
        print(f"Firebase Initialization Failed: {e}")

    try:
        with engine.connect() as connection:

            connection.execute(
                text("SELECT 1")
            )

            print("MySQL Connected Successfully!")

    except Exception as e:
        print(f"MySQL Connection Failed: {e}")


app.include_router(
    user_registration_router
)

@app.get("/")
def root():

    return {
        "message": "AegisLend AI Backend is Running 🚀"
    }