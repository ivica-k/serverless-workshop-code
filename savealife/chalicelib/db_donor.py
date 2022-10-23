from uuid import uuid4
from . import DBResponse

from boto3.dynamodb.conditions import Key


class DonorMixin:

    def donor_signup(self, donor_dict):
        uid = str(uuid4()).split("-")[-1]
        db_response = DBResponse(resource_id="", success=False, error_message="", return_value={})

        try:
            self._table.put_item(
                Item={
                    "first_name": donor_dict.get("first_name"),
                    "city": donor_dict.get("city"),
                    "type": donor_dict.get("type"),
                    "email": donor_dict.get("email"),
                    "PK": f"DONOR#{uid}",
                }
            )
            self._logger.debug(f"Inserted donor '{donor_dict.get('email')}' into DynamoDB table '{self._table}'")

            db_response.success = True
            db_response.resource_id = uid

            return db_response

        except Exception as exc:
            db_response.success = False
            db_response.error_message = str(exc)

            self._logger.exception(exc)

        finally:
            return db_response


    def donors_all(self):
        db_response = DBResponse(resource_id="", success=False, error_message="", return_value={})
        try:
            response = self._table.scan(
                FilterExpression=Key("PK").begins_with("DONOR"),
                ReturnConsumedCapacity="TOTAL",
            )

            donors = response.get("Items")

            self._logger.debug(f"Consumed {response.get('ConsumedCapacity').get('CapacityUnits')} capacity units")
            self._logger.debug(f"Fetched {len(donors)} donor(s)")

            if response.get("ResponseMetadata").get('HTTPStatusCode') == 200:
                db_response.success = True
                db_response.return_value = donors

            return db_response

        except Exception as exc:
            db_response.success = False
            db_response.error_message = str(exc)

            self._logger.exception(exc)

        finally:
            return db_response