import os, sys
from news.logger import logging
from news.exception import CustomException
from news.configuration.s3_operations import S3Operation
from news.entity.config_entity import ModelPusherConfig
from news.entity.artifact_entity import ModelPusherArtifacts
from news.constants import *

class ModelPusher:
    def __init__(self, model_pusher_config: ModelPusherConfig):
        """
        :param model_pusher_config: Configuration for model pusher
        """
        self.model_pusher_config = model_pusher_config
        self.awscloud = S3Operation()


    def initiate_model_pusher(self) -> ModelPusherArtifacts:
        """
            Method Name :   initiate_model_pusher
            Description :   This method initiates model pusher.

            Output      :    Model pusher artifact
        """
        logging.info("Entered initiate_model_pusher method of ModelTrainer class")
        try:
             # Ensure the final model path exists
            if not os.path.exists(self.model_pusher_config.TRAINED_MODEL_PATH):
                raise FileNotFoundError(f"Final model not found at {self.model_pusher_config.TRAINED_MODEL_PATH}")
            
            # Define the destination in S3
            model_s3_key = self.model_pusher_config.TRAINED_MODEL_PATH

            # Uploading the model to AWS S3 storage
            logging.info(f"Uploading {self.model_pusher_config.TRAINED_MODEL_PATH} to bucket {self.model_pusher_config.BUCKET_NAME}")
            self.awscloud.upload_folder(
                bucket_folder_name = self.model_pusher_config.MODEL_NAME,
                bucket_name = self.model_pusher_config.BUCKET_NAME,
                folder_name = model_s3_key
            )
            logging.info(f"Successfully uploaded final model to S3 bucket: {self.model_pusher_config.BUCKET_NAME}")

            # Saving the model pusher artifacts
            model_pusher_artifact = ModelPusherArtifacts(
                bucket_name=self.model_pusher_config.BUCKET_NAME,
                trained_model_path=self.model_pusher_config.TRAINED_MODEL_PATH
            )

            logging.info("Exited the initiate_model_pusher method of ModelTrainer class")
            return model_pusher_artifact

        except Exception as e:
            raise CustomException(e, sys) from e