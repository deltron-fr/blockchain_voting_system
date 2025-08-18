from block import Block, ActionType
from datetime import date
import hashlib

class Blockchain:
    def __init__(self):
        self.blocks = []
        self.genesis_block()

    def genesis_block(self):
        block = Block(ActionType.CREATE, "00000", 
                      {
                          "election_id": 1,
                          "candidate_ids": {
                              1 : "Peter",
                              2 : "Matthew",
                              3 : "Mark"
                          },
                          "start_time_of_election": date(2025, 8, 23)
                      }, 20)
        self.blocks.append(block)

    def hash_block(self, block):
        content = {
            "type": block.type,
            "prev_hash": block.prev_hash,
            "data": block.data,
            "nonce": block.nonce,
            "timestamp": block.timestamp
        }

        data = content.encode("utf-8")

        sha256_hash = hashlib.sha256()

        sha256_hash.update(data)
        return sha256_hash.hexdigest()

    def add_block(self, block):
        block.prev_hash = self.hash_block(self.blocks[-1])
        self.blocks.append(block)

