
import re

def is_valid_email(email: str) -> bool:
    """Validate email format."""
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(pattern, email) is not None

def is_valid_domain(domain: str) -> bool:
    """Validate domain format."""
    pattern = r"^(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$"
    return re.match(pattern, domain) is not None

def is_valid_username(username: str) -> bool:
    """Basic username validation (alphanumeric and some special chars)."""
    if not username:
        return False
    pattern = r"^[a-zA-Z0-9_-]+$"
    return re.match(pattern, username) is not None
