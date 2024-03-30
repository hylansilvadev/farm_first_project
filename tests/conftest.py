import pytest
from fastapi.testclient import TestClient

from app.main import app

TEST_URL = '/students/'

LIST_STUDENTS = [
    {
        'course': 'Test Course',
        'email': 'test@test.com',
        'name': 'User Test',
    },
    {
        'course': 'Test Course',
        'email': 'test@test.com',
        'name': 'User Test',
    },
    {
        'course': 'Test Course',
        'email': 'test@test.com',
        'name': 'User Test',
    },
    {
        'course': 'Test Course',
        'email': 'test@test.com',
        'name': 'User Test',
    },
    {
        'course': 'Test Course',
        'email': 'test@test.com',
        'name': 'User Test',
    },
    {
        'course': 'Test Course',
        'email': 'test@test.com',
        'name': 'User Test',
    },
]

@pytest.fixture(scope='module')
async def create_data_students():
    async with TestClient(app) as client:
        for student_data in LIST_STUDENTS:
            response = await client.post(TEST_URL, json=student_data)
            assert response.status_code == 201

            