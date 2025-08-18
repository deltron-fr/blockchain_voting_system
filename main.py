from blockchain import Blockchain
from block import Block, ActionType

def main():

    bc = Blockchain()
    sample_block = Block(ActionType.VOTE, 123, 
                         {
                             "election_id" : 1,
                             "candidate" : 2,
                             "signature": "kelz"
                         }, 20)
    sample_block_2 = Block(ActionType.VOTE, 123, 
                         {
                             "election_id" : 1,
                             "candidate" : 2,
                             "signature": "kelz_3"
                         }, 23)
    bc.add_block(sample_block)
    bc.add_block(sample_block_2)

    for block in bc.blocks:
        print(f"action type: {block.type}")
        print(f"Voting data: {block.data}")

if __name__ == "__main__":
    main()

