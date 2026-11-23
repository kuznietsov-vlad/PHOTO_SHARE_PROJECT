from fastapi import FastAPI

app = FastAPI(
    title="PhotoShare API",
    description="REST API для завантаження, трансформації, коментування та оцінювання світлин.",
    version="1.0.0",
)


@app.get("/api/healthchecker", tags=["System"])
def healthchecker():
    return {"message": "PhotoShare API is running"}