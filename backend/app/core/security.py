from __future__ import annotations

import hashlib
import hmac
import secrets
from typing import Tuple


def hash_passcode(passcode: str) -> Tuple[str, str]:
    salt = secrets.token_hex(16)
    digest = hashlib.pbkdf2_hmac(
        "sha256",
        passcode.encode("utf-8"),
        salt.encode("utf-8"),
        120_000,
    )
    return salt, digest.hex()


def verify_passcode(passcode: str, salt: str, hashed: str) -> bool:
    digest = hashlib.pbkdf2_hmac(
        "sha256",
        passcode.encode("utf-8"),
        salt.encode("utf-8"),
        120_000,
    ).hex()
    return hmac.compare_digest(digest, hashed)
