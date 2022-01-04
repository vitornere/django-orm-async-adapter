from fastapi.testclient import TestClient
from example.models import Example


class TestCreate():
    def test_create_example(self, client: TestClient):
        response = client.post('/examples/', json={
            'name': 'Example 51',
            'description': 'Description of Example 51'
        })
        assert response.status_code == 201
        response_json: dict = response.json()
        example_id = response_json.pop('id')
        assert response_json == {
            'name': 'Example 51',
            'description': 'Description of Example 51'
        }
        assert Example.objects.filter(id=example_id).last() is not None
