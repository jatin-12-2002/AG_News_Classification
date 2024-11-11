import os
import sys
import shutil
from news.logger import logging
from news.exception import CustomException
from news.entity.config_entity import DataValidationConfig, DataIngestionConfig
from news.entity.artifact_entity import DataIngestionArtifacts, DataValidationArtifacts

class DataValidation:
    def __init__(self, data_ingestion_artifact: DataIngestionArtifacts, data_validation_config: DataValidationConfig,
                 data_ingestion_config: DataIngestionConfig):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_ingestion_config = data_ingestion_config
            self.data_validation_config = data_validation_config
        except Exception as e:
            raise CustomException(e, sys)

    def validate_all_files_exist(self) -> bool:
        """Check if required CSV files exist in the extracted data."""
        try:
            logging.info("Checking if all required files exist in the extracted dataset.")

            # List of all files in the data ingestion directory
            all_files_in_dir = os.listdir(self.data_ingestion_config.data_ingestion_artifacts_dir)
            missing_files = [
                required_file for required_file in self.data_validation_config.required_file_list 
                if required_file not in all_files_in_dir
            ]

            validation_status = len(missing_files) == 0

            # Log missing files if any, and write validation status
            os.makedirs(self.data_validation_config.data_validation_dir, exist_ok=True)
            status_file_path = self.data_validation_config.valid_status_file_dir
            with open(status_file_path, 'w') as f:
                if validation_status:
                    f.write("Validation status: True\n")
                    logging.info("All required files are present.")
                else:
                    f.write("Validation status: False\n")
                    f.write(f"Missing files: {', '.join(missing_files)}\n")
                    logging.error(f"Missing required files: {', '.join(missing_files)}")

            return validation_status
        except Exception as e:
            raise CustomException(e, sys)

    def initiate_data_validation(self) -> DataValidationArtifacts:
        """Initiates data validation and returns a DataValidationArtifacts with the status."""
        logging.info("Starting data validation process.")
        try:
            # Validate all required files
            status = self.validate_all_files_exist()

            # Generate a data validation artifact based on the status
            data_validation_artifact = DataValidationArtifacts(validation_status=status)
            logging.info(f"Data validation artifact: {data_validation_artifact}")

            # Optionally copy the zip file if validation is successful
            if status:
                shutil.copy(self.data_ingestion_artifact.zip_data_file_path, os.getcwd())

            return data_validation_artifact
        except Exception as e:
            raise CustomException(e, sys)