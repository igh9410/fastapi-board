
from fastapi import APIRouter, status
from app.auth import schemas as auth_schemas
from app.auth.jwt import Token
from app.auth.routes import login_for_access_token, logout, signup
from app.boards import schemas as board_schemas
from app.boards.routes import create_board


router = APIRouter()

# Auth Routes
router.add_api_route("/api/auth/signup", signup, methods=["POST"], response_model=auth_schemas.UserCreate, status_code=status.HTTP_201_CREATED) # Signup Route
router.add_api_route("/api/auth/login", login_for_access_token, methods=["POST"], response_model=Token, status_code=status.HTTP_201_CREATED) # Login Route
router.add_api_route("/api/auth/logout", logout, methods=["DELETE"],  status_code=204) # Logout Route

# Board Routes
router.add_api_route("/api/boards/", create_board, methods=["POST"], response_model=board_schemas.BoardCreate, tags=["Boards"], status_code=status.HTTP_201_CREATED) # Create Board Route

      
