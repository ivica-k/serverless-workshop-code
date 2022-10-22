from uuid import uuid4
from . import DBResponse


class DonationMixin:
    def donation_create(self, donation_dict):
        uid = str(uuid4()).split("-")[-1]
        db_response = DBResponse(resource_id="", success=False, error_message="", return_value={})

        try:
            self._table.put_item(
                Item={
                    "city": donation_dict.get("city"),
                    "datetime": donation_dict.get("datetime"),
                    "address": donation_dict.get("address"),
                    "PK": f"DONATION#{uid}",
                }
            )
            self._logger.debug(
                f"Inserted donation '{donation_dict.get('city')}, {donation_dict.get('address')}' "
                f"into DynamoDB table '{self._table}'"
            )

            db_response.success = True
            db_response.resource_id = uid

            return db_response

        except Exception as exc:
            db_response.success = False
            db_response.error_message = str(exc)

            self._logger.exception(exc)

        finally:
            return db_response