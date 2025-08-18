from enum import Enum
import time

class ActionType(Enum):
    CREATE = "create"
    VOTE = "vote"

class Block:
    def __init__(self, type, prev_hash, nonce):
        self.type = type
        self.prev_hash = prev_hash
        self.data = {}
        self.nonce = nonce
        self.timestamp = int(time.time())

    def create_election(self, election_id, candidates, user_keys, signature, start_time, end_time):
        self.data["election_id"] = election_id
        self.data["candidates"] = candidates
        self.data["user_keys"] = user_keys
        self.data["signature"] = signature
        self.data["start_time"] = start_time
        self.data["end_time"] = end_time

    def create_vote(self, election_id, candidate_id, signature, public_key):
        self.data["election_id"] = election_id
        self.data["candidate_id"] = candidate_id
        self.data["signature"] = signature
        self.data["public_key"] = public_key
