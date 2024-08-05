import random
from datetime import datetime, timezone

def generate_otp():
    return '{:06d}'.format(random.randint(0, 999999)), datetime.now(timezone.utc).isoformat()