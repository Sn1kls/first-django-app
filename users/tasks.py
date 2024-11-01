from celery import shared_task


@shared_task
def test_job():
    print("Це тестова джоба для Celery!")
