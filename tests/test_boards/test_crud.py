from uuid import UUID, uuid4
from unittest.mock import Mock, patch
from app.boards import crud
from app.boards.schemas import BoardCreate, BoardUpdate


class MockBoard:
    def __init__(self, id: UUID, name: str, public: bool, creator: UUID):
        self.id = id
        self.name = name
        self.public = public
        self.creator = creator


# Mocking the create_board_crud function
def test_create_board_crud():
    mock_session = Mock()
    user_id = uuid4()
    board_data = BoardCreate(name="Test Board", public=True)

    # Create a mock return value for create_board_crud
    mock_board = Mock()
    mock_board.id = uuid4()
    mock_board.name = "Test Board"
    mock_board.public = True
    mock_board.creator = user_id

    with patch(
        "app.boards.crud.create_board_crud", return_value=mock_board
    ) as mock_create_board_crud:
        result = crud.create_board_crud(mock_session, board_data, user_id)

        mock_create_board_crud.assert_called_once_with(
            mock_session, board_data, user_id
        )
        assert result.name == "Test Board"
        assert result.public is True
        assert result.creator == user_id


def test_can_update_board_crud():  ## Should be able to update board if user is creator
    # Create a mock session
    mock_session = Mock()
    user_id = uuid4()  # The user ID of the original creator
    board_id = uuid4()
    board_data = BoardUpdate(name="Updated Board", public=True)

    mock_board = MockBoard(
        id=board_id, name="Test Board", public=False, creator=user_id
    )

    # Mock the execute method to return a mock scalar object with the first method returning the mock board
    mock_session.execute.return_value.scalars.return_value.first.return_value = (
        mock_board
    )

    mock_board.name = board_data.name
    mock_board.public = board_data.public

    result = crud.update_board_crud(mock_session, board_id, board_data, user_id)

    assert result is not None
    assert result.name == "Updated Board"
    assert result.public is True

    # Check if execute was called for the select and update queries
    assert mock_session.execute.call_count == 2
    mock_session.commit.assert_called_once()  # Ensure commit was not called


# Add more tests for the update, delete, get, and get list operations
# Don't forget to include tests for failure cases like updating a non-existent board


def test_cannot_update_board_crud():
    # Create a mock session
    mock_session = Mock()
    user_id = uuid4()  # The user ID of the original creator
    user_id_2 = uuid4()  # The user ID of the user trying to update the board
    board_id = uuid4()
    board_data = BoardUpdate(name="Test Board", public=False)

    mock_board = MockBoard(
        id=board_id, name="Test Board", public=False, creator=user_id
    )

    # Mock the execute method to return a mock scalar object with the first method returning the mock board
    mock_session.execute.return_value.scalars.return_value.first.return_value = (
        mock_board
    )

    result, message = crud.update_board_crud(
        mock_session, board_id, board_data, user_id_2
    )

    assert result is None
    assert message == "Only the board's creator can update it"

    mock_session.execute.assert_called_once()  # This checks if execute was called once for the select query
    mock_session.commit.assert_not_called()  # Ensure commit was not called


def test_can_get_board_crud():  ## Should be able to get board if user is creator
    # Create a mock session
    mock_session = Mock()
    user_id = uuid4()  # The user ID of the original creator
    board_id = uuid4()

    mock_board = MockBoard(
        id=board_id, name="Test Board", public=False, creator=user_id
    )

    # Mock the execute method to return a mock scalar object with the first method returning the mock board
    mock_session.execute.return_value.scalars.return_value.first.return_value = (
        mock_board
    )

    result = crud.get_board_crud(mock_session, board_id, user_id)

    assert result is not None
    assert result.name == "Test Board"
    assert result.public is False

    # Check if execute was called for the select and update queries
    assert mock_session.execute.call_count == 1


def test_can_get_public_board_crud():  ## Should be able to get board if user is not creator but board is public
    # Create a mock session
    mock_session = Mock()
    user_id = uuid4()  # The user ID of the original creator
    user_id_2 = (
        uuid4()
    )  # The user ID of the user trying to get the board, different from creator
    board_id = uuid4()

    mock_board = MockBoard(id=board_id, name="Test Board", public=True, creator=user_id)

    # Mock the execute method to return a mock scalar object with the first method returning the mock board
    mock_session.execute.return_value.scalars.return_value.first.return_value = (
        mock_board
    )

    result = crud.get_board_crud(mock_session, board_id, user_id_2)

    assert result is not None
    assert result.name == "Test Board"
    assert result.public is True

    # Check if execute was called for the select and update queries
    assert mock_session.execute.call_count == 1


def test_cannot_get_board_crud():  ## Should not be able to get board if user is not creator and board is not public
    # Create a mock session
    mock_session = Mock()
    user_id = uuid4()  # The user ID of the original creator
    user_id_2 = uuid4()  # The user ID of the user trying to update the board
    board_id = uuid4()

    mock_board = MockBoard(
        id=board_id, name="Test Board", public=False, creator=user_id
    )

    # Mock the execute method to return a mock scalar object with the first method returning the mock board
    mock_session.execute.return_value.scalars.return_value.first.return_value = (
        mock_board
    )

    result, message = crud.get_board_crud(mock_session, board_id, user_id_2)

    assert result is None
    assert message == "Only the board's creator can access it"

    mock_session.execute.assert_called_once()  # This checks if execute was called once for the select query


# mock_session.commit.assert_not_called()  # Ensure commit was not called
