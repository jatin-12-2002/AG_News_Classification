import os, sys
import torch
import pandas as pd
from transformers import TrainingArguments, Trainer
from datasets import Dataset, load_from_disk
import numpy as np
from sklearn.metrics import accuracy_score, f1_score
from typing import Dict
from news.constants import *
from news.entity.config_entity import ModelTrainerConfig
from news.entity.artifact_entity import ModelTrainerArtifacts, DataTransformationArtifacts
from news.logger import logging
from news.ml.model import RobertaModel

class ModelTrainer:
    def __init__(self,data_transformation_artifacts: DataTransformationArtifacts,
                 model_trainer_config: ModelTrainerConfig):
        self.data_transformation_artifacts = data_transformation_artifacts
        self.model_trainer_config = model_trainer_config
        self.robertamodel = RobertaModel(model_trainer_config)
        self.tokenizer = self.robertamodel.tokenizer


    def compute_metrics(self,pred):
        """Compute metrics for evaluation."""
        labels = pred.label_ids
        preds = np.argmax(pred.predictions, axis=self.model_trainer_config.AXIS)
        accuracy = accuracy_score(labels, preds)
        f1 = f1_score(labels, preds, average="weighted")
        return {
            self.model_trainer_config.ACCURACY: accuracy,
            self.model_trainer_config.F1: f1,
        }
    
    def tokenize_data(self, examples: Dict) -> Dict:
        """Tokenizes data for input to the model."""
        return self.tokenizer(examples[self.model_trainer_config.TEXT], 
                                       padding=self.model_trainer_config.PADDING, 
                                       truncation=True, 
                                       max_length=self.model_trainer_config.MAX_SEQ_LENGTH)
    
    def load_datasets(self) -> Dataset:
        """Convert train and test data into Hugging Face Dataset format."""
        # Load CSVs using pandas
        train_df = pd.read_csv(self.data_transformation_artifacts.transformed_train_data_path)
        test_df = pd.read_csv(self.data_transformation_artifacts.transformed_test_data_path)
        
        # Convert DataFrames to Hugging Face Dataset format
        train_dataset = Dataset.from_pandas(train_df)
        test_dataset = Dataset.from_pandas(test_df)
        
        # Tokenize data
        train_dataset = train_dataset.map(self.tokenize_data, batched=True)
        test_dataset = test_dataset.map(self.tokenize_data, batched=True)

        return train_dataset, test_dataset
    
    def initiate_model_trainer(self) -> ModelTrainerArtifacts:
        """Main method to set up, train, and save the model."""
        logging.info("Initializing model training")

        # Load the datasets
        train_dataset, test_dataset = self.load_datasets()

        # Define Training Arguments
        training_args = TrainingArguments(
            output_dir=self.model_trainer_config.TRAINED_MODEL_DIR,
            evaluation_strategy=self.model_trainer_config.EVAL_STRATEGY,
            learning_rate=self.model_trainer_config.LEARNING_RATE,
            per_device_train_batch_size=self.model_trainer_config.TRAIN_BATCH_SIZE,
            per_device_eval_batch_size=self.model_trainer_config.EVAL_BATCH_SIZE,
            num_train_epochs=self.model_trainer_config.EPOCHS,
            weight_decay=self.model_trainer_config.WEIGHT_DECAY,
            logging_dir=os.path.join(self.model_trainer_config.TRAINED_MODEL_DIR, "logs"),
            logging_steps=self.model_trainer_config.LOGGING_STEPS,
            save_strategy=self.model_trainer_config.SAVE_STRATEGY,
            save_total_limit=7,
            load_best_model_at_end=True
        )

        # Initialize the Trainer
        trainer = Trainer(
            model=self.robertamodel.model,
            args=training_args,
            train_dataset=train_dataset,
            eval_dataset=test_dataset,
            tokenizer=self.robertamodel.tokenizer,
            compute_metrics=self.compute_metrics
        )

        # Start training
        logging.info("Starting model training...")
        trainer.train()

        # Save the model
        trainer.model.save_pretrained(self.model_trainer_config.TRAINED_MODEL_PATH)
        # Save the tokenizer
        self.tokenizer.save_pretrained(self.model_trainer_config.TRAINED_MODEL_PATH)


        # Log output paths and return artifact
        logging.info("Model training completed and saved.")
        model_trainer_artifacts = ModelTrainerArtifacts(
            trained_model_path=self.model_trainer_config.TRAINED_MODEL_PATH
        )

        return model_trainer_artifacts