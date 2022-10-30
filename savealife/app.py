import logging

from os import getenv
from chalice import Chalice, Response
from chalicelib.db import get_app_db
from chalicelib.utils import chunk_list
from dataclasses import asdict

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass

first_name = getenv("WORKSHOP_NAME", "ivica")  # replace with your own name of course
stream_arn = getenv("STREAM_ARN")

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


@app.route("/donor/{donor_id}", methods=["GET"])
def donor_by_id(donor_id):
    db_response = get_app_db().donor_by_id(donor_id)

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


@app.route("/donation/{donation_id}", methods=["GET"])
def donation_by_id(donation_id):
    db_response = get_app_db().donation_by_id(donation_id)

    app.log.debug(f"DBResponse: {db_response}")

    return Response(
        body=asdict(db_response),
        status_code=200 if db_response.success else 400
    )


@app.on_dynamodb_record(stream_arn=stream_arn)
def handle_stream(event):
    for record in event:
        stream_data = record.new_image

        city_name = stream_data.get("city").get("S")
        db_response = get_app_db().donors_by_city(city_name)
        all_emails = [elem.get("email") for elem in db_response.return_value]

        batched_emails = list(chunk_list(all_emails, 50))

        app.log.debug(f"Gathered '{len(all_emails)}' from donors")
