from datetime import datetime, timedelta

from redis import Redis


def save_if_new(rdbc: Redis, question_id: int) -> bool:
    datetime.now()
    if rdbc.get(str(question_id)):
        return True
    rdbc.set(str(question_id), str(question_id), timedelta(hours=1))
    return False
