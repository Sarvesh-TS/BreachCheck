"""
API module for interacting with HaveIBeenPwned API
"""

import requests
import time
from typing import Dict, List, Optional

class HIBPAPIError(Exception):
    """Custom exception for HIBP API errors"""
    pass

class HIBPAPIClient:
    """Client for interacting with HaveIBeenPwned API"""
    
    BASE_URL = "https://haveibeenpwned.com/api/v3"
    
    def __init__(self, api_key: str):
        """Initialize the API client with API key"""
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update({
            'hibp-api-key': api_key,
            'User-Agent': 'BreachCheck-CLI-Tool'
        })
    
    def get_breaches_for_account(self, email: str, truncate: bool = False) -> List[Dict]:
        """
        Get breaches for a specific email account
        
        Args:
            email: Email address to check
            truncate: Whether to truncate response for faster results
            
        Returns:
            List of breach dictionaries
            
        Raises:
            HIBPAPIError: If API request fails
        """
        endpoint = f"{self.BASE_URL}/breachedaccount/{email}"
        
        params = {}
        if truncate:
            params['truncateResponse'] = 'true'
        
        try:
            # Add a small delay to respect rate limits
            time.sleep(1.6)  # HIBP allows ~1 request per 1.5 seconds
            
            response = self.session.get(endpoint, params=params, timeout=30)
            
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 404:
                # No breaches found - this is normal
                return []
            elif response.status_code == 400:
                raise HIBPAPIError("Bad request - invalid email format")
            elif response.status_code == 401:
                raise HIBPAPIError("Unauthorized - check your API key")
            elif response.status_code == 403:
                raise HIBPAPIError("Forbidden - API key may be invalid or expired")
            elif response.status_code == 429:
                raise HIBPAPIError("Rate limit exceeded - please wait before trying again")
            else:
                raise HIBPAPIError(f"API request failed with status {response.status_code}")
                
        except requests.RequestException as e:
            raise HIBPAPIError(f"Network error: {str(e)}")
    
    def get_all_breaches(self) -> List[Dict]:
        """
        Get all breaches from HIBP (for reference)
        
        Returns:
            List of all breach dictionaries
        """
        endpoint = f"{self.BASE_URL}/breaches"
        
        try:
            response = self.session.get(endpoint, timeout=30)
            
            if response.status_code == 200:
                return response.json()
            else:
                raise HIBPAPIError(f"Failed to fetch all breaches: {response.status_code}")
                
        except requests.RequestException as e:
            raise HIBPAPIError(f"Network error: {str(e)}")
    
    def get_breach_details(self, breach_name: str) -> Dict:
        """
        Get details for a specific breach
        
        Args:
            breach_name: Name of the breach
            
        Returns:
            Breach details dictionary
        """
        endpoint = f"{self.BASE_URL}/breach/{breach_name}"
        
        try:
            response = self.session.get(endpoint, timeout=30)
            
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 404:
                raise HIBPAPIError(f"Breach '{breach_name}' not found")
            else:
                raise HIBPAPIError(f"Failed to fetch breach details: {response.status_code}")
                
        except requests.RequestException as e:
            raise HIBPAPIError(f"Network error: {str(e)}")