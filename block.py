from enum import Enum
import time

class ActionType(Enum):
    CREATE = "create"
    VOTE = "vote"

class Block:
    def __init__(self, type):
        self.type = type
        self.prev_hash = "0" * 64
        self.data = {}
        self.nonce = 0
        self.timestamp = int(time.time())

    def create_election(self, election_id, candidates, user_keys, public_key, signature, start_time, end_time):
        self.data["election_id"] = election_id
        self.data["candidates"] = candidates
        self.data["user_keys"] = user_keys
        self.data["public_key"] = public_key
        self.data["signature"] = signature
        self.data["start_time"] = start_time
        self.data["end_time"] = end_time

    def create_vote(self, election_id, candidate_id, signature, public_key):
        self.data["election_id"] = election_id
        self.data["candidate_id"] = candidate_id
        self.data["signature"] = signature
        self.data["public_key"] = public_key

    

