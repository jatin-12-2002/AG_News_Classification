import sys
from news.logger import logging
from news.exception import CustomException
from news.components.data_ingestion import DataIngestion
from news.configuration.s3_operations import S3Operation
from news.constants import *

from news.entity.config_entity import (DataIngestionConfig)

from news.entity.artifact_entity import (DataIngestionArtifacts)

class TrainPipeline:
    def __init__(self):
        self.data_ingestion_config = DataIngestionConfig()
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
        
    
    def run_pipeline(self):
        logging.info("Entered the run_pipeline method of TrainPipeline class")
        try:
            print(f"*******************")
            print(f">>>>>> stage DATA INGESTION started <<<<<<")
            data_ingestion_artifacts = self.start_data_ingestion()
            print(f">>>>>> stage DATA INGESTION completed <<<<<<\n\nx==========x")

            
            logging.info("Exited the run_pipeline method of TrainPipeline class") 

        except Exception as e:
            raise CustomException(e, sys) from e