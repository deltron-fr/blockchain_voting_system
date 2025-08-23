from blockchain import Blockchain
from block import Block, ActionType
from datetime import datetime, time, date

def main():
    START_DATE = date(2025, 8, 23)
    END_DATE = date(2025, 8, 25)

    START_TIME = time(9, 30, 0)
    END_TIME = time(11, 0, 0)


    for block in bc.blocks:
        print(f"action type: {block.type}")
        print(f"prev Hash: {block.prev_hash}")
        print(f"Hash: {block.hash}")
        print(f"Voting data: {block.data["signature"]}")
        print("\n")



