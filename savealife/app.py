import logging

from os import getenv
from chalice import Chalice
from chalicelib.db import get_app_db

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass

first_name = getenv("WORKSHOP_NAME", "ivica")  # replace with your own name of course

app = Chalice(app_name=f"{first_name}-savealife")
app.log.setLevel(logging.DEBUG)


@app.route("/donor/signup", methods=["POST"])
def donor_signup():
    body = app.current_request.json_body

    app.log.debug(f"Received JSON payload: {body}")

    return get_app_db().donor_signup(body)


@app.route("/donation/create", methods=["POST"])
def donation_create():
    body = app.current_request.json_body

    app.log.debug(f"Received JSON payload: {body}")

    return get_app_db().donation_create(body)
