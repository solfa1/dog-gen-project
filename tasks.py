from celery_app import celery  # <-- import the Celery instance

@celery.task
def get_dog_pics(breed, limit=5):
    # Dummy implementation for testing
    return {"breed": breed, "limit": limit, "pics": [f"{breed}_pic_{i}" for i in range(limit)]}

