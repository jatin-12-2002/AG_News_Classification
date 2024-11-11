import os

from datetime import datetime

# Common constants
TIMESTAMP: str = datetime.now().strftime("%m_%d_%Y_%H_%M_%S")
ARTIFACTS_DIR = os.path.join("artifacts", TIMESTAMP)
LOGS_DIR = "logs"
LOGS_FILE_NAME = "news.log"
MODELS_DIR = "models"
BEST_MODEL_DIR = "best_model"
LABEL = 'label'
TEXT = 'text'


"""
Data INGESTION realted contant start with DATA_INGESTION VAR NAME
"""
BUCKET_NAME = 'agnews-data'
AWS_DATA_FILE_NAME = "archive.zip"
DATA_INGESTION_ARTIFACTS_DIR = "DataIngestionArtifacts"
DATA_INGESTION_TRAIN_FILE_DIR = "train.csv"
DATA_INGESTION_TEST_FILE_DIR = "test.csv"


"""
Data Validation realted contant start with DATA_VALIDATION VAR NAME
"""

DATA_VALIDATION_ARTIFACTS_DIR: str = "DataValidationArtifacts"

DATA_VALIDATION_STATUS_FILE = 'status.txt'

DATA_VALIDATION_ALL_REQUIRED_FILES = ["test.csv", "train.csv"]