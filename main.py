#!/usr/bin/env python3
"""
BreachCheck - CLI Tool for Data Breach Lookup
Entry point for the application
"""

import argparse
import sys
import os
from breachcheck.breaches import BreachChecker
from breachcheck.display import display_results, display_error
from breachcheck.utils import validate_email

def main():
    """Main entry point for the CLI application"""
    parser = argparse.ArgumentParser(
        description="Check if an email address has been compromised in data breaches",
        prog="breachcheck"
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Check command
    check_parser = subparsers.add_parser('check', help='Check email for breaches')
    check_parser.add_argument(
        '--email', 
        required=True, 
        help='Email address to check'
    )
    check_parser.add_argument(
        '--truncate',
        action='store_true',
        help='Truncate response (faster, less detailed)'
    )
    
    # Parse arguments
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    if args.command == 'check':
        email = args.email.strip()
        
        # Validate email format
        if not validate_email(email):
            display_error("Invalid email format")
            sys.exit(1)
        
        # Initialize breach checker
        try:
            checker = BreachChecker()
        except Exception as e:
            display_error(f"Configuration error: {str(e)}")
            sys.exit(1)
        
        # Check for breaches
        try:
            print(f"Checking breaches for: {email}")
            print("Please wait...")
            
            breaches = checker.check_email(email, truncate=args.truncate)
            display_results(email, breaches)
            
        except Exception as e:
            display_error(f"Error checking breaches: {str(e)}")
            sys.exit(1)

if __name__ == "__main__":
    main()