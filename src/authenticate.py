from requests import post, Response

from config import config


def get_token() -> Response:
    body = {
        "grant_type": "password",
        "client_id": "dsis-data",
        "username": config.user_id,
        "password": config.password,
    }
    response = post(
        url="https://dssecurity1242.dsis.equinor.com:9243"
        "/auth/realms/DecisionSpace_Integration_Server/protocol/openid-connect/token",
        verify=False,
        data=body,
    )
    json = response.json()
    return json["access_token"]
