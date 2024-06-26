from dataclasses import dataclass, field
from typing import List

@dataclass
class CreatePostDTO:
    title: str
    body: str
    user_id: str
    categories: List[str] = field(default_factory=list)