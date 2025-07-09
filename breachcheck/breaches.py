"""
Main breach checking logic
"""

import os
from typing import List, Dict, Optional
from datetime import datetime
from .api import HIBPAPIClient, HIBPAPIError
from .utils import load_config

class BreachChecker:
    """Main class for checking email breaches"""
    
    def __init__(self):
        """Initialize the breach checker with API configuration"""
        self.api_key = self._get_api_key()
        self.client = HIBPAPIClient(self.api_key)
    
    def _get_api_key(self) -> str:
        """Get API key from environment or config file"""
        # First try environment variable
        api_key = os.getenv('HIBP_API_KEY')
        
        if api_key:
            return api_key
        
        # Try loading from config file
        config = load_config()
        if config and 'HIBP' in config and 'API_KEY' in config['HIBP']:
            api_key = config['HIBP']['API_KEY']
            if api_key and api_key != 'your_api_key_here':
                return api_key
        
        raise ValueError(
            "No API key found. Please set HIBP_API_KEY environment variable "
            "or add API_KEY to config/config.ini file.\n"
            "Get your API key from: https://haveibeenpwned.com/API/Key"
        )
    
    def check_email(self, email: str, truncate: bool = False) -> List[Dict]:
        """
        Check if an email has been in any breaches
        
        Args:
            email: Email address to check
            truncate: Whether to get truncated response
            
        Returns:
            List of breach information dictionaries
        """
        try:
            raw_breaches = self.client.get_breaches_for_account(email, truncate)
            
            if not raw_breaches:
                return []
            
            # Process and format breach data
            processed_breaches = []
            for breach in raw_breaches:
                processed_breach = self._process_breach_data(breach)
                processed_breaches.append(processed_breach)
            
            # Sort by breach date (newest first)
            processed_breaches.sort(key=lambda x: x['date'], reverse=True)
            
            return processed_breaches
            
        except HIBPAPIError as e:
            raise Exception(f"API Error: {str(e)}")
    
    def _process_breach_data(self, breach: Dict) -> Dict:
        """
        Process raw breach data into a clean format
        
        Args:
            breach: Raw breach data from API
            
        Returns:
            Processed breach data
        """
        # Parse breach date
        breach_date = breach.get('BreachDate', '')
        if breach_date:
            try:
                date_obj = datetime.strptime(breach_date, '%Y-%m-%d')
                formatted_date = date_obj.strftime('%Y-%m-%d')
            except ValueError:
                formatted_date = breach_date
        else:
            formatted_date = 'Unknown'
        
        # Process data classes (what was compromised)
        data_classes = breach.get('DataClasses', [])
        if isinstance(data_classes, list):
            data_compromised = ', '.join(data_classes)
        else:
            data_compromised = str(data_classes)
        
        # Get domain
        domain = breach.get('Domain', 'Unknown')
        
        # Get breach name
        name = breach.get('Name', 'Unknown')
        
        # Get description
        description = breach.get('Description', '')
        
        # Get affected count
        pwn_count = breach.get('PwnCount', 0)
        
        # Check if verified
        is_verified = breach.get('IsVerified', False)
        
        # Check if sensitive
        is_sensitive = breach.get('IsSensitive', False)
        
        # Check if retired
        is_retired = breach.get('IsRetired', False)
        
        return {
            'name': name,
            'domain': domain,
            'date': formatted_date,
            'data_compromised': data_compromised,
            'description': description,
            'pwn_count': pwn_count,
            'is_verified': is_verified,
            'is_sensitive': is_sensitive,
            'is_retired': is_retired
        }
    
    def get_breach_summary(self, email: str) -> Dict:
        """
        Get a summary of breaches for an email
        
        Args:
            email: Email address to check
            
        Returns:
            Summary dictionary with counts and statistics
        """
        breaches = self.check_email(email)
        
        if not breaches:
            return {
                'total_breaches': 0,
                'verified_breaches': 0,
                'sensitive_breaches': 0,
                'latest_breach': None,
                'oldest_breach': None
            }
        
        verified_count = sum(1 for b in breaches if b['is_verified'])
        sensitive_count = sum(1 for b in breaches if b['is_sensitive'])
        
        # Sort by date for latest/oldest
        sorted_breaches = sorted(breaches, key=lambda x: x['date'])
        
        return {
            'total_breaches': len(breaches),
            'verified_breaches': verified_count,
            'sensitive_breaches': sensitive_count,
            'latest_breach': sorted_breaches[-1] if sorted_breaches else None,
            'oldest_breach': sorted_breaches[0] if sorted_breaches else None
        }