"""hash helpers"""
from _hashlib import HASH
from typing import Dict, List

BUF_SIZE = 65536

def chunked_hasher(hash_object: HASH, file_handle) -> str:
    """Calculate the hash of a file without reading it into memory completely"""
    while True:
        data = file_handle.read(BUF_SIZE)
        if not data:
            break
        hash_object.update(data)
    return hash_object.hexdigest()

def chunked_hasher_multiple(hash_objects: List[HASH], file_handle) -> Dict[str, str]:
    """Same as chunked_hasher, but for multiple hashing methods at a tme"""
    while True:
        data = file_handle.read(BUF_SIZE)
        if not data:
            break
        for h_obj in hash_objects:
            h_obj.update(data)
    return {h_obj.name: h_obj.hexdigest() for h_obj in hash_objects}
