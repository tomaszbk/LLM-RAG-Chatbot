from fastapi import FastAPI

from app.routes.generate import router as generate_router
from app.routes.load import router as load_router

app = FastAPI()


app.include_router(generate_router)
app.include_router(load_router)
