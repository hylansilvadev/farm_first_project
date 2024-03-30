from tests.conftest import client


def test_hello_world():
    response = client.get('root')
    assert response.status_code == 200
    assert response.json() == {'message': 'Hello World!'}
