import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health(client):
    response = client.get('/health')
    assert response.status_code == 200
    assert response.get_json()['status'] == 'OK'

def test_count(client):
    response = client.get('/count')
    assert response.status_code == 200
    assert 'count' in response.get_json()

def test_get_all_pictures(client):
    response = client.get('/picture')
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)

def test_get_picture_by_valid_id(client):
    response = client.get('/picture/0')
    assert response.status_code == 200
    assert response.get_json()['id'] == '0'

def test_get_picture_by_invalid_id(client):
    response = client.get('/picture/999')
    assert response.status_code == 404

def test_get_pictures_count_matches(client):
    response = client.get('/picture')
    data = response.get_json()
    assert len(data) >= 2

def test_get_picture_structure(client):
    response = client.get('/picture/0')
    data = response.get_json()
    assert 'id' in data
    assert 'pic_url' in data
    assert 'user_id' in data

def test_post_picture(client):
    new_pic = {"id": "2", "pic_url": "image3.jpg", "user_id": "3"}
    response = client.post('/picture', json=new_pic)
    assert response.status_code == 201
    assert response.get_json()['id'] == '2'

def test_update_picture(client):
    updated = {"pic_url": "updated.jpg"}
    response = client.put('/picture/0', json=updated)
    assert response.status_code == 200
    assert response.get_json()['pic_url'] == 'updated.jpg'

def test_delete_picture(client):
    response = client.delete('/picture/1')
    assert response.status_code == 200