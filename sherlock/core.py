"""Sherlock is a python SDK for AI agents to interact with the Sherlock API."""

# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/00_core.ipynb.

# %% auto 0
__all__ = ['API_URL', 'me_endpoint', 'get_offers_endpoint', 'Sherlock', 'Contact', 'main']

# %% ../nbs/00_core.ipynb 3
import os
from typing import Dict, Any
import httpx, json, time
import fastcore.utils as fc
from fastcore.test import *
from fastcore.script import *
from fastcore.utils import first, last, L, patch
from fastcore.all import asdict
from cryptography.hazmat.primitives.asymmetric import ed25519


from .auth import authenticate, link_account_to_email
from .config import get_cfg, save_cfg
from .crypto import from_pk_hex, generate_keys, priv_key_hex


# %% ../nbs/00_core.ipynb 5
API_URL = os.getenv('SHERLOCK_API_URL', "https://api.sherlockdomains.com")

# %% ../nbs/00_core.ipynb 6
def _handle_response(r):
    "Process response: raise for status and return json if possible. 402 status is expected for payment required."
    if r.status_code != 402: r.raise_for_status()
    try: return r.json()
    except: return r

# %% ../nbs/00_core.ipynb 8
class Sherlock:
    "Sherlock client class to interact with the Sherlock API."
    def __init__(self,
                priv : str = ''): # private key
        """
        Initialize Sherlock with a private key. If no key is provided, a new one is generated and stored in the config file.
        """
        cfg = get_cfg()

        if priv: self.pk, self.pub = from_pk_hex(priv) # if provided use the private key
        elif cfg.priv: self.pk, self.pub = from_pk_hex(cfg.priv) # if not provided use the private key from the config file
        else: 
            self.pk, self.pub = generate_keys()
            save_cfg({'priv': priv_key_hex(self.pk)})

        # access & refresh token for authenticated requests
        self.atok, self.rtok = self._authenticate()
        
    def _authenticate(self):
        "Authenticate with the server"
        return authenticate(self.pk, API_URL)
    
    def __str__(self): return f"Sherlock(pubkey={self.pub})"
    __repr__ = __str__

# %% ../nbs/00_core.ipynb 13
me_endpoint = f"{API_URL}/api/v0/auth/me"

# %% ../nbs/00_core.ipynb 14
def _mk_headers(tok): return {"Authorization": f"Bearer {tok}"}

# %% ../nbs/00_core.ipynb 16
@patch
def me(self: Sherlock):
    "Get authenticated user information"
    r = httpx.get(me_endpoint, headers=_mk_headers(self.atok))
    return _handle_response(r)

# %% ../nbs/00_core.ipynb 17
@patch
def _me(self: Sherlock):
    """
    Makes an authenticated request to verify the current authentication status and retrieve basic user details.
    Returns user information including logged_in status, email, and the public key being used for authentication.
    """
    return self.me()

# %% ../nbs/00_core.ipynb 21
@patch
def claim_account(self: Sherlock, email: str):
    "Claim an account by linking an email address"
    return link_account_to_email(email, self.atok)

# %% ../nbs/00_core.ipynb 22
@patch
def _claim_account(self: Sherlock, email: str):
    """
    Links an email address to an AI agent's account for web interface access and account recovery.
    
    Important notes:
    - Only accounts without an existing email can be linked
    - Each email can only be linked to one account
    - This method is rarely needed since emails are also set during domain registration
    """
    return self.claim_account(email)



# %% ../nbs/00_core.ipynb 25
@patch
def search(self: Sherlock,
                  q: str): # query
    "Search for domains with a query. Returns prices in USD cents."
    r = httpx.get(f"{API_URL}/api/v0/domains/search", params={"query": q})
    return _handle_response(r)

# %% ../nbs/00_core.ipynb 26
@patch
def _search(self: Sherlock,
                  q: str):
    """
    Search for available domains matching the query.
    Returns search results with available/unavailable domains, their prices in USD cents, and a search ID needed for purchase requests.
    The query can be a full domain name with or without the TLD but not subdomains or text.

    Valid queries: 
        - "example"
        - "example.com" 
        - "my-domain"
    
    Invalid queries:
        - "www.example.com"  # no subdomains
        - "this is a search" # no spaces
        - "sub.domain.com"   # no subdomains
    """

    return self.search(q)

