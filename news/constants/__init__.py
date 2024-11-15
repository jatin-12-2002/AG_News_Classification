import os

from datetime import datetime

# Common constants
TIMESTAMP: str = datetime.now().strftime("%m_%d_%Y_%H_%M_%S")
ARTIFACTS_DIR = os.path.join("artifacts", TIMESTAMP)
LOGS_DIR = "logs"
LOGS_FILE_NAME = "news.log"


"""
Data INGESTION realted contant start with DATA_INGESTION VAR NAME
"""
BUCKET_NAME = 'agnews-data'
AWS_DATA_FILE_NAME = "archive_mini.zip"
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
MODEL_TRAINER_MODEL_SAVE_PATH = "final_model"
MODEL_TRAINER_METRICS = ["accuracy","f1"]

LEARNING_RATE = 1e-5
EPOCHS = 1
TRAIN_BATCH_SIZE = 16
EVAL_BATCH_SIZE = 16
WEIGHT_DECAY = 0.1
LOGGING_STEPS = 1000
SAVE_STRATEGY = "epoch"
EVAL_STRATEGY = "epoch"
MAX_SEQ_LENGTH = 128  # Max length for tokenization
METRICS = ["accuracy","f1"]
AXIS = 1
PADDING = "max_length"

# Model Architecture constants
MODEL_NAME = 'roberta-base'
NUM_LABELS = 4
NUMBER_OF_LAYERS = 4


"""
Model EVALUATION realted contant start with MODEL_EVALUATION VAR NAME
"""
MODEL_EVALUATION_ARTIFACTS_DIR = 'ModelEvaluationArtifacts'
BEST_MODEL_DIR = "best_model"
MODEL_EVALUATION_FILE_NAME = 'model_evaluation.csv'


APP_HOST = "0.0.0.0"
APP_PORT = 8080