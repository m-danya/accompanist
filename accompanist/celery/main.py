from celery import Celery

from accompanist.config import settings

app = Celery(
    "accompanist-worker",
    broker=f"amqp://guest:guest@{settings.RABBITMQ_HOST}:{settings.RABBITMQ_PORT}",
    include=["accompanist.celery.tasks"],
)


if __name__ == "__main__":
    app.start()
