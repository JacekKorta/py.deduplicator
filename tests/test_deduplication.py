import pytest
import fakeredis

from src.utils import save_if_new

redis = fakeredis.FakeRedis()
redis.mset({"123": "098", "456": "765"})


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "question_id, expected_result",
    [(123, True), (456, True), ("123", True), ("456", True), ("1203", False), (765, False)],
)
async def test_save_if_new_method(question_id, expected_result):
    result = save_if_new(redis, question_id)

    assert result == expected_result
    assert redis.exists(question_id) == 1
