from nacl.signing import VerifyKey
from io import StringIO
from .model import get_verify_key_from_db, cache_verify_key
import requests
from .exceptions import MissingValueException
from binascii import unhexlify

def verify_request(json_data):
    customer_tid = json_data.get('tid')
    explorer_url = json_data.get('explorer_url')
    if customer_tid is None or explorer_url is None or "signature" not in json_data:
        raise MissingValueException("tid, signature, and explorer_url must be provided")
    verify_key = get_verify_key(explorer_url, customer_tid)
    validate_signature(json_data, verify_key)
    
def validate_signature(json_data, verify_key_bytes):
    data_bytes = _encode_json(json_data)
    signature = unhexlify(json_data.get('signature').encode())
    verify_key = VerifyKey(verify_key_bytes)
    verify_key.verify(data_bytes, signature)
    
def get_verify_key(explorer_url, customer_tid):
    verify_key = get_verify_key_from_db(customer_tid, explorer_url)
    if verify_key is not None:
        return verify_key
    
    verify_key = get_verify_key_from_explorer(customer_tid, explorer_url)
    cache_verify_key(customer_tid, explorer_url, verify_key)
    return verify_key

def get_verify_key_from_explorer(customer_tid, explorer_url):
    explorer_url = explorer_url.rstrip('/')
    user_url = f'{explorer_url}/users/{customer_tid}'
    pub_key = unhexlify(requests.get(user_url).json()['pubkey'])    
    return pub_key

def _encode_json(json_data):
    keys = ['tid', 'tname', 'timestamp', 'level', 'message', 'explorer_url', "vdc_name", "app_name", "status", "category", "type", "count"]
    b = StringIO()
    for key in keys:
        if key in json_data:
            b.write(key)
            b.write(str(json_data.get(key)))
    return b.getvalue().encode()