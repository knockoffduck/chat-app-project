from main import app

def test_home_page():
    """ 
        GIVEN a Flask application configured for testing
        WHEN the '/' page is requested (GET)
        THEN check the response is valid
    """
    with app.test_client() as client:
        response = client.get('/')
        assert response.status_code == 200

def test_chat_page():
    """ 
        GIVEN a Flask application configured for testing
        WHEN the '/chat/' page is requested (GET)
        THEN check the response is valid
    """
    with app.test_client() as client:
        response = client.get('/chat/')
        assert response.status_code == 200
