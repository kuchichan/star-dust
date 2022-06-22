from starlette import status
from starlette.testclient import TestClient


def test_me_endpoint(authorized_client: TestClient):
    response = authorized_client.get(url="/api/v1/users/me")
    assert response.status_code == status.HTTP_200_OK
