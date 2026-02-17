import string

# The standard Base62 character set: 0-9, a-z, A-Z
BASE62_CHARS = string.digits + string.ascii_lowercase + string.ascii_uppercase


def to_base62(num: int) -> str:
    if num < 0:
        raise ValueError
        
    if num == 0:
        return BASE62_CHARS[0]
    
    result = []
    while num > 0:
        result.append(BASE62_CHARS[num % 62])
        num //= 62
    
    return "".join(reversed(result))


def from_base62(s: str) -> int:
    """Decodes a Base62 string to an integer."""
    char_map = {char: i for i, char in enumerate(BASE62_CHARS)}
    num = 0
    for char in s:
        num = num * 62 + char_map[char]
    return num