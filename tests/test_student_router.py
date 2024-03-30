import pytest
from httpx import AsyncClient

from app.main import app

TEST_URL = '/students/'

DATA = {
    'course': 'Test Course',
    'email': 'test@test.com',
    'name': 'User Test',
}


@pytest.mark.asyncio
async def test_create_student_and_before_delete():
    async with AsyncClient(app=app, base_url='http://test') as client:

        create = await client.post(TEST_URL, json=DATA)

        doc = create.json()
        inserted_id = doc['id']

        assert create.status_code == 201
        assert doc['course'] == 'Test Course'
        assert doc['email'] == 'test@test.com'
        assert doc['name'] == 'User Test'

        delete = await client.delete(TEST_URL + f'{inserted_id}')
        assert delete.status_code == 204


@pytest.mark.asyncio
async def test_create_student_get_data_and_before_delete():
    async with AsyncClient(app=app, base_url='http://test') as client:

        create = await client.post(TEST_URL, json=DATA)

        doc_view = create.json()
        inserted_id = doc_view['id']

        assert create.status_code == 201
        assert doc_view['course'] == 'Test Course'
        assert doc_view['email'] == 'test@test.com'
        assert doc_view['name'] == 'User Test'

        read = await client.get(TEST_URL + f'{inserted_id}')

        doc_read = read.json()

        assert read.status_code == 200
        assert doc_read['course'] == 'Test Course'
        assert doc_read['email'] == 'test@test.com'
        assert doc_read['name'] == 'User Test'

        delete = await client.delete(TEST_URL + f'{inserted_id}')

        assert delete.status_code == 204


@pytest.mark.asyncio
async def test_get_list_of_students(create_data_students):
    async with AsyncClient(app=app, base_url='http://test') as client:
    
        get_all = await client.get(TEST_URL)
        assert get_all.status_code == 200
        