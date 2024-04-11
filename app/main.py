# app/main.py
from fastapi import FastAPI
from . import routes  # This will import the routes you define

app = FastAPI()

app.include_router(routes.router)  # Assuming you define a router in your routes.py
