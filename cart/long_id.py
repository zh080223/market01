import random
import time


def generate_order_id():
    timestamp = int(round(time.time() * 1000))
    timestamp_str = str(timestamp).zfill(13)
    random_str = str(random.randint(1, 999))
    order_id = timestamp_str + random_str
    return order_id
