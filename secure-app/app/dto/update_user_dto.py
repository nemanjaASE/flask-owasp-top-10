from dataclasses import dataclass
from datetime import date

@dataclass
class UpdateUserDTO:
    user_id: str
    first_name: str
    last_name: str
    username: str
    email: str
    birth_date: date