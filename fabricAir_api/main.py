import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.controllers.controller_routers import api_router

app = FastAPI(
    title="fabricAirApi", openapi_url="/openapi.json"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)

if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, log_level="info", reload=True)
