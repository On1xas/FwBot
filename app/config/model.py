from pydantic import BaseModel
from typing import List
from uuid import UUID
import datetime

class User(BaseModel):
    client_id: int
    token: str
    expired_time: str
    locale: str

class GameAccount(BaseModel):
    email: str
    pw: UUID

class AllianceConfiguration(BaseModel):
    count_open_window: int
    size_window_x: int
    size_window_y: int
    path_to_exe: str
    accounts: List[GameAccount]


class Config(BaseModel):
    user: User
    alliance_config: AllianceConfiguration
    version: str