# %% ../nbs/00_core.ipynb 29
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


# %% ../nbs/00_core.ipynb 30
@patch
def is_valid(self: Contact):
    "Check if the contact information is valid"
    return all(self.__dict__.values())

@patch
def set_contact_information(self: Sherlock,
                      cfn: str = '', # contact first name
                      cln: str = '', # contact last name
                      cem: str = '', # contact email
                      cadd: str = '', # contact address
                      cct: str = '', # contact city
                      cst: str = '', # contact state
                      cpc: str = '', # contact postal code
                      ccn: str = ''): # contact country
    "Set the contact information for the Sherlock user"
    c = Contact(cfn, cln, cem, cadd, cct, cst, cpc, ccn)
    if not c.is_valid(): raise ValueError("Invalid contact information")

    data = {
        "first_name": cfn,
        "last_name": cln,
        "email": cem,
        "address": cadd,
        "city": cct,
        "state": cst,
        "postal_code": cpc,
        "country": ccn
    }
    r = httpx.post(f"{API_URL}/api/v0/users/contact-information", json=data, headers=_mk_headers(self.atok))
    return _handle_response(r)


@patch
def get_contact_information(self: Sherlock):
    "Get the contact information for the Sherlock user."

    #| hide
    r = httpx.get(f"{API_URL}/api/v0/users/contact-information", headers=_mk_headers(self.atok))
    return _handle_response(r)
   

# %% ../nbs/00_core.ipynb 32
@patch
def _set_contact_information(self: Sherlock,
                      first_name: str = '',
                      last_name: str = '',
                      email: str = '',
                      address: str = '',
                      city: str = '',
                      state: str = '',
                      postal_code: str = '',
                      country: str = ''):
    """
    Set the contact information that will be used for domain purchases and ICANN registration.
    Contact information must be set before attempting any domain purchases.

    All fields are required:
        first_name: First name
        last_name: Last name
        email: Email address
        address: Street address
        city: City
        state: Two-letter state code for US/Canada (e.g., 'CA', 'NY') or province name (e.g., 'Madrid')
        postal_code: Postal code
        country: Two-letter country code ('US', 'ES', 'FR')
    """
    return self.set_contact_information(first_name, last_name, email, address, city, state, postal_code, country)


@patch
def _get_contact_information(self: Sherlock):
    """
    Retrieve the currently configured contact information that will be used for domain purchases and ICANN registration
    """
    return self.get_contact_information()


# %% ../nbs/00_core.ipynb 38
get_offers_endpoint = f"{API_URL}/api/v0/domains/purchase"

# %% ../nbs/00_core.ipynb 39
def _get_offers_payload(domain: str, # domain
                   contact: Contact, # contact
                   sid: str): # search id
    "Make a purchase payload"
    return {"domain": domain, "contact_information": contact.asdict(), "search_id": sid}

# %% ../nbs/00_core.ipynb 42
@patch
def get_purchase_offers(self: Sherlock,
                      sid: str, # search id
                      domain: str, # domain
                      c: Contact): # contact information
    "Request available payment options for a domain."
    if not c or not c.is_valid(): raise ValueError("Contact information is required")
    r = httpx.post(get_offers_endpoint, json=_get_offers_payload(domain, c, sid), headers=_mk_headers(self.atok))
    return _handle_response(r)


@patch
def _get_purchase_offers(self: Sherlock,
                      sid: str, # search id
                      domain: str): # domain
    """Request available payment options for a domain.

    This method retrieves the L402 offers available for purchasing a specified domain. 
    It requires a valid search ID and domain name. This method requires the contact information to be set.

    The response includes:
    - `version`: The version of the L402 protocol being used.
    - `payment_request_url`: A URL to request payment details.
    - `payment_context_token`: A token used to maintain the payment context.
    - `offers`: A list of available offers, each containing:
        - `id`: Unique identifier for the offer.
        - `title`: The domain name being offered.
        - `description`: A brief description of the offer, including the price.
        - `type`: The type of offer, e.g., 'one-time'.
        - `amount`: The cost of the domain in USD cents.
        - `currency`: The currency of the transaction, typically 'USD'.
        - `payment_methods`: Supported payment methods, such as 'credit_card' and 'lightning'.
"""
    contact = Contact(**self.get_contact_information())
    if not contact or not contact.is_valid(): raise ValueError("Contact information is required")
    return self.get_purchase_offers(sid, domain, contact)




