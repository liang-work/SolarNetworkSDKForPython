"""
Utility functions for Solar Network Python SDK.

This module provides utility functions for string manipulation,
date formatting, and other common operations.
"""

from typing import Optional


def capitalize_each_word(text: str) -> str:
    """Capitalize the first letter of each word in a string.
    
    Args:
        text: The input string
        
    Returns:
        The string with each word capitalized
    """
    if not text:
        return text
    
    return ' '.join(
        word[0].upper() + word[1:].lower() if word else ''
        for word in text.split(' ')
    )


def format_datetime(dt: Optional[str]) -> Optional[str]:
    """Format a datetime string.
    
    Args:
        dt: The datetime string
        
    Returns:
        The formatted datetime string
    """
    if not dt:
        return None
    
    # Simple formatting - in a real implementation, you might use
    # a library like dateutil or datetime for more robust parsing
    return dt


def get_translation_key(template_key: str) -> str:
    """Get a translation key from a template key.
    
    Args:
        template_key: The template key
        
    Returns:
        The translation key
    """
    parts = template_key.split('_')
    camel_case = ''.join(part.capitalize() for part in parts)
    return f'reaction{camel_case}'


def slugify(text: str) -> str:
    """Convert text to a URL-friendly slug.
    
    Args:
        text: The input text
        
    Returns:
        The slugified text
    """
    import re
    
    # Convert to lowercase and replace spaces with hyphens
    text = text.lower().replace(' ', '-')
    
    # Remove any non-alphanumeric characters except hyphens
    text = re.sub(r'[^a-z0-9\-]', '', text)
    
    # Remove multiple consecutive hyphens
    text = re.sub(r'-+', '-', text)
    
    # Remove leading and trailing hyphens
    text = text.strip('-')
    
    return text


def format_file_size(size_bytes: int) -> str:
    """Format file size in human-readable format.
    
    Args:
        size_bytes: The file size in bytes
        
    Returns:
        The formatted file size
    """
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB", "TB"]
    import math
    
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    
    return f"{s} {size_names[i]}"


def is_valid_email(email: str) -> bool:
    """Check if an email address is valid.
    
    Args:
        email: The email address to validate
        
    Returns:
        True if the email is valid, False otherwise
    """
    import re
    
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def truncate_string(text: str, max_length: int, suffix: str = "...") -> str:
    """Truncate a string to a maximum length.
    
    Args:
        text: The input text
        max_length: The maximum length
        suffix: The suffix to add when truncating
        
    Returns:
        The truncated string
    """
    if len(text) <= max_length:
        return text
    
    suffix_length = len(suffix)
    if max_length <= suffix_length:
        return suffix[:max_length]
    
    return text[:max_length - suffix_length] + suffix