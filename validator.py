

def validate_election(data):
    if data["user_keys"] == "":
        raise Exception("There are no voters")
    
    if data["start_time"] > data["end_time"]:
        raise Exception("Invalid Timeline")
    
def validate_election_existence(data, blockchain):
    for block in blockchain.blocks:
        if block.type == "create" and data["election_id"] == block.data["election_id"]:
                return True
        
    raise Exception("The election does not exist")

def validate_votes(data, blockchain):
    if validate_election_existence(data, blockchain):
        for block in blockchain.blocks:
            if block.type == "create" and data["election_id"] == block.data["election_id"]:
                    if data["public_key"] not in block.data["user_keys"]:
                        raise Exception("You are not permitted to participate in this election")


    