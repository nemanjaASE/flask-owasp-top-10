import hashlib
import requests

class PwnedService:
    def is_password_compromised(self, password):
        hashed_password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
        prefix, suffix = hashed_password[:5], hashed_password[5:]

        response = requests.get(f'https://api.pwnedpasswords.com/range/{prefix}')
        if response.status_code == 200:
            hashes = (line.split(':') for line in response.text.splitlines())
            for h, count in hashes:
                if suffix == h:
                    return True
        return False