# %% ../nbs/00_core.ipynb 47
@patch
def get_payment_details(self: Sherlock,
                    prurl: str, # payment request url
                    oid: str, # offer id
                    pm: str, # payment method
                    pct: str): # payment context token
    "Get payment details for an offer."
    data = {
        "offer_id": oid,
        "payment_method": pm,
        "payment_context_token": pct
    }
    r = httpx.post(prurl, json=data)
    return _handle_response(r)


# %% ../nbs/00_core.ipynb 49
@patch
def request_payment_details(self: Sherlock,
                    sid: str, # search id
                    domain: str, # domain
                    payment_method: str = 'credit_card', # payment method {'credit_card', 'lightning'}
                    contact: Contact = None): # contact information
    "Request payment information for purchasing a domain. Returns the details needed to complete the payment (like a checkout URL)."
    if not contact: contact = Contact(**self.get_contact_information())
    if not contact.is_valid(): raise ValueError("Contact information is required")
    offers = self.get_purchase_offers(sid, domain, contact)
    return self.get_payment_details(offers['payment_request_url'], offers['offers'][0]['id'], payment_method, offers['payment_context_token'])


@patch
def _request_payment_details(self: Sherlock,
                    sid: str, # search id
                    domain: str, # domain
                    payment_method: str = 'credit_card'): # payment method {'credit_card', 'lightning'}
    """
    Purchase a domain. This method won't charge your account, it will return the payment information needed to complete the purchase.
    Contact information must be set before calling this method.

    sid: Search ID from a previous search request
    domain: Domain name to purchase
    payment_method: Payment method to use {'credit_card', 'lightning'}
    """
    contact = Contact(**self.get_contact_information())
    if not contact or not contact.is_valid(): raise ValueError("Contact information is required")
    return self.request_payment_details(sid, domain, payment_method, contact)


# %% ../nbs/00_core.ipynb 51
@patch
def domains(self:Sherlock):
    "List of domains owned by the authenticated user"
    r = httpx.get(f"{API_URL}/api/v0/domains/domains", headers=_mk_headers(self.atok))
    return _handle_response(r)

# %% ../nbs/00_core.ipynb 52
@patch
def _domains(self:Sherlock):
    """
    List domains owned by the authenticated user.
    
    Each domain object contains:
        id (str): Unique domain identifier (domain_id in other methods)
        domain_name (str): The registered domain name
        created_at (str): ISO timestamp of domain creation
        expires_at (str): ISO timestamp of domain expiration
        auto_renew (bool): Whether domain is set to auto-renew
        locked (bool): Domain transfer lock status
        private (bool): WHOIS privacy protection status
        nameservers (list): List of nameserver hostnames
        status (str): Domain status (e.g. 'active')
    """
    return self.domains()


# %% ../nbs/00_core.ipynb 54
@patch
def dns_records(self:Sherlock,
                domain_id: str): # domain id
    "Get DNS records for a domain."
    r = httpx.get(f"{API_URL}/api/v0/domains/{domain_id}/dns/records", 
                 headers=_mk_headers(self.atok))
    return _handle_response(r)

# %% ../nbs/00_core.ipynb 55
@patch
def _dns_records(self:Sherlock,
                domain_id: str):
    """
    Get DNS records for a domain.

    domain_id: Domain UUID (e.g: 'd1234567-89ab-cdef-0123-456789abcdef')
    
    Each DNS record contains:
        id (str): Unique record identifier
        type (str): DNS record type (e.g. 'A', 'CNAME', 'MX', 'TXT')
        name (str): DNS record name
        value (str): DNS record value
        ttl (int): Time to live in seconds
    """
    return self.dns_records(domain_id)

