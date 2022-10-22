import logging
from os import getenv

import boto3

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass

ENV = getenv("ENV", "dev")
first_name = getenv("WORKSHOP_NAME", "ivica")  # replace with your own name of course

logger = logging.getLogger(f"{first_name}-savealife")

_DB = None
TABLE_NAME = getenv("TABLE_NAME")


def get_app_db():
    global _DB

    if _DB is None:
        _DB = SavealifeDB(
            table=boto3.resource("dynamodb").Table(TABLE_NAME), logger=logger
        )

    return _DB


class SavealifeDB:
    def __init__(self, table, logger):
        self._table = table
        self._logger = logger

    def donor_signup(self, donor_dict):
        try:
            self._table.put_item(
                Item={
                    "first_name": donor_dict.get("first_name"),
                    "city": donor_dict.get("city"),
                    "type": donor_dict.get("type"),
                    "email": donor_dict.get("email"),
                }
            )
            self._logger.debug(
                f"Inserted donor '{donor_dict.get('email')}' into DynamoDB table '{self._table}'"
            )

            return True

        except Exception as exc:
            self._logger.exception(exc)
