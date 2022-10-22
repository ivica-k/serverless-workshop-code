from dataclasses import dataclass


@dataclass
class DBResponse:
    resource_id: str
    success: bool
    error_message: str
    return_value: dict
