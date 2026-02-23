from celery import Celery

celery = Celery(
    "dog_generator",
    broker="amqp://guest:guest@rabbitmq:5672//",  # your RabbitMQ URL
    backend="rpc://",  # or whatever result backend you want
)

celery.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    enable_utc=True,
)
