from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy import text
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.routes import auth

app = FastAPI(
    title="PhotoShare API",
    description="REST API для завантаження, трансформації, коментування та оцінювання світлин.",
    version="1.0.0",
)

app.include_router(auth.router)


@app.get("/api/healthchecker", tags=["System"])
def healthchecker(db: Session = Depends(get_db)):
    try:
        result = db.execute(text("SELECT 1")).fetchone()
        if result is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database is not configured correctly",
            )
        return {"message": "PhotoShare API is running and connected to PostgreSQL"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error connecting to the database: {e}",
        )