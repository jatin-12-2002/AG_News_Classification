import sys
from news.logger import logging
from news.exception import CustomException
from news.components.data_ingestion import DataIngestion
from news.components.data_validation import DataValidation
from news.components.data_transformation import DataTransformation
from news.components.model_trainer import ModelTrainer
from news.configuration.s3_operations import S3Operation
from news.constants import *

from news.entity.config_entity import (DataIngestionConfig,
                                       DataValidationConfig,
                                       DataTransformationConfig,
                                       ModelTrainerConfig)

from news.entity.artifact_entity import (DataIngestionArtifacts,
                                         DataValidationArtifacts,
                                         DataTransformationArtifacts,
                                         ModelTrainerArtifacts)

class TrainPipeline:
    def __init__(self):
        self.data_ingestion_config = DataIngestionConfig()
        self.data_validation_config = DataValidationConfig()
        self.data_transformation_config = DataTransformationConfig()
        self.model_trainer_config = ModelTrainerConfig()
        self.awscloud = S3Operation()

    
     # This method is used to start the data ingestion
    def start_data_ingestion(self) -> DataIngestionArtifacts:
        logging.info("Entered the start_data_ingestion method of TrainPipeline class")
        try:
            logging.info("Getting the data from AWS S3 cloud storage")
            data_ingestion = DataIngestion(
                data_ingestion_config=self.data_ingestion_config, awscloud=self.awscloud
            )
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
            logging.info("Got the data from AWS S3 cloud storage")
            logging.info(
                "Exited the start_data_ingestion method of TrainPipeline class"
            )
            return data_ingestion_artifact

        except Exception as e:
            raise CustomException(e, sys) from e
        
    
    def start_data_validation(
        self, data_ingestion_artifact: DataIngestionArtifacts
    ) -> DataValidationArtifacts:
        logging.info("Entered the start_data_validation method of TrainPipeline class")

        try:
            data_validation = DataValidation(
                data_ingestion_artifact=data_ingestion_artifact,
                data_validation_config=self.data_validation_config,
                data_ingestion_config=self.data_ingestion_config
            )

            data_validation_artifact = data_validation.initiate_data_validation()

            logging.info("Performed the data validation operation")

            logging.info(
                "Exited the start_data_validation method of TrainPipeline class"
            )

            return data_validation_artifact

        except Exception as e:
            raise CustomException(e, sys) from e
        
    
    def start_data_transformation(self, data_ingestion_artifacts = DataIngestionArtifacts) -> DataTransformationArtifacts:
        logging.info("Entered the start_data_transformation method of TrainPipeline class")
        try:
            data_transformation = DataTransformation(
                data_ingestion_artifacts = data_ingestion_artifacts,
                data_transformation_config=self.data_transformation_config
            )

            data_transformation_artifacts = data_transformation.initiate_data_transformation()
            
            logging.info("Exited the start_data_transformation method of TrainPipeline class")
            return data_transformation_artifacts

        except Exception as e:
            raise CustomException(e, sys) from e
    
        
    def start_model_trainer(self, data_transformation_artifacts: DataTransformationArtifacts) -> ModelTrainerArtifacts:
        logging.info(
            "Entered the start_model_trainer method of TrainPipeline class"
        )
        try:
            model_trainer = ModelTrainer(data_transformation_artifacts=data_transformation_artifacts,
                                        model_trainer_config=self.model_trainer_config
                                        )
            model_trainer_artifacts = model_trainer.initiate_model_trainer()
            logging.info("Exited the start_model_trainer method of TrainPipeline class")
            return model_trainer_artifacts

        except Exception as e:
            raise CustomException(e, sys) 
        
    
    def run_pipeline(self):
        logging.info("Entered the run_pipeline method of TrainPipeline class")
        try:
            print(f"*******************")
            print(f">>>>>> stage DATA INGESTION started <<<<<<")
            data_ingestion_artifacts = self.start_data_ingestion()
            print(f">>>>>> stage DATA INGESTION completed <<<<<<\n\nx==========x")

            print(f"*******************")
            print(f">>>>>> stage DATA VALIDATION started <<<<<<")            
            data_validation_artifact = self.start_data_validation(
                data_ingestion_artifact=data_ingestion_artifacts
            )
            print(f">>>>>> stage DATA VALIDATION completed <<<<<<\n\nx==========x")

            print(f"*******************")
            print(f">>>>>> stage DATA TRANSFORMATION started <<<<<<")
            data_transformation_artifacts = self.start_data_transformation(
                data_ingestion_artifacts=data_ingestion_artifacts
            )
            print(f">>>>>> stage DATA TRANSFORMATION completed <<<<<<\n\nx==========x")

            print(f"*******************")
            print(f">>>>>> stage MODEL TRAINING started <<<<<<")
            model_trainer_artifacts = self.start_model_trainer(
                data_transformation_artifacts=data_transformation_artifacts
            )
            print(f">>>>>> stage MODEL TRAINING completed <<<<<<\n\nx==========x")
            print(f"*******************")

            logging.info("Exited the run_pipeline method of TrainPipeline class") 

        except Exception as e:
            raise CustomException(e, sys) from e