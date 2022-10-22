import json
import os
from unittest import mock

from chalice.test import Client

ENV = os.getenv("ENV", "dev")
first_name = os.getenv("WORKSHOP_NAME", "ivica")  # replace with your own name of course


@mock.patch.dict(os.environ, {"TABLE_NAME": f"{first_name}-savealife-{ENV}"})
def test_donor_signup():
    from app import app

    json_payload = {
        "first_name": "ivica",
        "city": "Amsterdam",
        "type": "A+",
        "email": "ivica@server.com",
    }

    with Client(app) as client:
        response = client.http.post(
            "/donor/signup",
            headers={"Content-Type": "application/json"},
            body=json.dumps(json_payload),
        )

        assert response.status_code == 200
        assert response.json_body.get("success")