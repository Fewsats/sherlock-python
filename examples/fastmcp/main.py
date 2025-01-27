
from fastmcp import FastMCP
from sherlock.core import Sherlock
import os

# Create FastMCP and Sherlock instances
mcp = FastMCP("Sherlock Domains MCP Server")
s = Sherlock()


@mcp.tool()
async def _me() -> str:
    """Makes an authenticated request to verify the current authentication status and retrieve basic user details.
Returns user information including logged_in status, email, and the public key being used for authentication."""
    return str(s._me())


@mcp.tool()
async def _set_contact_information(first_name: str, last_name: str, email: str, address: str, city: str, state: str, postal_code: str, country: str) -> str:
    """Set the contact information that will be used for domain purchases and ICANN registration.
Contact information must be set before attempting any domain purchases.

All fields are required:
    first_name: First name
    last_name: Last name
    email: Email address
    address: Street address
    city: City
    state: Two-letter state code for US/Canada (e.g., 'CA', 'NY') or province name (e.g., 'Madrid')
    postal_code: Postal code
    country: Two-letter country code ('US', 'ES', 'FR')"""
    return str(s._set_contact_information(first_name, last_name, email, address, city, state, postal_code, country))


@mcp.tool()
async def _get_contact_information() -> str:
    """Retrieve the currently configured contact information that will be used for domain purchases and ICANN registration"""
    return str(s._get_contact_information())


@mcp.tool()
async def _search(q: str) -> str:
    """Search for available domains matching the query.
Returns search results with available/unavailable domains, their prices in USD cents, and a search ID needed for purchase requests.
The query can be a full domain name with or without the TLD but not subdomains or text.

Valid queries: 
    - "example"
    - "example.com" 
    - "my-domain"

Invalid queries:
    - "www.example.com"  # no subdomains
    - "this is a search" # no spaces
    - "sub.domain.com"   # no subdomains"""
    return str(s._search(q))


@mcp.tool()
async def _purchase_domain(sid: str, domain: str, payment_method: str) -> str:
    """Purchase a domain. This method won't charge your account, it will return the payment information needed to complete the purchase.
Contact information must be set before calling this method.

sid: Search ID from a previous search request
domain: Domain name to purchase
payment_method: Payment method to use {'credit_card', 'lightning'}"""
    return str(s._purchase_domain(sid, domain, payment_method))


@mcp.tool()
async def _domains() -> str:
    """List domains owned by the authenticated user.

Each domain object contains:
    id (str): Unique domain identifier (domain_id in other methods)
    domain_name (str): The registered domain name
    created_at (str): ISO timestamp of domain creation
    expires_at (str): ISO timestamp of domain expiration
    auto_renew (bool): Whether domain is set to auto-renew
    locked (bool): Domain transfer lock status
    private (bool): WHOIS privacy protection status
    nameservers (list): List of nameserver hostnames
    status (str): Domain status (e.g. 'active')"""
    return str(s._domains())


@mcp.tool()
async def _dns_records(domain_id: str) -> str:
    """Get DNS records for a domain.

domain_id: Domain UUID (e.g: 'd1234567-89ab-cdef-0123-456789abcdef')

Each DNS record contains:
    id (str): Unique record identifier
    type (str): DNS record type (e.g. 'A', 'CNAME', 'MX', 'TXT')
    name (str): DNS record name
    value (str): DNS record value
    ttl (int): Time to live in seconds"""
    return str(s._dns_records(domain_id))


@mcp.tool()
async def _create_dns_record(domain_id: str, type: str, name: str, value: str, ttl: int) -> str:
    """Create a new DNS record for a domain.

domain_id: Domain UUID (e.g., 'd1234567-89ab-cdef-0123-456789abcdef')
type: DNS record type ('A', 'AAAA', 'CNAME', 'MX', 'TXT', etc.)
name: Subdomain or record name (e.g., 'www' creates www.yourdomain.com)
value: Record value (e.g., IP address for A records, domain for CNAME)
ttl: Time To Live in seconds (default: 3600)"""
    return str(s._create_dns_record(domain_id, type, name, value, ttl))


@mcp.tool()
async def _update_dns_record(domain_id: str, record_id: str, type: str, name: str, value: str, ttl: int) -> str:
    """Update an existing DNS record for a domain.

NOTE: Updating a record will change its record id.

domain_id: Domain UUID (e.g., 'd1234567-89ab-cdef-0123-456789abcdef')
record_id: DNS record UUID to update
type: DNS record type ('A', 'AAAA', 'CNAME', 'MX', 'TXT', etc.)
name: Subdomain or record name (e.g., 'www' for www.yourdomain.com)
value: New record value (e.g., IP address for A records)
ttl: Time To Live in seconds (default: 3600)"""
    return str(s._update_dns_record(domain_id, record_id, type, name, value, ttl))


@mcp.tool()
async def _delete_dns_record(domain_id: str, record_id: str) -> str:
    """Delete a DNS record for a domain.

domain_id: Domain UUID (e.g., 'd1234567-89ab-cdef-0123-456789abcdef')
record_id: DNS record ID to delete"""
    return str(s._delete_dns_record(domain_id, record_id))


if __name__ == "__main__":
    mcp.run()
