"""Sherlock is a python SDK for AI agents to interact with the Sherlock API."""

# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/00_core.ipynb.

# %% auto 0
__all__ = ['API_URL', 'me_endpoint', 'purchase_endpoint', 'Contact', 'Sherlock', 'main']

# %% ../nbs/00_core.ipynb 3
from typing import Dict, Any
import httpx, json, time
from cryptography.hazmat.primitives.asymmetric import ed25519
import fastcore.utils as fc
from fastcore.test import *
from fastcore.script import *
from fastcore.utils import first, last, L, patch
from fastcore.all import asdict
from .crypto import *

# %% ../nbs/00_core.ipynb 4
API_URL = "https://api.sherlockdomains.com"

# %% ../nbs/00_core.ipynb 9
def _handle_response(r):
    "Process response: raise for status and return json if possible. 402 status is expected for payment required."
    if r.status_code != 402: r.raise_for_status()
    try: return r.json()
    except: return r

def _get_challenge(pub_key: str): # public key
    "Get authentication challenge for a public key"
    r = httpx.post(f"{API_URL}/api/v0/auth/challenge", json={"public_key": pub_key})
    return _handle_response(r)['challenge']


# %% ../nbs/00_core.ipynb 13
def _sign_challenge(pk: ed25519.Ed25519PrivateKey, 
                   c: str): # challenge
    "Sign a challenge with a private key"
    return pk.sign(bytes.fromhex(c)).hex()

# %% ../nbs/00_core.ipynb 17
def _submit_challenge(pub: str, # public key
          c: str, # challenge
          sig: str): # signature
    "Submit a challenge and signature to the server to get access and refresh tokens"
    r = httpx.post(f"{API_URL}/api/v0/auth/login", json={
        "public_key": pub,
        "challenge": c,
        "signature": sig
    })
    r = _handle_response(r)
    return r['access'], r['refresh']

# %% ../nbs/00_core.ipynb 21
from .config import *

# %% ../nbs/00_core.ipynb 22
class Contact(fc.BasicRepr):
    "Contact information for a domain purchase"
    first_name: str
    last_name: str
    email: str
    address: str
    city: str
    state: str
    postal_code: str
    country: str

    def __init__(self, first_name, last_name, email, address, city, state, postal_code, country): fc.store_attr()
    def asdict(self): return self.__dict__['__stored_args__']
    def from_dict(d): return Contact(**d) if d else None

class Sherlock:
    "Sherlock client class to interact with the Sherlock API."
    def __init__(self,
                priv : str = '', # private key
                c : Contact = None): # contact info for purchases
        """
        Initialize Sherlock with a private key and contact info. If no key is provided, a new one is generated and stored in the config file.
        
        """
        cfg = get_cfg()

        if priv: self.pk, self.pub = from_pk_hex(priv) # if provided use the private key
        elif cfg.priv: self.pk, self.pub = from_pk_hex(cfg.priv) # if not provided use the private key from the config file
        else: 
            self.pk, self.pub = generate_keys()
            save_cfg({'priv': priv_key_hex(self.pk)})

        ci = Contact.from_dict(get_contact_info())
        self.c = c if c else ci
        if c and not ci: save_contact_info(c.asdict()) # if contact info is provided and not in the config file, save it
        
        # access & refresh token for authenticated requests
        self.atok, self.rtok = self._authenticate()
        
    def _authenticate(self):
        "Authenticate with the server with a public key and private key"
        c = _get_challenge(self.pub)
        sig = _sign_challenge(self.pk, c)
        return _submit_challenge(self.pub, c, sig)
    
    def __str__(self): return f"Sherlock(pubkey={self.pub})"
    __repr__ = __str__

# %% ../nbs/00_core.ipynb 27
me_endpoint = f"{API_URL}/api/v0/auth/me"

# %% ../nbs/00_core.ipynb 28
def _mk_headers(tok): return {"Authorization": f"Bearer {tok}"}

# %% ../nbs/00_core.ipynb 30
@patch
def me(self: Sherlock):
    "Get authenticated user information"
    r = httpx.get(me_endpoint, headers=_mk_headers(self.atok))
    return _handle_response(r)

# %% ../nbs/00_core.ipynb 34
@patch
def search(self: Sherlock,
                  q: str): # query
    "Search for domains with a query. Returns prices in USD cents."
    r = httpx.get(f"{API_URL}/api/v0/domains/search", params={"query": q})
    return _handle_response(r)

# %% ../nbs/00_core.ipynb 37
@patch
def is_valid(self: Contact):
    "Check if the contact information is valid"
    return all(self.__dict__.values())

@patch
def set_contact(self: Sherlock,
                      cfn: str = '', # contact first name
                      cln: str = '', # contact last name
                      cem: str = '', # contact email
                      cadd: str = '', # contact address
                      cct: str = '', # contact city
                      cst: str = '', # contact state
                      cpc: str = '', # contact postal code
                      ccn: str = ''): # contact country
    "Set the contact information for the Sherlock object"
    c = Contact(cfn, cln, cem, cadd, cct, cst, cpc, ccn)
    if not c.is_valid(): raise ValueError("Invalid contact information")
    self.c = c
    save_contact_info(c.asdict())


