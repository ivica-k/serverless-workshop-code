import logging

from os import getenv
from chalice import Chalice, Response
from chalicelib.db import get_app_db
from dataclasses import asdict

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

    db_response = get_app_db().donor_signup(body)

    app.log.debug(f"DBResponse: {db_response}")

    return Response(
        body=asdict(db_response),
        status_code=200 if db_response.success else 400
    )


@app.route("/donors", methods=["GET"])
def donors_get():
    db_response = get_app_db().donors_all()

    app.log.debug(f"DBResponse: {db_response}")

    return Response(
        body=asdict(db_response),
        status_code=200 if db_response.success else 400
    )


@app.route("/donation/create", methods=["POST"])
def donation_create():
    body = app.current_request.json_body

    app.log.debug(f"Received JSON payload: {body}")

    db_response = get_app_db().donation_create(body)

    app.log.debug(f"DBResponse: {db_response}")

    return Response(
        body=asdict(db_response),
        status_code=200 if db_response.success else 400
    )


@app.route("/donations", methods=["GET"])
def donations_get():
    db_response = get_app_db().donations_all()

    app.log.debug(f"DBResponse: {db_response}")

    return Response(
        body=asdict(db_response),
        status_code=200 if db_response.success else 400
    )
