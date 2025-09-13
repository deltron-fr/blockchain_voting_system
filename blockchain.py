from block import Block, ActionType
from datetime import date, datetime, time
from validator import validate_election, validate_votes, verify_sig
from users import hash_pk, get_user_key_data
from keys import generate_signature
from utils import load_chain
import copy
import hashlib
import json

class Blockchain:
    def __init__(self):
        chain_data = load_chain("chain.json")

        if not chain_data:
            self.blocks = []
            self.genesis_block()
        else:
            self.blocks = [Block.from_dict(d) for d in chain_data]

    def genesis_block(self):
        START_DATE = date(2025, 9, 13)
        END_DATE = date(2025, 9, 20)

        START_TIME = time(1, 10, 0)
        END_TIME = time(19, 0, 0)
        block = Block(ActionType.CREATE.value)
        pk = get_user_key_data("keys/example_pub2.pem")
        gen_pk = hash_pk(get_user_key_data("keys/example_pub2.pem"))

        block.create_election(
            1, {
                1: "Matthew",
                2: "Mark",
                3: "John"
            },
            [
                "e9d0113834e213bd0b72f79b07f2edfd3bc04e40490e5dd32c7a2fa207dff676", "2057ba096442f2c4df58fb10510c623dc758da6d937d05505676e5535e2ab9b7",
                "1d036a0601b3692a08e25d121c77f428744dff20def739c08fa8c7dea95b81c0", "960461e3a805122036310be84ffb78b2a6b7d2bbcad93f3e4bac3f2069d48513"
            ],
            gen_pk, "null", datetime.combine(START_DATE, START_TIME), datetime.combine(END_DATE, END_TIME)
        )
        block.data["signature"] = generate_signature(block.data["election_data"], "keys/example2.pem")
        block.data["election_data"]
        if verify_sig(block, pk):
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
            content["data"]["election_data"]["start_time"] = str(content["data"]["election_data"]["start_time"])
            content["data"]["election_data"]["end_time"] = str(content["data"]["election_data"]["end_time"])

        serialized_content = json.dumps(content, sort_keys=True)

        data = serialized_content.encode("utf-8")
        sha256_hash = hashlib.sha256()

        sha256_hash.update(data)
        return sha256_hash.hexdigest()
    

    def add_block(self, block):
        block.data["public_key"] = hash_pk(block.data["public_key"])

        if block.type == "create":
            validate_election(block.data)
            
        elif block.type == "vote":
            validate_votes(block.data, self)

        block.prev_hash = self.hash_block(self.blocks[-1])

        mined_hash = self.mine_block(block, 3)
        block.hash = mined_hash
        self.blocks.append(block)
        self.save_chain()
        return mined_hash

    def mine_block(self, block, difficulty):
        diff_metric = "0" * difficulty
        block_hash = self.hash_block(block)
        while not block_hash.startswith(diff_metric):
            block.nonce += 1
            block_hash = self.hash_block(block)

        return block_hash
    
    def save_chain(self):
        with open("chain.json", mode="w", encoding="utf-8") as f:
            chain = [block.to_dict() for block in self.blocks]
            json.dump(chain, f, indent=4)

        