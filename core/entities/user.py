from dataclasses import dataclass


@dataclass
class User:
    tg_id: int
    username: str
    first_name: str
    last_name: str = None
