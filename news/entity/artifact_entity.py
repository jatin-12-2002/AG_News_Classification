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