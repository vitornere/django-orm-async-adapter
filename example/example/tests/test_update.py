import pytest
from fastapi.testclient import TestClient
from example.models import Example


class TestUpdate:
    @pytest.fixture(autouse=True)
    def setup(self, db):
        self.last_example = Example.objects.last()

    def test_update_example(self, client: TestClient):
        response = client.put(
            f'/examples/{self.last_example.id}',
            json={
                'name': 'Example -1',
                'description': 'Description of Example -1'
            }
        )
        assert response.status_code == 200
        assert response.json() == {
            'id': self.last_example.id,
            'name': 'Example -1',
            'description': 'Description of Example -1'
        }
        example = Example.objects.get(id=self.last_example.id)
        assert example.name == 'Example -1'
        assert example.description == 'Description of Example -1'
