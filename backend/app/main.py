from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import health 

app = FastAPI(title="Legal Advisor AI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)