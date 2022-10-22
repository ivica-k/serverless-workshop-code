from uuid import uuid4


class DonationMixin:
    def donation_create(self, donation_dict):
        uid = str(uuid4()).split("-")[-1]

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

            return True

        except Exception as exc:
            self._logger.exception(exc)