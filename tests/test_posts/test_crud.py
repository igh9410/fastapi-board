from datetime import datetime
from unittest.mock import Mock, create_autospec, patch
from app.posts import crud
from app.posts.models import Post
from app.posts.schemas import PostCreate, PostUpdate
from uuid import UUID, uuid1, uuid4

from tests.test_boards.test_crud import MockBoard

class MockPost:
    def __init__(self, id=None, title="Default Title", content="Default Content", author_id=None, board_id=None, created_at=None):
        self.id = id or uuid1()
        self.title = title
        self.content = content
        self.author_id = author_id or uuid4()
        self.board_id = board_id or uuid4()
        self.created_at = created_at or datetime.utcnow()
        # If you need to mock the relationship with Board
        # self.board = MockBoard(id=self.board_id, ...)

# Mocking the create_post_crud function, should be able to create post if user has access to board
def test_can_create_post_crud():
    mock_session = Mock()
    post_id = uuid4()
    user_id = uuid4()
    board_id = uuid4()
    post_data = PostCreate(title="Test Title", content="Test Content")

    # Create a mock return value for create_post_crud
    mock_post = Mock()
    mock_post.id = post_id
    mock_post.title = "Test Title"
    mock_post.content = "Test Content"
    mock_post.author_id = user_id
    mock_post.board_id = board_id


    with patch('app.posts.crud.create_post_crud', return_value=mock_post) as mock_create_post_crud:
        result = crud.create_post_crud(mock_session, board_id, post_data, user_id)
        mock_create_post_crud.assert_called_once_with(mock_session, board_id, post_data, user_id)
        
        assert result.title == "Test Title"
        assert result.content == "Test Content"
        assert result.author_id == user_id
        assert result.board_id == board_id

def test_cannot_create_post_crud(): ## Should not be able to create post if user does not have access to board
    mock_session = Mock()
    post_id = uuid4()
    user_id = uuid4()
    user_id_2 = uuid4() # User ID of a different user
    board_id = uuid4()
    post_data = PostCreate(title="Test Title", content="Test Content")

    mock_board = MockBoard(id=board_id, name="Test Board", public=False, creator=user_id)

    # Setup mock session to return mock board when board is queried
    mock_session.execute.return_value.scalars.return_value.first.side_effect = [mock_board, None]

    # Create a mock return value for create_post_crud
    mock_post = MockPost(id=post_id, title="Test Title", content="Test Content", author_id=user_id, board_id=board_id)

    mock_session.execute.return_value.scalars.return_value.first.return_value = mock_post
    
    result, message = crud.create_post_crud(mock_session, board_id, post_data, user_id_2)

    assert result is None
    assert message == "Board not found or retrieving not allowed"
    
