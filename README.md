# AG
celery -A celery_app worker --loglevel=info


uvicorn app:app --host 0.0.0.0 --port 8080


aws s3 cp /path/to/local_folder s3://your-bucket-name/your-folder-name --recursive

022499021177.dkr.ecr.us-east-1.amazonaws.com/agnews

5b719dde7cd17f4d9d103673ffe4e755f36393022c9b2bde3a387ea8669b02854b7518033597b97c