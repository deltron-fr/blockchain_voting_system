from datetime import datetime, timezone
from keys import verify_signature

# Validates election creation data
def validate_election(data):
    if not data["election_data"]["user_keys"]:
        raise Exception("There are no voters")
    
    if not data["election_data"]["candidates"]:
         raise Exception("There are no candidates")
    
    if data["election_data"]["start_time"] > data["election_data"]["end_time"]:
        raise Exception("Invalid Timeline")
    
    return True

# Retrieves the election block corresponding to the vote data
def get_election_block(data, blockchain):
    for block in blockchain.blocks:
        if block.type == "create" and data["vote"]["election_id"] == block.data["election_data"]["election_id"]:
                return block
        
    raise Exception("The election does not exist")

# Validates vote data
def validate_votes(data, blockchain):
    election_block = get_election_block(data, blockchain)
    
    if data["public_key"] not in election_block.data["election_data"]["user_keys"]:
        raise Exception("You are not permitted to participate in this election")
                
    current_time = datetime.now(timezone.utc)
    start_time = election_block.data["election_data"]["start_time"]
    end_time = election_block.data["election_data"]["end_time"]

    if current_time < start_time or current_time > end_time:
        raise Exception("Voting is not within the election timeframe")
            
    for block in blockchain.blocks:
        if block.type == "vote":
            if data["public_key"] == block.data["public_key"] and data["vote"]["election_id"] == block.data["vote"]["election_id"]:
                raise Exception("This user has already voted")

    return True

# Verifies the signature of a block
def verify_sig(block, pk):
    if block.type == "create":
        payload = block.data["election_data"]
        signature = block.data["signature"]

        if verify_signature(payload, pk, signature) != True:
            return False
        
        return True
    else:
        payload = block.data["vote"]
        signature = block.data["signature"]

        if verify_signature(payload, pk, signature) != True:
            return False
        
        return True