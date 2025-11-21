import click
from block import Block, ActionType
from blockchain import Blockchain
from users import get_user_key_data
from keys import generate_signature
from utils import load_candidates, load_keys, display_results
from datetime import datetime
import json

@click.group()
def cli():
    pass

@cli.command()
@click.argument("election_id", type=int)
@click.argument("candidates_file", type=click.Path(exists=True))
@click.argument("user_keys_file", type=click.Path(exists=True))
@click.argument("pk_file", type=click.Path(exists=True))
@click.argument("sk_file", type=click.Path(exists=True))
@click.argument("start_time_str", type=str)
@click.argument("end_time_str", type=str)
def create_election(election_id, candidates_file, user_keys_file, pk_file, sk_file, start_time_str, end_time_str):
    candidates = load_candidates(candidates_file)
    user_keys = load_keys(user_keys_file)

    start_time = datetime.fromisoformat(start_time_str.replace("Z", "+00:00"))
    end_time = datetime.fromisoformat(end_time_str.replace("Z", "+00:00"))

    block = Block(ActionType.CREATE.value)

    user_pk = get_user_key_data(pk_file)

    block.create_election(election_id, candidates, user_keys, user_pk, "null", start_time, end_time)
    block.data["signature"] = generate_signature(block.data["election_data"], sk_file)

    bc.add_block(block)

    click.secho("block added successfully", fg='green')

@cli.command()
@click.argument("election_id", type=int)
@click.argument("c_id", type=int)
@click.argument("pk_file", type=click.Path(exists=True))
@click.argument("sk_file", type=click.Path(exists=True))
def vote(election_id, c_id, pk_file, sk_file):
    block = Block(ActionType.VOTE.value)

    user_pk = get_user_key_data(pk_file)
    
    block.create_vote(election_id, c_id, "null", user_pk)
    block.data["signature"] = generate_signature(block.data["vote"], sk_file)

    bc.add_block(block)

    click.secho("block added successfully", fg='green')

@cli.command()
@click.argument("election_id", type=int)
def results(election_id):
    with open("chain.json", mode="r", encoding="utf-8") as f:
        chain_data = json.load(f)
    chain = [Block.from_dict(block) for block in chain_data]

    total_results, winner = display_results(chain, election_id)
    print("==== Election Results ===")
    for candidate_id, votes in total_results.items():
        print(f"{candidate_id}: {votes} votes")
    
    if len(winner) == 0:
        print("No votes were cast in this election.")
        return
    
    elif len(winner) == 1:
        print("The winner is:")
        name, count = next(iter(winner.items()))
        print(f"{name} with {count} votes")
        return

    print("It's a tie between:")
    for candidate in winner:
        print(f"{candidate} with {total_results[candidate]} votes")

if __name__ == "__main__":
    bc = Blockchain()
    cli()



