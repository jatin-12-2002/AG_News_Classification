# Creating model architecture.
import os,sys
from news.entity.config_entity import ModelTrainerConfig
import torch
from transformers import RobertaForSequenceClassification, RobertaTokenizer
from news.exception import CustomException

class RobertaModel(torch.nn.Module):
    def __init__(self, model_trainer_config: ModelTrainerConfig):
        """
        Initializes the RobertaModel for sequence classification with the specified number of labels.
        Freezes the first few layers as per requirements.
        """
        super(RobertaModel, self).__init__()
        self.model_trainer_config = model_trainer_config
        self.tokenizer = RobertaTokenizer.from_pretrained(self.model_trainer_config.MODEL_NAME)
        self.model = RobertaForSequenceClassification.from_pretrained(model_trainer_config.MODEL_NAME, 
                                                                      num_labels=self.model_trainer_config.NUM_LABELS)

        # Freezing the embeddings and initial encoder layers
        for param in self.model.roberta.embeddings.parameters():
            param.requires_grad = False
        for i, layer in enumerate(self.model.roberta.encoder.layer):
            if i < self.model_trainer_config.NUMBER_OF_LAYERS:  # Adjust the number of layers to freeze as needed
                for param in layer.parameters():
                    param.requires_grad = False

    def forward(self, input_ids, attention_mask, labels=None):
        """
        Forward pass for the model.
        """
        try:
            output = self.model(input_ids=input_ids, attention_mask=attention_mask, labels=labels, return_dict=False)
            return output
        
        except Exception as e:
            raise CustomException(e, sys) from e