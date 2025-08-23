import json
from copy import deepcopy


def serialize_payload(payload):

    payload_copy = deepcopy(payload)

    if "start_time" in payload_copy:
        payload_copy["start_time"] = str(payload_copy["start_time"])
        payload_copy["end_time"] = str(payload_copy["end_time"])

    serialized_payload = json.dumps(payload_copy, sort_keys=True)

    return serialized_payload.encode("utf-8")