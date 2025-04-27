import pytest
from todoapp import app # Assuming your Flask app instance is named 'app' in 'todoapp.py'

# Fixture to create a test client for your app
# This allows sending simulated requests to your Flask app without running a live server
@pytest.fixture
def client():
    app.config['TESTING'] = True
    # Use a temporary, separate list for testing to avoid modifying the actual global list
    app.config['TODO_LIST_TEST'] = []
    # You might need to modify your app slightly to use app.config['TODO_LIST_TEST']
    # when TESTING is True, or provide a way to inject/reset the list for tests.
    # For simplicity here, we'll assume the tests can manipulate the global list directly,
    # but be aware this can have side effects if tests run in parallel or are complex.
    # A better approach involves factory patterns or context managers.

    # Reset the global list before each test
    # This requires access to the list, ensure it's accessible (e.g., import it)
    # from todoapp import todo_list # Assuming todo_list is the global list
    # todo_list.clear()

    with app.test_client() as client:
        yield client
    # Cleanup after test if needed
    # todo_list.clear()


def test_index_page_loads(client):
    """Test if the index page ('/') loads successfully."""
    response = client.get('/')
    assert response.status_code == 200
    assert b"<h1>My To-Do List</h1>" in response.data # Check for a key element


def test_add_valid_item(client):
    """Test adding a valid item via /submit."""
    # First, check the initial state (optional, assumes list is empty)
    response = client.get('/')
    assert b"Test Task 1" not in response.data
    assert b"test@example.com" not in response.data

    # Submit a new item
    response = client.post('/submit', data={
        'task': 'Test Task 1',
        'email': 'test@example.com',
        'priority': 'High'
    }, follow_redirects=True) # follow_redirects=True to follow the redirect to '/'

    assert response.status_code == 200
    # Check if the item appears on the index page after submission
    assert b"Test Task 1" in response.data
    assert b"test@example.com" in response.data
    assert b"High" in response.data
    # Optional: Check for success flash message if implemented and configured for testing
    # assert b"To-Do item added successfully!" in response.data


def test_add_invalid_email(client):
    """Test adding an item with an invalid email."""
    response = client.post('/submit', data={
        'task': 'Invalid Email Task',
        'email': 'not-an-email',
        'priority': 'Medium'
    }, follow_redirects=True)

    assert response.status_code == 200
    # Check that the invalid item was NOT added
    assert b"Invalid Email Task" not in response.data
    # Check for error flash message (requires flash messages to be testable)
    # This often involves checking the session or configuring flashing differently for tests.
    # A simpler check might be just ensuring the item isn't in the list.
    # assert b"Invalid or missing email address." in response.data


def test_add_invalid_priority(client):
    """Test adding an item with an invalid priority."""
    response = client.post('/submit', data={
        'task': 'Invalid Priority Task',
        'email': 'valid@email.com',
        'priority': 'Urgent' # Invalid priority
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b"Invalid Priority Task" not in response.data
    # assert b"Invalid priority selected." in response.data


def test_clear_list(client):
    """Test clearing the list via /clear."""
    # Add an item first
    client.post('/submit', data={
        'task': 'Item To Clear',
        'email': 'clear@me.com',
        'priority': 'Low'
    }, follow_redirects=True)

    # Verify it was added
    response = client.get('/')
    assert b"Item To Clear" in response.data

    # Now clear the list
    response_clear = client.post('/clear', follow_redirects=True)
    assert response_clear.status_code == 200

    # Verify the list is empty
    assert b"Item To Clear" not in response_clear.data
    assert b"Your To-Do list is empty!" in response_clear.data # Check for empty message
    # assert b"To-Do list cleared." in response_clear.data # Check for clear flash message
