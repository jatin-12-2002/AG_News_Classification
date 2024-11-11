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