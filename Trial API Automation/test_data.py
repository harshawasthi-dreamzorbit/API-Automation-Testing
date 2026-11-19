import hashlib
import uuid
from config import (
    BUSINESS_NAME,
    OWNER_NAME,
    MOBILE,
    APP_VERSION
)


def fingerprint(name):
    """
    Generate SHA-256 fingerprint from machine identifier.
    """
    return hashlib.sha256(name.encode()).hexdigest()


def unique_email(prefix="trial"):
    """
    Generate unique email for test execution.
    """
    unique_id = uuid.uuid4().hex[:12]

    return f"{prefix}_{unique_id}@example.in"


def create_payload(
    machine_id,
    email=None,
    mobile=MOBILE
):
    """
    Generate request payload for Trial Start API.
    """

    if email is None:
        email = unique_email()

    return {
        "fingerprint": fingerprint(machine_id),
        "email": email,
        "business_name": BUSINESS_NAME,
        "owner_name": OWNER_NAME,
        "mobile": mobile,
        "app_version": APP_VERSION,
        "machine_info": {}
    }