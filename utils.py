import json
from copy import deepcopy


def serialize_payload(payload):

    payload_copy = deepcopy(payload)

    if "start_time" in payload_copy:
        payload_copy["start_time"] = str(payload_copy["start_time"])
        payload_copy["end_time"] = str(payload_copy["end_time"])

    serialized_payload = json.dumps(payload_copy, sort_keys=True)

    return serialized_payload.encode("utf-8")


def load_candidates(file_path):
    candidates = {}

    with open(file_path, "r") as f:
        for idx, name in enumerate(f):
            candidates[idx + 1] = name.strip()

    return candidates

def load_keys(file_path):
    keys = []
    with open(file_path, "r") as f:
        for key in f:
            keys.append(key.strip())

    return keys

def tally_votes(blockchain, election_id):
    tally = {}

    for block in blockchain.blocks:
        if block.type == "vote" and block.data["vote"]["election_id"] == election_id:
            candidate_id = block.data["vote"]["candidate_id"]
            if candidate_id in tally:
                tally[candidate_id] += 1
            else:
                tally[candidate_id] = 1
    
    return tally

def display_results(blockchain, election_id):
    for block in blockchain.blocks:
        if block.type == "create" and block.data["election_data"]["election_id"] == election_id:
            election_block = block

            candidates = election_block.data["election_data"]["candidates"]
            break
    
    tally = tally_votes(blockchain, election_id)

    results_dict = {}

    for k, v in candidates.items():
        if k in tally:
            results_dict[v] = tally[k]

    winner = {}
    max_no = float("-inf")
    for name, count in results_dict.items():
        if count >= max_no:
            winner[name] = count
            max_no = count

    return results_dict, winner

    
    
