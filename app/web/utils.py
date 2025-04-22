import re
from fastapi import HTTPException, status


# Basic email verification function
async def verify_email(email: str) -> bool:
    email_regex = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")

    # Basic regex check
    return bool(email_regex.match(email))


async def strip_phone_number(phone: str) -> str:
    only_digits = re.sub(r"\D", "", phone)
    return only_digits


async def raise_bad_request(model_type: str, value: any):
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=f"Invalid {model_type}: {value}"
    )
