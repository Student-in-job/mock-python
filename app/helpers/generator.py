import random
import string


class Generator:
    @staticmethod
    def generate_string(length: int) -> str:
        max_length = length
        random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=max_length))
        return random_string

    @staticmethod
    def generate_int(length: int) -> str:
        max_length = length
        random_string = ''.join(random.choices(string.digits, k=max_length))
        return random_string
