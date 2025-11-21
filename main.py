from fastapi import FastAPI
from pydantic import BaseModel

class Vote(BaseModel):
    election_id: int
    candidates: dict[int, str]
    user_keys: list
    public_key: str

app = FastAPI()

