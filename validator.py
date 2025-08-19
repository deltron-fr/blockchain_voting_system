from datetime import datetime

def validate_election(data):
    if not data["user_keys"]:
        raise Exception("There are no voters")
    
    if not data["candidates"]:
         raise Exception("There are no candidates")
    
    if data["start_time"] > data["end_time"]:
        raise Exception("Invalid Timeline")
    
    
    return True
    
def get_election_block(data, blockchain):
    for block in blockchain.blocks:
        if block.type == "create" and data["election_id"] == block.data["election_id"]:
                return block
        
    raise Exception("The election does not exist")

def validate_votes(data, blockchain):
    
    election_block = get_election_block(data, blockchain)
    
    if data["public_key"] not in election_block.data["user_keys"]:
        raise Exception("You are not permitted to participate in this election")
                
    current_time = datetime.now()
    start_time = election_block.data["start_time"]
    end_time = election_block.data["end_time"]

    if current_time < start_time or current_time > end_time:
        raise Exception("Voting is not within the election timeframe")
            
    for block in blockchain.blocks:
        if data["public_key"] == block.data["public_key"] and data["election_id"] == election_block.data["election_id"]:
            raise Exception("This user has already voted")

    return True


    