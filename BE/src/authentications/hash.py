import hashlib

from passlib.context import CryptContext

# Configure password hashing context
_pwd_context = CryptContext(schemes=["argon2", "bcrypt"], deprecated="auto")


class HashHelper:
    """
    Helper class for securely hashing and verifying passwords.
    Supports both argon2 and bcrypt.
    """

    @staticmethod
    def hash_password(password: str) -> str:
        """
        Hash a plain text password using the configured scheme.
        For bcrypt, applies SHA-256 if password is too long.
        """
        # Get the default scheme (first in the list)
        scheme = _pwd_context.schemes()[0]
        if scheme == "bcrypt" and len(password.encode("utf-8")) > 72:
            password = hashlib.sha256(password.encode()).hexdigest()
        return _pwd_context.hash(password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """
        Verify a plain text password against a hashed password.
        For bcrypt, applies SHA-256 if password is too long.
        """
        # Detect bcrypt hash by prefix
        if hashed_password.startswith(("$2b$", "$2a$", "$2y$")):
            if len(plain_password.encode("utf-8")) > 72:
                plain_password = hashlib.sha256(plain_password.encode()).hexdigest()
        return _pwd_context.verify(plain_password, hashed_password)
