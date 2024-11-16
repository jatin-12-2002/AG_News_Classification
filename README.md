# AG
celery -A celery_app worker --loglevel=info


uvicorn app:app --host 0.0.0.0 --port 8080


aws s3 cp /path/to/local_folder s3://your-bucket-name/your-folder-name --recursive

022499021177.dkr.ecr.us-east-1.amazonaws.com/agnews

b82aebe36b9b8e6069e58ebd040d5d868f7380f2fc642d9dbc47a47446da78f766d4b587a262ebd4