"""
Display module for formatting and printing results
"""

from typing import List, Dict
from tabulate import tabulate
import sys

def display_results(email: str, breaches: List[Dict]):
    """
    Display breach results in a formatted table
    
    Args:
        email: Email address that was checked
        breaches: List of breach dictionaries
    """
    if not breaches:
        print(f"\n✅ Good news! No breaches found for: {email}")
        print("This email address does not appear in any known data breaches.")
        return
    
    # Create summary
    total_breaches = len(breaches)
    verified_breaches = sum(1 for b in breaches if b['is_verified'])
    sensitive_breaches = sum(1 for b in breaches if b['is_sensitive'])
    
    print(f"\n⚠️  BREACHES FOUND for: {email}")
    print(f"Total breaches: {total_breaches}")
    print(f"Verified breaches: {verified_breaches}")
    
    if sensitive_breaches > 0:
        print(f"⚠️  Sensitive breaches: {sensitive_breaches}")
    
    print("\nDetailed Results:")
    print("=" * 80)
    
    # Prepare data for table
    table_data = []
    
    for breach in breaches:
        # Truncate long descriptions
        description = breach.get('description', '')
        if len(description) > 60:
            description = description[:57] + "..."
        
        # Add status indicators
        status = ""
        if breach.get('is_verified'):
            status += "✓ "
        if breach.get('is_sensitive'):
            status += "🔒 "
        if breach.get('is_retired'):
            status += "🗄️ "
        
        # Format affected count
        pwn_count = breach.get('pwn_count', 0)
        if pwn_count > 0:
            affected = f"{pwn_count:,}"
        else:
            affected = "Unknown"
        
        table_data.append([
            breach['name'],
            breach['domain'],
            breach['date'],
            breach['data_compromised'][:40] + "..." if len(breach['data_compromised']) > 40 else breach['data_compromised'],
            affected,
            status.strip()
        ])
    
    # Display table
    headers = ['Breach Name', 'Domain', 'Date', 'Data Compromised', 'Affected', 'Status']
    
    print(tabulate(
        table_data,
        headers=headers,
        tablefmt='grid',
        stralign='left'
    ))
    
    # Add legend
    print("\nStatus Legend:")
    print("✓ = Verified breach")
    print("🔒 = Sensitive breach")
    print("🗄️ = Retired/historical breach")
    
    # Security recommendations
    print("\n🔒 Security Recommendations:")
    print("• Change passwords for all affected accounts immediately")
    print("• Enable two-factor authentication (2FA) where possible")
    print("• Monitor your accounts for suspicious activity")
    print("• Consider using a password manager with unique passwords")
    print("• Check your credit reports if financial data was compromised")

def display_error(message: str):
    """
    Display an error message
    
    Args:
        message: Error message to display
    """
    print(f"\n❌ Error: {message}", file=sys.stderr)

def display_breach_details(breach: Dict):
    """
    Display detailed information about a single breach
    
    Args:
        breach: Breach dictionary with detailed information
    """
    print(f"\n📋 Breach Details: {breach['name']}")
    print("=" * 50)
    
    details = [
        ("Name", breach['name']),
        ("Domain", breach['domain']),
        ("Breach Date", breach['date']),
        ("Affected Accounts", f"{breach.get('pwn_count', 'Unknown'):,}" if breach.get('pwn_count') else "Unknown"),
        ("Data Compromised", breach['data_compromised']),
        ("Verified", "Yes" if breach.get('is_verified') else "No"),
        ("Sensitive", "Yes" if breach.get('is_sensitive') else "No"),
        ("Retired", "Yes" if breach.get('is_retired') else "No")
    ]
    
    for label, value in details:
        print(f"{label:.<20} {value}")
    
    if breach.get('description'):
        print(f"\nDescription:")
        print(breach['description'])

def display_loading():
    """Display a loading message"""
    print("🔍 Checking for breaches...")

def display_summary(email: str, summary: Dict):
    """
    Display a summary of breach information
    
    Args:
        email: Email address
        summary: Summary dictionary
    """
    print(f"\n📊 Breach Summary for: {email}")
    print("=" * 50)
    
    if summary['total_breaches'] == 0:
        print("✅ No breaches found")
        return
    
    print(f"Total breaches: {summary['total_breaches']}")
    print(f"Verified breaches: {summary['verified_breaches']}")
    print(f"Sensitive breaches: {summary['sensitive_breaches']}")
    
    if summary['latest_breach']:
        print(f"Latest breach: {summary['latest_breach']['name']} ({summary['latest_breach']['date']})")
    
    if summary['oldest_breach']:
        print(f"Oldest breach: {summary['oldest_breach']['name']} ({summary['oldest_breach']['date']})")

def print_banner():
    """Print application banner"""
    banner = """
    ██████╗ ██████╗ ███████╗ █████╗  ██████╗██╗  ██╗     ██████╗██╗  ██╗███████╗ ██████╗██╗  ██╗
    ██╔══██╗██╔══██╗██╔════╝██╔══██╗██╔════╝██║  ██║    ██╔════╝██║  ██║██╔════╝██╔════╝██║ ██╔╝
    ██████╔╝██████╔╝█████╗  ███████║██║     ███████║    ██║     ███████║█████╗  ██║     █████╔╝ 
    ██╔══██╗██╔══██╗██╔══╝  ██╔══██║██║     ██╔══██║    ██║     ██╔══██║██╔══╝  ██║     ██╔═██╗ 
    ██████╔╝██║  ██║███████╗██║  ██║╚██████╗██║  ██║    ╚██████╗██║  ██║███████╗╚██████╗██║  ██╗
    ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝     ╚═════╝╚═╝  ╚═╝╚══════╝ ╚═════╝╚═╝  ╚═╝
    
    Data Breach Lookup Tool - Powered by HaveIBeenPwned
    """
    print(banner)