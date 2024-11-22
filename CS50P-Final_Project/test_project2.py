# Test per FZ2 (to be done)

import pytest
import sqlite3
from unittest import mock
from project import extract_hall_of_fame  # Adjust the import based on the location of your function

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