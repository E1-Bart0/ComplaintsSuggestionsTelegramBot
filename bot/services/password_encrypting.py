from typing import Union

from bcrypt import checkpw, gensalt, hashpw


def generate_hash_for_password(password: str) -> str:
    """Generating hash for password"""
    return hashpw(password.encode(), gensalt()).decode()


def check_password(password: str, h_password: Union[bytes, str]) -> bool:
    """Check if password correct"""
    h_password = h_password if isinstance(h_password, bytes) else h_password.encode()
    return checkpw(password.encode(), h_password)
