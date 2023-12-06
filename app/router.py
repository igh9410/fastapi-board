
from fastapi import APIRouter, status
from app.auth import schemas as auth_schemas
from app.auth.routes import login, logout, signup
from app.boards import schemas as board_schemas
from app.boards.routes import create_board_route, delete_board_route, get_board_route, update_board
from app.posts.routes import create_post_route
from app.posts import schemas as post_schemas



router = APIRouter()

# Auth Routes
router.add_api_route("/api/auth/signup", signup, methods=["POST"], response_model=auth_schemas.UserCreate, status_code=status.HTTP_201_CREATED) # Signup Route
router.add_api_route("/api/auth/login", login, methods=["POST"], response_model=auth_schemas.Token, status_code=status.HTTP_201_CREATED) # Login Route
router.add_api_route("/api/auth/logout", logout, methods=["DELETE"],  status_code=status.HTTP_204_NO_CONTENT) # Logout Route

# Board Routes
router.add_api_route("/api/boards/", create_board_route, methods=["POST"], response_model=board_schemas.BoardCreate, tags=["Boards"], status_code=status.HTTP_201_CREATED) # Create Board Route
router.add_api_route("/api/boards/{id}", update_board, methods=["PATCH"], response_model=board_schemas.BoardUpdate, tags=["Boards"], status_code=status.HTTP_200_OK) # Update Board Route
router.add_api_route("/api/boards/{id}", delete_board_route, methods=["DELETE"], response_model=None, tags=["Boards"], status_code=status.HTTP_204_NO_CONTENT) # Delete Board Route
router.add_api_route("/api/boards/{id}", get_board_route, methods=["GET"], response_model=board_schemas.BoardGet, tags=["Boards"], status_code=status.HTTP_200_OK) # Get Board Route      

# Post Routes
router.add_api_route("/api/boards/{board_id}/posts/", create_post_route, methods=["POST"], response_model=post_schemas.PostCreate, tags=["Posts"], status_code=status.HTTP_201_CREATED) # Create Post Route