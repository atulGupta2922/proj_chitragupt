from fastapi import FastAPI
from app.routes import app_routes
from app.middleware.webhook_validator import WebhookValidator

app = FastAPI()

@app.get("/healthcheck")
def healthcheck():
    return {"message": "proj_chitragupt is running!"}


# app.add_middleware(WebhookValidator)

app.include_router(app_routes.router)