# TEST per INSERT SCORE + HALL OF FAME (1+2 funziona!)

import sqlite3
from project import insert_score, extract_hall_of_fame
from unittest.mock import patch
from unittest import mock
import pytest

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