import os
import sys
import torch
from transformers import RobertaTokenizer, RobertaForSequenceClassification
from news.logger import logging
from news.exception import CustomException
from news.constants import *
from news.pipeline.train_pipeline import TrainPipeline
from news.configuration.s3_operations import S3Operation


class PredictionPipeline:
    def __init__(self):
        """
        Initialize the PredictionPipeline class.
        """
        try:
            logging.info("Initializing the PredictionPipeline class")
            
            # Paths and configurations
            self.model_dir = BEST_MODEL_DIR
            self.model_file = os.path.join(self.model_dir, "model.safetensors")
            self.awscloud = S3Operation()
            self.bucket_name = BUCKET_NAME

            # Label mapping for AG News classification
            self.label_mapping = {
                0: "World",
                1: "Sports",
                2: "Business",
                3: "Sci/Tech"
            }

            logging.info("PredictionPipeline class initialized successfully")
        except Exception as e:
            raise CustomException(e, sys) from e
        
    def training(self):
        try:
            train_pipeline = TrainPipeline()

            train_pipeline.run_pipeline()

        except Exception as e:
            raise CustomException(e, sys) from e

    def check_best_model_exists(self):
        """
        Check if the best_model folder and necessary files exist locally.
        """
        try:
            logging.info("Checking if the best_model directory and files exist")
            if not os.path.exists(self.model_dir):
                logging.warning(f"Best model directory '{self.model_dir}' not found.")
                return False

            if not os.path.isfile(self.model_file):
                logging.warning(f"Model file '{self.model_file}' not found.")
                return False

            logging.info("All necessary files found in the best_model directory")
            return True
        
        except Exception as e:
            raise CustomException(e, sys) from e

    def preprocess_text(self, texts, tokenizer):
        """
        Preprocess the input text using the tokenizer.
        """
        try:
            logging.info("Preprocessing the input text")
            inputs = tokenizer(
                texts, padding=True, truncation=True, max_length=MAX_SEQ_LENGTH, return_tensors="pt"
            )
            logging.info("Text preprocessing completed successfully")
            return inputs
        
        except Exception as e:
            raise CustomException(e, sys) from e

    def predict_texts(self, texts, model, tokenizer):
        """
        Predict the labels for the given texts using the model and tokenizer.
        """
        try:
            logging.info("Starting prediction process")
            inputs = self.preprocess_text(texts, tokenizer)

            model.eval()
            device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            model.to(device)
            inputs = {key: val.to(device) for key, val in inputs.items()}

            with torch.no_grad():
                outputs = model(**inputs)
                logits = outputs.logits

            predicted_class_ids = torch.argmax(logits, dim=1)
            confidence_scores = torch.nn.functional.softmax(logits, dim=1).max(dim=1).values
            # Map label IDs to their corresponding AG News category names
            predicted_labels = [
                {
                    "label": self.label_mapping[label_id.item()],
                    "confidence": confidence.item()
                }
                for label_id, confidence in zip(predicted_class_ids, confidence_scores)
            ]
            
            logging.info("Prediction process completed successfully")
            return predicted_labels
        
        except Exception as e:
            raise CustomException(e, sys) from e

    def run_pipeline(self, texts):
        """
        Main pipeline to handle prediction.
        """
        try:
            logging.info("Running the prediction pipeline")

            # Check if the best_model folder exists locally
            if not self.check_best_model_exists():
                logging.warning("Best model not found locally. Checking on S3.")
                
                # Check if the best_model exists in AWS S3
                if not self.awscloud.check_folder_exists(BEST_MODEL_DIR, BUCKET_NAME):
                    logging.warning("Best model not found in S3. Starting training process.")
                    
                    self.training()

                # Download the model from S3 after training or if it already exists
                self.awscloud.download_folder(
                    folder_key=BEST_MODEL_DIR,
                    bucket_name=BUCKET_NAME,
                    local_dir=BEST_MODEL_DIR,
                )

            # Load model and tokenizer
            logging.info("Loading model and tokenizer")
            model = RobertaForSequenceClassification.from_pretrained(self.model_dir)
            tokenizer = RobertaTokenizer.from_pretrained(self.model_dir)

            # Predict
            predictions = self.predict_texts(texts, model, tokenizer)
            logging.info("Prediction pipeline completed successfully")
            return predictions
        except Exception as e:
            raise CustomException(e, sys) from e


# Example Usage
if __name__ == "__main__":
    try:
        pipeline = PredictionPipeline()

        # Example texts for prediction
        sample_texts = [
            "The stock market is performing exceptionally well today.",
            "A devastating hurricane is expected to hit the coast tomorrow.",
        ]
        results = pipeline.run_pipeline(sample_texts)
        for text, result in zip(sample_texts, results):
            print(f"Text: {text}\nPredicted Label: {result['label']}\nConfidence: {result['confidence']:.2f}\n")
    except Exception as e:
        logging.error(f"Error in prediction pipeline: {e}")