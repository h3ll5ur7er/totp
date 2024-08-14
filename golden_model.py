from hashlib import sha1
import calendar
import time
from datetime import datetime, timedelta
import unicodedata
from hmac import compare_digest
import hmac
import base64
DIGEST = sha1
INTERVAL = 30
SECRET = "JBSWY3DPEHPK3PXP"
DIGITS = 6

def strings_equal(s1: str, s2: str) -> bool:
    s1 = unicodedata.normalize("NFKC", s1)
    s2 = unicodedata.normalize("NFKC", s2)
    return compare_digest(s1.encode("utf-8"), s2.encode("utf-8"))

def verify(otp: str, for_time:datetime|None = None, valid_window: int = 0):
    if for_time is None:
        for_time = datetime.now()

    if valid_window:
        for i in range(-valid_window, valid_window + 1):
            if strings_equal(str(otp), str(at(for_time, i))):
                return True
        return False

    return strings_equal(str(otp), str(at(for_time)))

def timecode(for_time: datetime) -> int:
    if for_time.tzinfo:
        return int(calendar.timegm(for_time.utctimetuple()) / INTERVAL)
    else:
        return int(time.mktime(for_time.timetuple()) / INTERVAL)


def byte_secret() -> bytes:
    secret = SECRET
    missing_padding = len(SECRET) % 8
    if missing_padding != 0:
        secret += "=" * (8 - missing_padding)
    return base64.b32decode(secret, casefold=True)

def int_to_bytestring(i: int, padding: int = 8) -> bytes:
    result = bytearray()
    while i != 0:
        result.append(i & 0xFF)
        i >>= 8
    return bytes(bytearray(reversed(result)).rjust(padding, b"\0"))

def generate_otp(input: int) -> str:
    if input < 0:
        raise ValueError("input must be positive integer")
    hasher = hmac.new(byte_secret(), int_to_bytestring(input), DIGEST)
    hmac_hash = bytearray(hasher.digest())
    offset = hmac_hash[-1] & 0xF
    code = (
        (hmac_hash[offset] & 0x7F) << 24
        | (hmac_hash[offset + 1] & 0xFF) << 16
        | (hmac_hash[offset + 2] & 0xFF) << 8
        | (hmac_hash[offset + 3] & 0xFF)
    )
    str_code = str(10_000_000_000 + (code % 10**DIGITS))
    return str_code[-DIGITS :]



def at(for_time: datetime|int, counter_offset: int = 0) -> str:
    if not isinstance(for_time, datetime):
        for_time = datetime.fromtimestamp(for_time)
    counter = for_time + timedelta(seconds=counter_offset)
    return generate_otp(timecode(counter))

def now():
    return generate_otp(timecode(datetime.now()))


def main():
    now_time = datetime.now()
    for i in range(-10, 10):
        otp = at(now_time, i*30)
        print(otp, verify(otp))

if __name__ == "__main__":
    main()