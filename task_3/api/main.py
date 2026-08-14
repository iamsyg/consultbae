# api/main.py

from fastapi import FastAPI, Depends, HTTPException
from api.db.db import get_connection
from dotenv import load_dotenv

app = FastAPI()

load_dotenv()


def get_db():
    conn = get_connection()
    try:
        yield conn
    finally:
        conn.close()


@app.get("/health/db")
def database_health(db=Depends(get_db)):
    try:
        with db.cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()

        return {
            "database": "connected",
            "result": result[0]
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Database connection failed: {str(e)}"
        )