# Test per FZ3 (to be done)

import sqlite3
from project import insert_score
from unittest.mock import patch

def test_insert_score():
    with sqlite3.connect(":memory:") as db:
        db.execute('CREATE TABLE scores (username TEXT, score INTEGER)')

        # Mock sqlite3.connect to return this in-memory database
        with patch('sqlite3.connect', return_value=db):
            insert_score('test_user', 100)

        result = db.execute('SELECT username, score FROM scores').fetchall()
        assert result == [('test_user', 100)]

