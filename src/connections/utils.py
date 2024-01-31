""" Utils for connections """

import hashlib
import json
import uuid


def generate_uuid_from_dict(data_dict: dict) -> str:
    """Generate a UUID from a dictionary"""
    dict_string = json.dumps(data_dict, sort_keys=True)
    dict_string = dict_string.lower()

    # Create a hash of the string
    hash_object = hashlib.sha1(dict_string.encode())

    # Generate a UUID from the hash
    return str(uuid.UUID(bytes=hash_object.digest()[:16]))
