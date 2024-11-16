# AG
celery -A celery_app worker --loglevel=info


uvicorn app:app --reload


aws s3 cp /path/to/local_folder s3://your-bucket-name/your-folder-name --recursive

022499021177.dkr.ecr.us-east-1.amazonaws.com/agnews

2ea632bf09f32d18f56c46a1b8596550cca6b485d5ca3d226ca444cdef384b6204ac23f42bc0aae2