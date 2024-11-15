import os
import sys, shutil
import numpy as np
import torch
import pandas as pd
from news.logger import logging
from news.exception import CustomException
from torch.utils.data import DataLoader
from datasets import Dataset
from safetensors.torch import load_file
from typing import Dict
from news.constants import *
from news.configuration.s3_operations import S3Operation
from sklearn.metrics import accuracy_score, f1_score
from safetensors import safe_open
from news.entity.config_entity import ModelEvaluationConfig, ModelTrainerConfig
from news.entity.artifact_entity import ModelEvaluationArtifacts, ModelTrainerArtifacts, DataTransformationArtifacts
from news.ml.model import RobertaModel

class ModelEvaluation:
    def __init__(self, model_evaluation_config: ModelEvaluationConfig,
                 model_trainer_artifacts: ModelTrainerArtifacts,
                 data_transformation_artifacts: DataTransformationArtifacts,
                 model_trainer_config: ModelTrainerConfig):
        
        self.model_evaluation_config = model_evaluation_config
        self.model_trainer_artifacts = model_trainer_artifacts
        self.data_transformation_artifacts = data_transformation_artifacts
        self.model_trainer_config = model_trainer_config
        self.robertamodel = RobertaModel(model_trainer_config)
        self.tokenizer = self.robertamodel.tokenizer
        self.awscloud = S3Operation()
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    def get_best_model_from_aws(self) -> str:
        try:
            logging.info("Entered the get_best_model_from_aws method of Model Evaluation class")
            os.makedirs(self.model_evaluation_config.BEST_MODEL_DIR_PATH, exist_ok=True)
            best_model_path = self.model_evaluation_config.BEST_MODEL_DIR_PATH
            self.awscloud.download_folder(local_dir=best_model_path,
                                          folder_key=BEST_MODEL_DIR,
                                          bucket_name=self.model_evaluation_config.BUCKET_NAME)
            logging.info("Exited the get_best_model_from_aws method of Model Evaluation class")
            return best_model_path
        except Exception as e:
            logging.warning("Best model not found on AWS, will proceed with locally trained model.")
            return None

    def evaluate_model(self, model_path: str, test_data_loader: DataLoader) -> float:
        try:
            model = self.robertamodel.model

            # Load the model weights from the safetensors file
            state_dict = load_file(model_path)
            model.load_state_dict(state_dict)

            model.to(self.device)
            model.eval()
            
            # Define lists to store predictions and true labels
            predictions, true_labels = [], []

            with torch.no_grad():
                for batch in test_data_loader:
                    # Tokenize batch text
                    inputs = self.tokenizer(batch[TEXT], padding=True, truncation=True,
                                            max_length=MAX_SEQ_LENGTH, return_tensors="pt")
                    inputs = {k: v.to(self.device) for k, v in inputs.items()}
                    labels = batch[LABEL].to(self.device)

                    # Forward pass
                    outputs = model(**inputs)
                    _, preds = torch.max(outputs.logits, dim=1)

                    predictions.extend(preds.cpu().tolist())
                    true_labels.extend(labels.cpu().tolist())

            # Calculate accuracy and F1 score
            accuracy = accuracy_score(true_labels, predictions)
            f1 = f1_score(true_labels, predictions, average='weighted')
            return accuracy, f1

        except Exception as e:
            raise CustomException(e, sys) from e
    
    def save_evaluation_results(self, model_type: str, accuracy: float, f1: float):
        """Save model evaluation results to a CSV file."""
        try:
            evaluation_path = self.model_evaluation_config.MODEL_EVALUATION_FILE_NAME
            results = {"Model Type": [model_type], "Accuracy": [accuracy], "F1 Score": [f1]}
            results_df = pd.DataFrame(results)

            # Append or create CSV
            if os.path.exists(evaluation_path):
                results_df.to_csv(evaluation_path, mode='a', header=False, index=False)
            else:
                results_df.to_csv(evaluation_path, index=False)

            logging.info(f"Saved evaluation results for {model_type} to {evaluation_path}")
        except Exception as e:
            raise CustomException(e, sys) from e

    def copy_best_model(self, source_path: str):
        """Copy the best model to the 'best_model' folder in the project directory."""
        try:
            # Define the path for the 'best_model' folder in the current project directory
            best_model_path = os.path.join(os.getcwd(), BEST_MODEL_DIR)
            os.makedirs(best_model_path, exist_ok=True)
            
            # Copy all files from the source path to the 'best_model' directory
            for file_name in os.listdir(source_path):
                shutil.copy(os.path.join(source_path, file_name), best_model_path)
            
            logging.info(f"Copied best model from {source_path} to {best_model_path}")
        except Exception as e:
            raise CustomException(e, sys) from e


    def tokenize_data(self, examples: Dict) -> Dict:
        return self.tokenizer(examples[TEXT], 
                              padding=PADDING, 
                              truncation=True, 
                              max_length=MAX_SEQ_LENGTH)

    def initiate_model_evaluation(self) -> ModelEvaluationArtifacts:
        try:
            logging.info("Starting model evaluation process.")
            test_df = pd.read_csv(self.data_transformation_artifacts.transformed_test_data_path)
            test_dataset = Dataset.from_pandas(test_df)
            test_dataset = test_dataset.map(self.tokenize_data, batched=True)
            test_loader = DataLoader(test_dataset, batch_size=EVAL_BATCH_SIZE)

            best_model_path = self.get_best_model_from_aws()
            if best_model_path and os.path.exists(os.path.join(best_model_path, 'model.safetensors')):
                aws_accuracy, aws_f1 = self.evaluate_model(os.path.join(best_model_path, 'model.safetensors'), test_loader)
            else:
                aws_accuracy, aws_f1 = 0, 0
            self.save_evaluation_results("AWS Model", aws_accuracy, aws_f1)
            
            local_accuracy, local_f1 = self.evaluate_model(os.path.join(self.model_trainer_artifacts.trained_model_path, 'model.safetensors'), test_loader)
            self.save_evaluation_results("Local Model", local_accuracy, local_f1)

            if local_accuracy >= aws_accuracy and local_f1 >= aws_f1:
                best_model_path = self.model_trainer_artifacts.trained_model_path
                is_model_accepted = True
                logging.info("Local model chosen as the best model.")
            else:
                is_model_accepted = False
                logging.info("AWS model chosen as the best model.")

            # Copy the best model to the final directory
            self.copy_best_model(best_model_path)

            model_evaluation_artifacts = ModelEvaluationArtifacts(
                trained_model_accuracy=max(local_accuracy, aws_accuracy),
                is_model_accepted=is_model_accepted,
                best_model_path=best_model_path
            )

            logging.info(f"Evaluation metrics for {best_model_path} - Accuracy: {max(local_accuracy, aws_accuracy)}, F1 Score: {max(local_f1, aws_f1)}")

            logging.info("Model evaluation completed successfully.")
            return model_evaluation_artifacts

        except Exception as e:
            raise CustomException(e, sys) from e