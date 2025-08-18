from blockchain import Blockchain
from block import Block, ActionType

def main():

    bc = Blockchain()
    sample_block = Block(ActionType.VOTE.value)
    sample_block_2 = Block(ActionType.VOTE.value)

    sample_block.create_vote(1, 2, "power_study", "AAAAAA")
    sample_block_2.create_vote(1, 1, "westerner", "WWWWWWW")

    bc.add_block(sample_block)
    bc.add_block(sample_block_2)

    for block in bc.blocks:
        print(f"action type: {block.type}")
        print(f"prev Hash: {block.prev_hash}")
        print(f"prev Hash: {type(block.prev_hash)}")
        print(f"Voting data: {block.data}")
        print("\n")

if __name__ == "__main__":
    main()

