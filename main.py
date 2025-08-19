from blockchain import Blockchain
from block import Block, ActionType
from datetime import datetime, time, date

def main():

    bc = Blockchain()
    sample_block = Block(ActionType.VOTE.value)
    sample_block_2 = Block(ActionType.VOTE.value)
    sample_block_3 = Block(ActionType.CREATE.value)
    #sample_block_4 = Block(ActionType.VOTE.value)

    START_DATE = date(2025, 8, 18)
    END_DATE = date(2025, 8, 21)

    START_TIME = time(10, 30, 0)
    END_TIME = time(11, 0, 0)

    sample_block.create_vote(1, 2, "power_study", "b8d09bda055423a85ad3f6e2b9c838d0abbd6346e06b355b20592d9008cc0986")
    sample_block_2.create_vote(1, 1, "westerner", "e513a4ece47e72ebfebbf0362c417ee3b712826921ef97e804b092e78cf3f4ef")
    sample_block_3.create_election(2, {1: "Mark", 2: "Jerome"}, ["user1", "user2", "user3"], "AAAAAA", "my_sig", datetime.combine(START_DATE, START_TIME), datetime.combine(END_DATE, END_TIME))

    bc.add_block(sample_block)
    bc.add_block(sample_block_2)
    bc.add_block(sample_block_3)


    for block in bc.blocks:
        print(f"action type: {block.type}")
        print(f"prev Hash: {block.prev_hash}")
        print(f"Hash: {block.hash}")
        print(f"Voting data: {block.data}")
        print("\n")

if __name__ == "__main__":
    main()

