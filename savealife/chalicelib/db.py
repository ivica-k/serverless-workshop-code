import logging
from os import getenv

import boto3

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass

from .db_donation import DonationMixin
from .db_donor import DonorMixin


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


class SavealifeDB(DonorMixin, DonationMixin):
    def __init__(self, table, logger):
        self._table = table
        self._logger = logger