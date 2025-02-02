# Sherlock Domains & Fewsats Python SDK

Sherlock is a Python SDK for managing domain names and DNS records through the Sherlock API.

Fewsats is a Python SDK for managing Lightning Network payments through the Fewsats API.
## Installation

```sh
pip install sherlock-domains fewsats
```
## Examples
1. Domain Search & Purchase:
```python
from sherlock.core import Sherlock
import json


s = Sherlock(os.getenv('SHERLOCK_PRIVATE_KEY'))

r = s._search("example.com")
d = next((x for x in r['available'] if x['name'] == "notahuman.me"), None)

contact_info = json.loads(os.getenv('CONTACT_INFO'))
s._set_contact_information(first_name=contact_info['first_name'], last_name=contact_info['last_name'], email=contact_info['email'], address=contact_info['address'], city=contact_info['city'], state=contact_info['state'], postal_code=contact_info['postal_code'], country=contact_info['country'])

purchase = s._request_payment_details(
    r['id'], 
    d['name'],
    payment_method='lightning'
)
# this will return a lightning invoice information needed by fewsats to pay for the domain
print(purchase)

# pay the invoice using fewsats
from fewsats.core import Client

fs = Client(api_key=os.getenv("FEWSATS_API_KEY"))

fs.pay_lightning(invoice="lnbc....", description="..")

```

2. DNS Management:
```python
s = Sherlock()
domains = s.domains()
domain_id = domains[0]['id']

# Create DNS record
s.create_dns(
    domain_id,
    type="A",
    name="www",
    value="1.2.3.4",
    ttl=3600
)
```
