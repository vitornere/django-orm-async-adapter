import pytest
from typing import List
from fastapi.testclient import TestClient
from example.models import Example


class TestGet:
    @pytest.fixture(autouse=True)
    def setup(self, db):
        self.last_example = Example.objects.last()

    def test_get_all(self, client: TestClient):
        response = client.get('/examples/')
        assert response.status_code == 200
        response_json: List[dict] = response.json()
        example_ids = [example.pop('id') for example in response_json]
        response_json == [
            {
                'id': i,
                'name': f'Example {i}',
                'description': f'Description of Example {i}'
            } for i in example_ids
        ]

    def test_get_one(self, client: TestClient):
        response = client.get(f'/examples/{self.last_example.id}')
        assert response.status_code == 200
        response_json = response.json()
        response_json == [{
            'name': f'Example {self.last_example.id}',
            'description': f'Description of Example {self.last_example.id}'
        }]

    def test_get_decreasing(self, client: TestClient):
        response = client.get('/examples/?order_type=desc')
        assert response.status_code == 200
        response_json: List[dict] = response.json()
        example_ids = [example.pop('id') for example in response_json]
        response_json == [
            {
                'id': i,
                'name': f'Example {i}',
                'description': f'Description of Example {i}'
            } for i in example_ids
        ]

    def test_get_filtered(self, client: TestClient):
        response = client.get(
            f'/examples/?partial_name={self.last_example.id}'
        )
        assert response.status_code == 200
        response_json: List[dict] = response.json()
        response_json == [{
            'id': self.last_example.id,
            'name': self.last_example.name,
            'description': self.last_example.description
        }]

    def test_get_paginated(self, client: TestClient):
        response = client.get('/examples/?page=2&per_page=5')
        assert response.status_code == 200
        response_json: List[dict] = response.json()
        example_ids = [example.pop('id') for example in response_json]
        response_json == [
            {
                'id': i,
                'name': f'Example {i}',
                'description': f'Description of Example {i}'
            } for i in example_ids
        ]
