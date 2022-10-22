import json

from app import app
from chalice.test import Client


def test_donor_signup():
    json_payload = {
        "first_name": "ivica",
        "city": "Amsterdam",
        "type": "A+",
        "email": "ivica@server.com"
    }

    with Client(app) as client:
        response = client.http.post(
            "/donor/signup",
            headers={"Content-Type": "application/json"},
            body=json.dumps(json_payload)
        )

        assert response.status_code == 200
        assert response.json_body == json_payload
