from dataclasses import dataclass


# Data Ingestion Artifacts
@dataclass
class DataIngestionArtifacts:
    zip_data_file_path: str
    train_csv_file_path: str
    test_csv_file_path: str


# Data Validation Artifacts
@dataclass
class DataValidationArtifacts:
    validation_status: bool


# Data Transformation Artifacts
@dataclass
class DataTransformationArtifacts:
    transformed_train_data_path: str       # Path to the transformed training data
    transformed_test_data_path: str        # Path to the transformed test data