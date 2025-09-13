from enum import Enum
import time
from datetime import datetime
import copy

class ActionType(Enum):
    CREATE = "create"
    VOTE = "vote"

class Block:
    def __init__(self, type, prev_hash=None, data=None, nonce=0, timestamp=None, hash_val=None):
        self.type = type
        self.prev_hash = prev_hash if prev_hash is not None else "0" * 64
        self.hash = hash_val if hash_val is not None else "0" * 64
        self.data = data if data is not None else {}
        self.nonce = nonce
        self.timestamp = timestamp if timestamp is not None else int(time.time())

    def create_election(self, election_id, candidates, user_keys, public_key, signature, start_time, end_time):
        self.data["election_data"] = {
            "election_id" : election_id,
            "candidates" : candidates,
            "user_keys" : user_keys,
            "start_time" : start_time,
            "end_time" : end_time
        }
        self.data["public_key"] = public_key
        self.data["signature"] = signature
        

    def create_vote(self, election_id, candidate_id, signature, public_key):
        self.data["vote"] = {
            "election_id" : election_id,
            "candidate_id" : candidate_id
        }
        self.data["signature"] = signature
        self.data["public_key"] = public_key

    def to_dict(self):
        data_copy = copy.deepcopy(self.data)

        if self.type == "create":
            data_copy["election_data"]["start_time"] = data_copy["election_data"]["start_time"].isoformat()
            data_copy["election_data"]["end_time"] = data_copy["election_data"]["end_time"].isoformat()

        return {
            "type": self.type,
            "prev_hash": self.prev_hash,
            "data": data_copy,
            "nonce": self.nonce,
            "timestamp": self.timestamp,  
            "hash": self.hash
        }


    @classmethod
    def from_dict(cls, data):
        block_type = data["type"]
        block_data = copy.deepcopy(data["data"])

        if block_type == "create":
            block_data["election_data"]["start_time"] = datetime.fromisoformat(block_data["election_data"]["start_time"])
            block_data["election_data"]["end_time"] = datetime.fromisoformat(block_data["election_data"]["end_time"])

            for k, _ in block_data["election_data"]["candidates"].items():
                k = int(k)

        return cls(
            type=block_type,
            prev_hash=data["prev_hash"],
            data=block_data,
            nonce=data["nonce"],
            timestamp=data["timestamp"],
            hash_val=data.get("hash")
        )

    

