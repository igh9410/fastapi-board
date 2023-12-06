from dotenv import load_dotenv
from fastapi import FastAPI, Request
from starlette.middleware.sessions import SessionMiddleware
from app.db import init_db
from .router import router as app_router
from app.config import settings

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key=settings.SESSION_SECRET_KEY)
app.include_router(app_router)

load_dotenv() ## Load .env file

init_db()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/session")
async def some_endpoint(request: Request):
   
    session_token = request.cookies.get("session_token")
    
  
   

    return {"session_token": session_token}