# %% ../nbs/00_core.ipynb 40
purchase_endpoint = f"{API_URL}/api/v0/domains/purchase"

# %% ../nbs/00_core.ipynb 41
def _purchase_data(domain: str, # domain
                   contact: Contact, # contact
                   sid: str): # search id
    "Make a purchase payload"
    return {"domain": domain, "contact_information": contact.asdict(), "search_id": sid}

# %% ../nbs/00_core.ipynb 44
@patch
def request_purchase(self: Sherlock,
                      domain: str, # domain
                      sid: str, # search id
                      cfn: str = '', # contact first name
                      cln: str = '', # contact last name
                      cem: str = '', # contact email
                      cadd: str = '', # contact address
                      cct: str = '', # contact city
                      cst: str = '', # contact state
                      cpc: str = '', # contact postal code
                      ccn: str = ''): # contact country
    "Request a purchase of a domain. Requires contact information."
    c = Contact(cfn, cln, cem, cadd, cct, cst, cpc, ccn)
    c = c if c.is_valid() else self.c
    if not c or not c.is_valid(): raise ValueError("Contact information is required")

    r = httpx.post(purchase_endpoint, json=_purchase_data(domain, self.c, sid), headers=_mk_headers(self.atok))
    return _handle_response(r)

# %% ../nbs/00_core.ipynb 49
@patch
def process_payment(self: Sherlock,
                    prurl: str, # payment request url
                    oid: str, # offer id
                    pm: str, # payment method
                    pct: str): # payment context token
    "Process a payment for an offer"
    data = {
        "offer_id": oid,
        "payment_method": pm,
        "payment_context_token": pct
    }
    r = httpx.post(prurl, json=data)
    return _handle_response(r)


# %% ../nbs/00_core.ipynb 52
@patch
def domains(self:Sherlock):
    "List of domains owned by the authenticated user"
    r = httpx.get(f"{API_URL}/api/v0/domains/domains", headers=_mk_headers(self.atok))
    return _handle_response(r)

# %% ../nbs/00_core.ipynb 54
@patch
def dns_records(self:Sherlock,
                domain_id: str): # domain id
    "Get DNS records for a domain"
    r = httpx.get(f"{API_URL}/api/v0/domains/{domain_id}/dns/records", 
                 headers=_mk_headers(self.atok))
    return _handle_response(r)

# %% ../nbs/00_core.ipynb 56
@patch
def create_dns(self:Sherlock,
               domain_id: str, # domain id
               type: str = "TXT", # type
               name: str = "test", # name
               value: str = "test-1", # value
               ttl: int = 3600): # ttl
    "Create a new DNS record"
    data = {"records": [{"type":type, "name":name, "value":value, "ttl":ttl}]}
    r = httpx.post(f"{API_URL}/api/v0/domains/{domain_id}/dns/records",
                  headers=_mk_headers(self.atok), json=data)
    return _handle_response(r)

# %% ../nbs/00_core.ipynb 59
@patch
def update_dns(self:Sherlock,
               domain_id: str, # domain id
               record_id: str, # record id
               type: str = "TXT", # type
               name: str = "test-2", # name
               value: str = "test-2", # value
               ttl: int = 3600): # ttl
    "Update a DNS record"
    data = {"records": [{"id":record_id, "type":type, "name":name, 
                        "value":value, "ttl":ttl}]}
    r = httpx.patch(f"{API_URL}/api/v0/domains/{domain_id}/dns/records",
                   headers=_mk_headers(self.atok), json=data)
    return _handle_response(r)

# %% ../nbs/00_core.ipynb 61
@patch
def delete_dns(self:Sherlock,
               domain_id: str, # domain id
               record_id: str): # record id
    "Delete a DNS record"
    r = httpx.delete(f"{API_URL}/api/v0/domains/{domain_id}/dns/records/{record_id}",
                    headers=_mk_headers(self.atok))
    return _handle_response(r)

# %% ../nbs/00_core.ipynb 64
@patch
def as_tools(self:Sherlock):
    "Return the Sherlock class as a list of tools ready for agents to use"
    return L([
        self.me,
        self.set_contact,
        self.search,
        self.request_purchase,
        self.process_payment,
        self.domains,
        self.dns_records,
        self.create_dns,
        self.update_dns,
        self.delete_dns,
    ])

# %% ../nbs/00_core.ipynb 67
from inspect import signature, Parameter
import argparse

# %% ../nbs/00_core.ipynb 69
def main():
    "CLI interface for Sherlock"
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest='cmd')
    s = Sherlock()
    
    for m in s.as_tools():
        p = sub.add_parser(m.__name__, help=m.__doc__)
        for name,param in signature(m).parameters.items():
            if name != 'self': 
                required = param.default == param.empty
                p.add_argument(f'--{name}', required=required)
    
    args = parser.parse_args()
    if args.cmd: print(getattr(s,args.cmd)(**{k:v for k,v in vars(args).items() 
                                             if k!='cmd' and v is not None}))
    else: parser.print_help()