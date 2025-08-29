from block import Block, ActionType
from blockchain import Blockchain
from users import get_user_key_data
from keys import generate_signature
from utils import display_results

def main():
    bc = Blockchain()

    first = Block(ActionType.VOTE.value)
    second = Block(ActionType.VOTE.value)
    third = Block(ActionType.VOTE.value)
    fourth = Block(ActionType.VOTE.value)

    first.create_vote(1, 1, "null", get_user_key_data("keys/example_pub.pem"))
    second.create_vote(1, 1, "null", get_user_key_data("keys/example_pub1.pem"))
    third.create_vote(1, 1, "null", get_user_key_data("keys/exam4_pub.pem"))
    fourth.create_vote(1, 3, "null", get_user_key_data("keys/exam5_pub.pem"))

    first.data["signature"] = generate_signature(first.data["vote"], "keys/example.pem")
    second.data["signature"] = generate_signature(second.data["vote"], "keys/example1.pem")
    third.data["signature"] = generate_signature(third.data["vote"], "keys/exam4.pem")
    fourth.data["signature"] = generate_signature(fourth.data["vote"], "keys/exam5.pem")


    bc.add_block(first)
    bc.add_block(second)
    bc.add_block(third)
    bc.add_block(fourth)

    results = display_results(bc, 1)
    print(f"Election Count:\n")
    for name, count in results.items():
        print(f"{name}: {count}")
    print("\n")

if __name__ == "__main__":
    main()
    





