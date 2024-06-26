from dataclasses import dataclass
from datetime import date

@dataclass
class UserRegistrationDTO:
    first_name: str
    last_name: str
    username: str
    email: str
    password: str
    birth_date: date