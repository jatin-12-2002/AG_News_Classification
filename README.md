# AG
celery -A celery_app worker --loglevel=info
uvicorn app:app --reload
