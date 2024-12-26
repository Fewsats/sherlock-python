from fastmcp import FastMCP
from sherlock.core import Sherlock
import os

# Create FastMCP and Sherlock instances
mcp = FastMCP("Sherlock Domains MCP Server")
s = Sherlock()

@mcp.tool()
async def me() -> str:
    """Get authenticated user information"""
    return str(s.me())

@mcp.tool()
async def search(query: str) -> str:
    """Search for domains with a query. Returns prices in USD cents."""
    return str(s.search(query))

@mcp.tool()
async def request_purchase(domain: str, search_id: str, cfn: str = '', cln: str = '', cem: str = '', cadd: str = '', cct: str = '', cst: str = '', cpc: str = '', ccn: str = '') -> str:
    """Request a purchase of a domain. Requires contact information."""
    return str(s.request_purchase(domain, search_id, cfn, cln, cem, cadd, cct, cst, cpc, ccn))

@mcp.tool()
async def set_contact(cfn: str = '', cln: str = '', cem: str = '', cadd: str = '', cct: str = '', cst: str = '', cpc: str = '', ccn: str = '') -> str:
    """Set contact information for the authenticated user"""
    return str(s.set_contact(cfn, cln, cem, cadd, cct, cst, cpc, ccn))

@mcp.tool()
async def process_payment(payment_request_url: str, offer_id: str, payment_context_token: str) -> str:
    """Process a payment for an offer"""
    payment_method = 'credit_card'
    return str(s.process_payment(payment_request_url, offer_id, payment_method, payment_context_token))

@mcp.tool()
async def domains() -> str:
    """List of domains owned by the authenticated user"""
    return str(s.domains())

@mcp.tool()
async def dns_records(domain_id: str) -> str:
    """Get DNS records for a domain"""
    return str(s.dns_records(domain_id))

@mcp.tool()
async def create_dns(domain_id: str, type: str = "TXT", name: str = "test", value: str = "test-1", ttl: int = 3600) -> str:
    """Create a new DNS record"""
    return str(s.create_dns(domain_id, type, name, value, ttl))

@mcp.tool()
async def update_dns(domain_id: str, record_id: str, type: str = "TXT", name: str = "test-2", value: str = "test-2", ttl: int = 3600) -> str:
    """Update a DNS record"""
    return str(s.update_dns(domain_id, record_id, type, name, value, ttl))

@mcp.tool()
async def delete_dns(domain_id: str, record_id: str) -> str:
    """Delete a DNS record"""
    return str(s.delete_dns(domain_id, record_id))

if __name__ == "__main__":
    mcp.run()