# %% ../nbs/00_core.ipynb 57
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
def _create_dns_record(self:Sherlock,
                domain_id: str, # domain id
                type: str = "TXT", # type
                name: str = "test", # name
                value: str = "test-1", # value
                ttl: int = 3600): # ttl
    """
    Create a new DNS record for a domain.
    
    domain_id: Domain UUID (e.g., 'd1234567-89ab-cdef-0123-456789abcdef')
    type: DNS record type ('A', 'AAAA', 'CNAME', 'MX', 'TXT', etc.)
    name: Subdomain or record name (e.g., 'www' creates www.yourdomain.com)
    value: Record value (e.g., IP address for A records, domain for CNAME)
    ttl: Time To Live in seconds (default: 3600)
    """
    return self.create_dns(domain_id, type, name, value, ttl)


# %% ../nbs/00_core.ipynb 61
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

# %% ../nbs/00_core.ipynb 63
@patch
def _update_dns_record(self:Sherlock,
                domain_id: str, # domain id
                record_id: str, # record id
                type: str = "TXT", # type
                name: str = "test-2", # name
                value: str = "test-2", # value
                ttl: int = 3600): # ttl
    """
    Update an existing DNS record for a domain.

    NOTE: Updating a record will change its record id.
    
    domain_id: Domain UUID (e.g., 'd1234567-89ab-cdef-0123-456789abcdef')
    record_id: DNS record UUID to update
    type: DNS record type ('A', 'AAAA', 'CNAME', 'MX', 'TXT', etc.)
    name: Subdomain or record name (e.g., 'www' for www.yourdomain.com)
    value: New record value (e.g., IP address for A records)
    ttl: Time To Live in seconds (default: 3600)
    """
    return self.update_dns(domain_id, record_id, type, name, value, ttl)


# %% ../nbs/00_core.ipynb 64
@patch
def delete_dns(self:Sherlock,
               domain_id: str, # domain id
               record_id: str): # record id
    "Delete a DNS record"
    r = httpx.delete(f"{API_URL}/api/v0/domains/{domain_id}/dns/records/{record_id}",
                    headers=_mk_headers(self.atok))
    return _handle_response(r)

# %% ../nbs/00_core.ipynb 66
@patch
def _delete_dns_record(self:Sherlock,
                domain_id: str, # domain id
                record_id: str): # record id
    """
    Delete a DNS record for a domain.
    
    domain_id: Domain UUID (e.g., 'd1234567-89ab-cdef-0123-456789abcdef')
    record_id: DNS record ID to delete
    """
    return self.delete_dns(domain_id, record_id)


# %% ../nbs/00_core.ipynb 68
@patch
def as_tools(self:Sherlock):
    "Return the Sherlock class as a list of tools ready for agents to use"
    return L([
        self._me,
        self._set_contact_information,
        self._get_contact_information,
        self._search, 
        self._request_payment_details,
        self._domains,
        self._dns_records,
        self._create_dns_record,
        self._update_dns_record,
        self._delete_dns_record,
    ])

# %% ../nbs/00_core.ipynb 71
from inspect import signature, Parameter
import argparse

# %% ../nbs/00_core.ipynb 72
@patch
def as_cli(self:Sherlock):
    "Return the Sherlock class as a list of tools ready for agents to use"
    return L([
        self.me,
        self.set_contact_information,
        self.get_contact_information,
        self.search,
        self.request_payment_details,
        self.domains,
        self.dns_records,
        self.create_dns,
        self.update_dns,
        self.delete_dns,
    ])

# %% ../nbs/00_core.ipynb 74
def main():
    "CLI interface for Sherlock"
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest='cmd')
    s = Sherlock()
    
    for m in s.as_cli():
        p = sub.add_parser(m.__name__, help=m.__doc__)
        for name,param in signature(m).parameters.items():
            if name != 'self': 
                required = param.default == param.empty
                p.add_argument(f'--{name}', required=required)
    
    args = parser.parse_args()
    if args.cmd: print(getattr(s,args.cmd)(**{k:v for k,v in vars(args).items() 
                                             if k!='cmd' and v is not None}))
    else: parser.print_help()
