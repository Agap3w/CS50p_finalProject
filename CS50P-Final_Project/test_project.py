import sqlite3, pytest, pygame
from project import insert_score, extract_hall_of_fame, get_username_and_mode
from unittest.mock import patch
from unittest import mock

def test_insert_score():
    with sqlite3.connect(":memory:") as db:
        db.execute('CREATE TABLE scores (username TEXT, score INTEGER)')

        # Mock sqlite3.connect to return this in-memory database
        with patch('sqlite3.connect', return_value=db):
            insert_score('test_user', 100)

        result = db.execute('SELECT username, score FROM scores').fetchall()
        assert result == [('test_user', 100)]


# Mock database data
mock_hall_of_fame_data = [
    ('Alice', 100),
    ('Bob', 90),
    ('Charlie', 80),
    ('David', 70),
    ('Eve', 60)
]

# Test for the extract_hall_of_fame function
def test_extract_hall_of_fame():
    # Mock the sqlite3.connect to return a mock connection object
    with mock.patch('sqlite3.connect') as mock_connect:
        # Create a mock cursor
        mock_cursor = mock.MagicMock()
        mock_connect.return_value.__enter__.return_value.cursor.return_value = mock_cursor

        # Mock the cursor's execute method to return the mock data
        mock_cursor.fetchall.return_value = mock_hall_of_fame_data

        # Call the extract_hall_of_fame function
        result = extract_hall_of_fame()

        # Assert the expected result
        assert result == mock_hall_of_fame_data

        # Assert the SQL query was executed correctly
        mock_cursor.execute.assert_called_once_with(
            "SELECT username, MAX(score) as best_score FROM scores GROUP BY username ORDER BY best_score DESC LIMIT ?", (5,)
        )


# Define globals that will be used across the module
screen = None
clock = None

@pytest.fixture
def setup_pygame():
    """Fixture to initialize and clean up Pygame."""
    global screen, clock
    pygame.init()
    screen = pygame.display.set_mode((800, 840))
    clock = pygame.time.Clock()
    
    # Inject the globals into the project module
    import project
    project.screen = screen
    project.clock = clock
    
    yield
    
    pygame.quit()

def test_get_username_and_mode(setup_pygame, monkeypatch):
    # Mock events to simulate user interactions
    events = [
        pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_a, 'unicode': 'a'}),  # Input "A"
        pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_RETURN}),             # Press Enter
        pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'pos': (260, 330), 'button': 1}),  # Click EASY button
        pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'pos': (360, 510), 'button': 1}),  # Click Submit button
    ]
    
    # Keep track of which event to return
    event_index = 0
    
    def mock_get():
        nonlocal event_index
        if event_index < len(events):
            # Return one event at a time
            current_event = [events[event_index]]
            event_index += 1
            return current_event
        return []  # Return empty list when we've used all events

    monkeypatch.setattr(pygame.event, 'get', mock_get)
    
    # Run the function and capture its output
    result = get_username_and_mode()
    
    # Assert the expected result
    assert result == ('A', 'EASY')
