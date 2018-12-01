import random
import string


def random_string(size=6, chars=string.ascii_uppercase.replace('0', '') + string.digits.replace('0', '')):
    return ''.join(random.choice(chars) for _ in range(size))