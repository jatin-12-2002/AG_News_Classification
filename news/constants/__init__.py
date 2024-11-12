import os

from datetime import datetime

# Common constants
TIMESTAMP: str = datetime.now().strftime("%m_%d_%Y_%H_%M_%S")
ARTIFACTS_DIR = os.path.join("artifacts", TIMESTAMP)
LOGS_DIR = "logs"
LOGS_FILE_NAME = "news.log"
MODELS_DIR = "models"
BEST_MODEL_DIR = "best_model"


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


"""
Data Transformation realted contant start with DATA_TRANSFORMATION VAR NAME
"""

DATA_TRANSFORMATION_ARTIFACTS_DIR = "DataTransformationArtifacts"
DATA_TRANSFORMATION_TRAIN_TRANSFORMED_FILE = "transformed_train.csv"                  # Transformed training data file
DATA_TRANSFORMATION_TEST_TRANSFORMED_FILE  = "transformed_test.csv"                    # Transformed test data file
CLASS = "class_index"
TITLE = "title"
DESCRIPTION = "description"
LABEL = 'label'
TEXT = 'text'


"""
Model Trainer realted contant start with MODEL_TRAINER VAR NAME
"""

MODEL_TRAINER_ARTIFACTS_DIR = 'ModelTrainerArtifacts'
TRAINED_MODEL_DIR = 'trained_model'
TRAINED_MODEL_NAME = 'model.h5'
X_TEST_FILE_NAME = 'x_test.csv'
Y_TEST_FILE_NAME = 'y_test.csv'

X_TRAIN_FILE_NAME = 'x_train.csv'

RANDOM_STATE = 42
EPOCH = 1
BATCH_SIZE = 128
VALIDATION_SPLIT = 0.2


# Model Architecture constants
MODEL_NAME = 'roberta-base'
NUM_LABELS = 4
NUMBER_OF_LAYERS = 4