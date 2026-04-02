import pytest
from app import app, programs

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'ACEest Fitness & Gym' in response.data

def test_programs_json(client):
    response = client.get('/programs')
    assert response.status_code == 200
    data = response.get_json()
    assert 'Fat Loss (FL)' in data
    assert 'workout' in data['Fat Loss (FL)']

def test_program_detail(client):
    response = client.get('/program/Fat Loss (FL)')
    assert response.status_code == 200
    assert b'Fat Loss (FL)' in response.data

def test_program_not_found(client):
    response = client.get('/program/Unknown')
    assert response.status_code == 404

def test_client_form(client):
    response = client.get('/client')
    assert response.status_code == 200
    assert b'Client Profile' in response.data

def test_client_post(client):
    response = client.post('/client', data={
        'name': 'John Doe',
        'age': '25',
        'weight': '70',
        'program': 'Fat Loss (FL)'
    })
    assert response.status_code == 200
    assert b'John Doe' in response.data
