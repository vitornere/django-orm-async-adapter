import pytest
from fastapi.testclient import TestClient
from example.models import Example


class TestDelete:
    @pytest.fixture(autouse=True)
    def setup(self, db):
        self.last_example = Example.objects.last()

    def test_delete_example(self, client: TestClient):
        response = client.delete(f'/examples/{self.last_example.id}')
        assert response.status_code == 204
        examples = Example.objects.all()
        assert len(examples) == 49
        assert examples.first().id != self.last_example.id
