from src.config import Settings

settings = Settings()


def test_get_rabbitmq_uri():
    rabbit = settings.rabbit
    expected_uri = (
        f"amqp://{rabbit.user}:{rabbit.password}@{rabbit.host}:{rabbit.port}/{rabbit.vhost}"
    )

    result_uri = settings.rabbitmq_uri

    assert expected_uri == result_uri
