
from fastapi import APIRouter, status
from app.auth import schemas
from app.auth.jwt import Token
from app.auth.routes import login_for_access_token, logout, signup


router = APIRouter()


router.add_api_route("/api/auth/signup", signup, methods=["POST"], response_model=schemas.UserCreate, status_code=status.HTTP_201_CREATED) # Signup Route
router.add_api_route("/api/auth/login", login_for_access_token, methods=["POST"], response_model=Token, status_code=status.HTTP_201_CREATED) # Login Route
router.add_api_route("/api/auth/logout", logout, methods=["DELETE"],  status_code=204) # Logout Route

      
