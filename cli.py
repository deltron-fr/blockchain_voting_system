import click
from block import Block, ActionType
from blockchain import Blockchain
from users import get_user_key_data
from keys import generate_signature

@click.group()
def cli():
    pass

@cli.command()
def create_election():
    pass

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



