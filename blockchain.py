from block import Block, ActionType
from datetime import date
import hashlib
import json

class Blockchain:
    def __init__(self):
        self.blocks = []
        self.genesis_block()

    def genesis_block(self):
        block = Block(ActionType.CREATE.value)
        block.create_election(
            1, {
                1: "Matthew",
                2: "Mark",
                3: "John"
            },
            [
                "userkey_1", "userkey_2"
            ],
            "my_signature", date(2025, 8, 20), date(2025, 8, 25)
        )

        self.blocks.append(block)

    def hash_block(self, block):
        copy_block = block

        content = {
            "type": copy_block.type,
            "prev_hash": copy_block.prev_hash,
            "data": copy_block.data,
            "nonce": copy_block.nonce,
            "timestamp": copy_block.timestamp
        }

        if copy_block.type == "create":
            content["data"]["start_time"] = str(content["data"]["start_time"])
            content["data"]["end_time"] = str(content["data"]["end_time"])

        serialized_content = json.dumps(content, sort_keys=True)

        data = serialized_content.encode("utf-8")

        sha256_hash = hashlib.sha256()

        sha256_hash.update(data)
        return sha256_hash.hexdigest()
    
    def add_block(self, block):
        
        block.prev_hash = self.hash_block(self.blocks[-1])
        mined_hash = self.mine_block(block, 5)
        self.blocks.append(block)
        return mined_hash

    def mine_block(self, block, difficulty):
        diff_metric = "0" * difficulty
        block_hash = self.hash_block(block)
        while not block_hash.startswith(diff_metric):
            block.nonce += 1
            block_hash = self.hash_block(block)

        return block_hash


    

