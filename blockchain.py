from block import Block, ActionType
from datetime import date, datetime, time
from validator import validate_election, validate_votes
from users import verify_signature, generate_signature, verify_user_pk
import copy
import hashlib
import json

class Blockchain:
    def __init__(self):
        self.blocks = []
        self.genesis_block()

    def genesis_block(self):
        START_DATE = date(2025, 8, 19)
        END_DATE = date(2025, 8, 21)

        START_TIME = time(20, 10, 0)
        END_TIME = time(11, 0, 0)
        block = Block(ActionType.CREATE.value)
        block.create_election(
            1, {
                1: "Matthew",
                2: "Mark",
                3: "John"
            },
            [
                "e9d0113834e213bd0b72f79b07f2edfd3bc04e40490e5dd32c7a2fa207dff676", "2057ba096442f2c4df58fb10510c623dc758da6d937d05505676e5535e2ab9b7"
            ],
            "eb7c7e1023dc482199695cf8e37aea68c7d0646b1c3cef82ff4f7a46482cf31f", generate_signature("genesis", "keys/example.pem" ), datetime.combine(START_DATE, START_TIME), datetime.combine(END_DATE, END_TIME)
        )

        self.blocks.append(block)

    def hash_block(self, block):
        copy_block = copy.deepcopy(block)

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

        if block.type == "create":
            validate_election(block.data["election_data"])
            
        elif block.type == "vote":
            validate_votes(block.data["vote"], self)

        block.prev_hash = self.hash_block(self.blocks[-1])

        mined_hash = self.mine_block(block, 3)
        block.hash = mined_hash
        self.blocks.append(block)
        return mined_hash

    def mine_block(self, block, difficulty):
        diff_metric = "0" * difficulty
        block_hash = self.hash_block(block)
        while not block_hash.startswith(diff_metric):
            block.nonce += 1
            block_hash = self.hash_block(block)

        return block_hash


    

