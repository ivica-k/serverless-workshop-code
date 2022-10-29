from uuid import uuid4
from . import DBResponse

from boto3.dynamodb.conditions import Key

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
                    "SK": f"CITY#{donation_dict.get('city')}"
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

    def donations_all(self):
        db_response = DBResponse(resource_id="", success=False, error_message="", return_value={})
        try:
            response = self._table.scan(
                FilterExpression=Key("PK").begins_with("DONATION"),
                ReturnConsumedCapacity="TOTAL",
            )

            donations = response.get("Items")

            self._logger.debug(f"Consumed {response.get('ConsumedCapacity').get('CapacityUnits')} capacity units")
            self._logger.debug(f"Fetched {len(donations)} donation(s)")

            if response.get("ResponseMetadata").get('HTTPStatusCode') == 200:
                db_response.success = True
                db_response.return_value = donations

            return db_response

        except Exception as exc:
            db_response.success = False
            db_response.error_message = str(exc)

            self._logger.exception(exc)

        finally:
            return db_response

    def donation_by_id(self, donation_id):
        db_response = DBResponse(resource_id="", success=False, error_message="", return_value={})
        try:
            response = self._table.query(
                KeyConditionExpression="PK = :PK",
                ExpressionAttributeValues={
                    ":PK": f"DONATION#{donation_id}"
                },
                ReturnConsumedCapacity="TOTAL",
            )

            self._logger.debug(f"Consumed {response.get('ConsumedCapacity').get('CapacityUnits')} capacity units")
            self._logger.debug(f"Retrieved donation with id {donation_id}")

            if response.get("ResponseMetadata").get('HTTPStatusCode') == 200:
                db_response.success = True
                db_response.return_value = response.get("Items")[0]

            return db_response

        except Exception as exc:
            db_response.success = False
            db_response.error_message = str(exc)

            self._logger.exception(exc)

        finally:
            return db_response