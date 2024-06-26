from dataclasses import dataclass

@dataclass
class ResetPasswordDTO:
    password: str
    token: str