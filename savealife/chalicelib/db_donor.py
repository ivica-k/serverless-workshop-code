from uuid import uuid4


class DonorMixin:
    def donor_signup(self, donor_dict):
        uid = str(uuid4()).split("-")[-1]

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
            self._logger.debug(
                f"Inserted donor '{donor_dict.get('email')}' into DynamoDB table '{self._table}'"
            )

            return True

        except Exception as exc:
            self._logger.exception(exc)