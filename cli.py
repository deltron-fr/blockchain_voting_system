import click
from block import Block, ActionType
from blockchain import Blockchain
from users import get_user_key_data
from keys import generate_signature
from utils import load_candidates, load_keys
from datetime import datetime

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

if __name__ == "__main__":
    bc = Blockchain()
    cli()



