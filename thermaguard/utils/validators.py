"""
Validation utilities.

Common validation functions for API inputs and data.
"""

from datetime import datetime, timedelta
import re
from thermaguard.logger import logger


def validate_chamber_id(chamber_id: str) -> bool:
    """
    Validate chamber ID format.
    
    Args:
        chamber_id: Chamber identifier to validate
        
    Returns:
        True if valid, False otherwise
    """
    if not chamber_id:
        return False
    
    # Allow alphanumeric with underscores and hyphens
    pattern = r'^[a-zA-Z0-9_-]+$'
    return bool(re.match(pattern, chamber_id))


def validate_timestamp(timestamp: datetime) -> bool:
    """
    Validate timestamp is reasonable.
    
    Args:
        timestamp: Timestamp to validate
        
    Returns:
        True if valid, False otherwise
    """
    now = datetime.utcnow()
    
    # Timestamp should not be in the future
    if timestamp > now + timedelta(minutes=5):
        logger.warning(f"Timestamp in the future: {timestamp}")
        return False
    
    # Timestamp should not be too old (more than 1 year)
    if timestamp < now - timedelta(days=365):
        logger.warning(f"Timestamp too old: {timestamp}")
        return False
    
    return True
