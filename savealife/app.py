from os import getenv
from chalice import Chalice

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass

first_name = getenv("WORKSHOP_NAME", "ivica")  # replace with your own name of course

app = Chalice(app_name=f"{first_name}-savealife")

@app.route("/donor/signup", methods=["POST"])
def donor_signup():
    body = app.current_request.json_body

    return body