from dataclasses import dataclass
import os
from news.constants import *


@dataclass
class DataIngestionConfig:
    def __init__(self):
        self.data_ingestion_artifacts_dir: str = os.path.join(
            ARTIFACTS_DIR, DATA_INGESTION_ARTIFACTS_DIR
        )
        self.aws_data_file_path: str = os.path.join(
            self.data_ingestion_artifacts_dir, AWS_DATA_FILE_NAME
        )
        self.train_csv_file_path: str = os.path.join(
            self.data_ingestion_artifacts_dir, DATA_INGESTION_TRAIN_FILE_DIR
        )
        self.test_csv_file_path: str = os.path.join(
            self.data_ingestion_artifacts_dir, DATA_INGESTION_TEST_FILE_DIR
        )
        self.S3_DATA_NAME = AWS_DATA_FILE_NAME


@dataclass
class DataValidationConfig:
    def __init__(self):
        self.data_validation_dir: str = os.path.join(ARTIFACTS_DIR, DATA_VALIDATION_ARTIFACTS_DIR)
        self.valid_status_file_dir: str = os.path.join(self.data_validation_dir, DATA_VALIDATION_STATUS_FILE)
        self.required_file_list = DATA_VALIDATION_ALL_REQUIRED_FILES


@dataclass
class DataTransformationConfig:
    def __init__(self):
        self.data_transformation_artifacts_dir: str = os.path.join(ARTIFACTS_DIR, DATA_TRANSFORMATION_ARTIFACTS_DIR)
        self.df_train_path: str = os.path.join(self.data_transformation_artifacts_dir, DATA_TRANSFORMATION_TRAIN_TRANSFORMED_FILE)
        self.df_test_path: str = os.path.join(self.data_transformation_artifacts_dir, DATA_TRANSFORMATION_TEST_TRANSFORMED_FILE)
        self.CLASS = CLASS
        self.TITLE = TITLE
        self.DESCRIPTION = DESCRIPTION 
        self.LABEL = LABEL
        self.TEXT = TEXT

@dataclass
class ModelTrainerConfig: 
    def __init__(self):
        self.TRAINED_MODEL_DIR: str = os.path.join(ARTIFACTS_DIR,MODEL_TRAINER_ARTIFACTS_DIR) 
        self.TRAINED_MODEL_PATH = os.path.join(self.TRAINED_MODEL_DIR,MODEL_TRAINER_MODEL_SAVE_PATH)
        self.ACCURACY = MODEL_TRAINER_METRICS[0]
        self.F1 = MODEL_TRAINER_METRICS[1]

        self.LEARNING_RATE = LEARNING_RATE
        self.EPOCHS = EPOCHS
        self.TRAIN_BATCH_SIZE = TRAIN_BATCH_SIZE
        self.EVAL_BATCH_SIZE = EVAL_BATCH_SIZE
        self.WEIGHT_DECAY = WEIGHT_DECAY
        self.LOGGING_STEPS = LOGGING_STEPS
        self.SAVE_STRATEGY = SAVE_STRATEGY
        self.EVAL_STRATEGY = EVAL_STRATEGY
        self.MAX_SEQ_LENGTH = MAX_SEQ_LENGTH
        self.LABEL = LABEL
        self.TEXT = TEXT
        self.AXIS = AXIS
        self.PADDING = PADDING

        self.MODEL_NAME = MODEL_NAME
        self.NUM_LABELS = NUM_LABELS
        self.NUMBER_OF_LAYERS = NUMBER_OF_LAYERS