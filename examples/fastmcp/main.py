
from fastmcp import FastMCP
from sherlock.core import Sherlock
import os

# Create FastMCP and Sherlock instances
mcp = FastMCP("Sherlock Domains MCP Server")
s = Sherlock()


@mcp.tool()
async def _me() -> str:
    """Makes an authenticated request to verify the current authentication status.

Returns:
    dict: Authentication status containing:
        - logged_in (bool): Whether the user is authenticated

Raises:
    HTTPError: If the request fails or authentication is invalid"""
    return str(s._me())


@mcp.tool()
async def _set_contact(cfn: str, cln: str, cem: str, cadd: str, cct: str, cst: str, cpc: str, ccn: str) -> str:
    """Set the contact information that will be used for domain purchases and ICANN registration

Args:
    cfn (str): First name
    cln (str): Last name
    cem (str): Email address
    cadd (str): Street address
    cct (str): City
    cst (str): State/Province
    cpc (str): Postal code
    ccn (str): Country code (e.g., 'US')

Raises:
    ValueError: If any required field is empty"""
    return str(s._set_contact(cfn, cln, cem, cadd, cct, cst, cpc, ccn))


@mcp.tool()
async def _get_contact() -> str:
    """Retrieve the currently configured contact information that will be used for domain purchases and ICANN registration

Returns:
    Contact: Contact information object"""
    return str(s._get_contact())


@mcp.tool()
async def _search(q: str) -> str:
    """Search for available domains matching the query.

Args:
    q (str): Query string to search for domains (can be a full domain name or partial text)

Returns:
    dict: Search results containing:
        - id (str): Unique search ID used for subsequent purchase requests
        - created_at (str): ISO timestamp of when the search was performed
        - available (list): List of available domains, each containing:
            - name (str): Full domain name
            - tld (str): Top-level domain
            - tags (list): Domain categories or features
            - price (int): Price in USD cents
            - currency (str): Currency code (e.g., 'USD')
            - available (bool): Domain availability status
        - unavailable (list): List of unavailable domain names

Raises:
    HTTPError: If the search request fails
    ValueError: If query contains invalid characters"""
    return str(s._search(q))


@mcp.tool()
async def purchase_domain(sid: str, domain: str, payment_method: str) -> str:
    """Purchase a domain. This method won't charge your account, it will return the payment information for purchasing a domain.
For credit card payments it returns a checkout URL. For Lightning Network payments it returns an invoice.

NOTE: Before calling this method the contact information needs to be set for the Sherlock object.

Args:
    sid (str): Search ID from previous search request
    domain (str): Domain name to purchase
    payment_method (str): Payment method {'credit_card', 'lightning'}

Returns:
    dict:
        - payment_method (dict): 
            - checkout_url (str): URL for credit card payment processing
            - lightning_invoice (str): Lightning Network invoice
        - expires_at (str): ISO timestamp of when the payment expires"""
    return str(s.purchase_domain(sid, domain, payment_method))


@mcp.tool()
async def _domains() -> str:
    """List domains owned by the authenticated user.

Returns:
    list: List of domain objects containing:
        - id (str): Unique domain identifier (domain_id in other methods)
        - domain_name (str): The registered domain name
        - created_at (str): ISO timestamp of domain creation
        - expires_at (str): ISO timestamp of domain expiration
        - auto_renew (bool): Whether domain is set to auto-renew
        - locked (bool): Domain transfer lock status
        - private (bool): WHOIS privacy protection status
        - nameservers (list): List of nameserver hostnames
        - status (str): Domain status (e.g. 'active')

Raises:
    HTTPError: If the request fails or authentication is invalid"""
    return str(s._domains())


@mcp.tool()
async def _dns_records(domain_id: str) -> str:
    """Get DNS records for a domain.

Args
    domain_id: str - domain uuid (e.g: 'd1234567-89ab-cdef-0123-456789abcdef')

Returns:
    str: Domain name
    list: List of DNS records with:
        - id (str): Unique record identifier
        - type (str): DNS record type (e.g. 'A', 'CNAME', 'MX', 'TXT')
        - name (str): DNS record name
        - value (str): DNS record value
        - ttl (int): Time to live in seconds"""
    return str(s._dns_records(domain_id))


@mcp.tool()
async def _create_dns_record(domain_id: str, type: str, name: str, value: str, ttl: int) -> str:
    """Create a new DNS record for a domain.

Args:
    domain_id (str): Domain UUID (e.g., 'd1234567-89ab-cdef-0123-456789abcdef')
    type (str): DNS record type ('A', 'AAAA', 'CNAME', 'MX', 'TXT', etc.)
    name (str): Subdomain or record name (e.g., 'www' creates www.yourdomain.com)
    value (str): Record value (e.g., IP address for A records, domain for CNAME)
    ttl (int): Time To Live in seconds (default: 3600)

Returns:
    dict: Created DNS record containing:
        - records (list): List with the created record containing:
            - id (str): Unique record identifier
            - type (str): DNS record type
            - name (str): Record name
            - value (str): Record value
            - ttl (int): Time to live in seconds

Raises:
    HTTPError: If the request fails or authentication is invalid"""
    return str(s._create_dns_record(domain_id, type, name, value, ttl))


@mcp.tool()
async def _update_dns_record(domain_id: str, record_id: str, type: str, name: str, value: str, ttl: int) -> str:
    """Update an existing DNS record for a domain.

NOTE: Updating a record will change its record id.

Args:
    domain_id (str): Domain UUID (e.g., 'd1234567-89ab-cdef-0123-456789abcdef')
    record_id (str): DNS record UUID to update
    type (str): DNS record type ('A', 'AAAA', 'CNAME', 'MX', 'TXT', etc.)
    name (str): Subdomain or record name (e.g., 'www' for www.yourdomain.com)
    value (str): New record value (e.g., IP address for A records)
    ttl (int): Time To Live in seconds (default: 3600)

Returns:
    dict: Updated DNS record containing:
        - records (list): List with the modified record containing:
            - id (str): Record identifier
            - type (str): DNS record type
            - name (str): Record name
            - value (str): Updated value
            - ttl (int): Time to live in seconds

Raises:
    HTTPError: If the request fails, record doesn't exist, or authentication is invalid"""
    return str(s._update_dns_record(domain_id, record_id, type, name, value, ttl))


@mcp.tool()
async def _delete_dns_record(domain_id: str, record_id: str) -> str:
    """Delete a DNS record for a domain.

Args:
    domain_id (str): Domain UUID (e.g., 'd1234567-89ab-cdef-0123-456789abcdef')
    record_id (str): DNS record ID to delete

Returns:
    dict: Empty response"""
    return str(s._delete_dns_record(domain_id, record_id))


if __name__ == "__main__":
    mcp.run()
