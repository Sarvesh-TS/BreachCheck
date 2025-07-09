"""
Utility functions for the BreachCheck application
"""

import re
import os
import configparser
from typing import Optional, Dict

def validate_email(email: str) -> bool:
    """
    Validate email format using regex
    
    Args:
        email: Email address to validate
        
    Returns:
        True if email format is valid, False otherwise
    """
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_pattern, email) is not None

def mask_email(email: str, mask_char: str = '*') -> str:
    """
    Mask part of an email address for privacy
    
    Args:
        email: Email address to mask
        mask_char: Character to use for masking
        
    Returns:
        Masked email address
    """
    if '@' not in email:
        return email
    
    local, domain = email.split('@', 1)
    
    # Mask local part (keep first and last character if possible)
    if len(local) <= 2:
        masked_local = mask_char * len(local)
    else:
        masked_local = local[0] + mask_char * (len(local) - 2) + local[-1]
    
    # Mask domain part (keep first character and domain extension)
    if '.' in domain:
        domain_parts = domain.split('.')
        domain_name = domain_parts[0]
        domain_ext = '.'.join(domain_parts[1:])
        
        if len(domain_name) <= 2:
            masked_domain = mask_char * len(domain_name)
        else:
            masked_domain = domain_name[0] + mask_char * (len(domain_name) - 1)
        
        masked_domain = masked_domain + '.' + domain_ext
    else:
        masked_domain = mask_char * len(domain)
    
    return f"{masked_local}@{masked_domain}"

def load_config(config_path: str = "config/config.ini") -> Optional[configparser.ConfigParser]:
    """
    Load configuration from config file
    
    Args:
        config_path: Path to config file
        
    Returns:
        ConfigParser object or None if file doesn't exist
    """
    if not os.path.exists(config_path):
        return None
    
    config = configparser.ConfigParser()
    try:
        config.read(config_path)
        return config
    except Exception as e:
        print(f"Error reading config file: {e}")
        return None

def save_config(config: configparser.ConfigParser, config_path: str = "config/config.ini"):
    """
    Save configuration to config file
    
    Args:
        config: ConfigParser object
        config_path: Path to config file
    """
    # Create config directory if it doesn't exist
    os.makedirs(os.path.dirname(config_path), exist_ok=True)
    
    try:
        with open(config_path, 'w') as configfile:
            config.write(configfile)
    except Exception as e:
        print(f"Error saving config file: {e}")

def format_number(number: int) -> str:
    """
    Format a number with thousand separators
    
    Args:
        number: Number to format
        
    Returns:
        Formatted number string
    """
    return f"{number:,}"

def truncate_text(text: str, max_length: int, suffix: str = "...") -> str:
    """
    Truncate text to a maximum length
    
    Args:
        text: Text to truncate
        max_length: Maximum length
        suffix: Suffix to add if truncated
        
    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text
    
    return text[:max_length - len(suffix)] + suffix

def sanitize_filename(filename: str) -> str:
    """
    Sanitize a filename by removing invalid characters
    
    Args:
        filename: Filename to sanitize
        
    Returns:
        Sanitized filename
    """
    # Remove invalid characters for file names
    invalid_chars = r'[<>:"/\\|?*]'
    sanitized = re.sub(invalid_chars, '_', filename)
    
    # Remove leading/trailing dots and spaces
    sanitized = sanitized.strip('. ')
    
    return sanitized

def get_env_or_default(key: str, default: str = "") -> str:
    """
    Get environment variable or return default value
    
    Args:
        key: Environment variable key
        default: Default value if key not found
        
    Returns:
        Environment variable value or default
    """
    return os.getenv(key, default)

def create_config_template(config_path: str = "config/config.ini"):
    """
    Create a template configuration file
    
    Args:
        config_path: Path where to create the config file
    """
    config = configparser.ConfigParser()
    
    # Add HIBP section
    config.add_section('HIBP')
    config.set('HIBP', 'API_KEY', 'your_api_key_here')
    config.set('HIBP', '; Get your API key from', 'https://haveibeenpwned.com/API/Key')
    
    # Add general settings
    config.add_section('GENERAL')
    config.set('GENERAL', 'DEFAULT_TRUNCATE', 'false')
    config.set('GENERAL', 'OUTPUT_FORMAT', 'table')
    
    # Save the template
    save_config(config, config_path)
    print(f"Configuration template created at: {config_path}")
    print("Please edit the file and add your HIBP API key.")

def check_dependencies():
    """
    Check if all required dependencies are installed
    """
    required_packages = ['requests', 'tabulate', 'python-dotenv']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("Missing required packages:")
        for package in missing_packages:
            print(f"  - {package}")
        print("\nInstall missing packages with:")
        print(f"pip install {' '.join(missing_packages)}")
        return False
    
    return True

def setup_environment():
    """
    Setup the environment for the application
    """
    # Load environment variables from .env file if it exists
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        pass  # python-dotenv not installed, continue without it
    
    # Create config directory if it doesn't exist
    os.makedirs('config', exist_ok=True)
    
    # Create config template if it doesn't exist
    config_path = 'config/config.ini'
    if not os.path.exists(config_path):
        create_config_template(config_path)