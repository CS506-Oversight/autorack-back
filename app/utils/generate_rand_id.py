import random
import string


def generate_rand_id(prefix: str) -> str:
    return prefix + ''.join([random.choice(string.ascii_letters + string.digits) for n in range(32)])


def generate_rand_purchase_id() -> str:
    return ''.join([random.choice(string.digits) for n in range(10)])
