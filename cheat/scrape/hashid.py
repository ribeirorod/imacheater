# Return a short aplhanumeric hashid from string input:
import pandas as pd

pd.read_csv()
from hashids import Hashids 

default_args = {
    "alphabet" : "@abcdefghijklmnopqrstuvwxyz1234567890",
    "salt" : "we came, we saw, we conquer"
}

data = {
    'region': (3,'eu', 'germany'), 
    'category': (3,'eletronics'),
    'brand': (5,'offnutrition', 'super brush 2001'),
    'description': ('something about the product')
}

shortid = []
for item in data:

    # check if item has length predefined, if not return 8 by default
    length = data[item][0] if isinstance(data[item][0],int) else 6
    hashids = Hashids(**default_args, min_length=4)
    
    id = hashids.encode(data[item][1:])
    shortid.append(id)

finalid = "".join(shortid)


hashid = hashids.encode(123, 456, 789) # 'dzvuMqiXL'
hashid = hashids.decode('dzvuMqiXL') # 'dzvuMqiXL'


# first we need a numeric reference for the input string
# We have 2 digits keys for each allowed value on our alphaet


alpha = list(default_args['alphabet'])
ids = dict(zip(alpha, list(range(10, len(alpha) + 10 ))))
ids.update({e:99 for e in ';,. /'})
ids_rev = dict((str(v),k) for k,v in ids.items())


string_id = [str(ids[letter.lower()]) for letter in 'EU,Germany,Eletronics']

numeric_id = int("".join(string_id))
encoded_id = hashids.encode(numeric_id)
decoded_id = hashids.decode(hashid)

import re

_string_id = re.findall('..', str(decoded_id[0]))

decoded_str = []
for id in _string_id:
    join_str = ids_rev[id] if id != '99' else ' '
    decoded_str.append(join_str)

decoded = "".join(decoded_str).split(',').capitalize()



import hashlib

enc_table = "@abcdefghijklmnopqrstuvwxyz1234567890"

def shorten_hash(s, s_lenght=8, enc_tbl = enc_table):
    """Generate a Hexadecimal string with the given length
    shorten_hash("hello world",8) -> '309ecc48 """
    return hashlib.sha1(s.encode('utf-8')).hexdigest()[s_lenght]


#Python
import hashlib
import base64
def shorten_hash(s, s_lenght=8):
    """Generate a Base64 encoded string with the given length
    shorten_hash("hello world",8) -> 'YWJjY2Q=' """
    return base64.b64encode(hashlib.sha1(s.encode('utf-8')).digest())[:s_lenght]

hashlib.sha1(short.decode('utf-8')).hexdigest()
#Python
import hashlib
import base64
def shorten_hash(s, s_lenght=8):
    """Generate a Base64 encoded string with the given length
    shorten_hash("hello world",8) -> 'YWJjY2Q=' """
    return base64.urlsafe_b64encode(hashlib.sha1(s.encode('utf-8')).digest())[:s_lenght]


def long_string(encoded_hash):
    """ Return decoded readable string from encoded hash id"""
    return base64.b32decode(encoded_hash).decode('utf-8')
