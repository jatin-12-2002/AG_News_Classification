import os,sys
import re
import pandas as pd
import string
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords', quiet=True)
from nltk.stem import PorterStemmer
from news.entity.config_entity import DataTransformationConfig
from news.entity.artifact_entity import DataTransformationArtifacts, DataIngestionArtifacts
from news.exception import CustomException
from news.logger import logging

class DataTransformation:
    def __init__(self, data_transformation_config: DataTransformationConfig, data_ingestion_artifacts: DataIngestionArtifacts):
        self.data_transformation_config = data_transformation_config
        self.data_ingestion_artifacts = data_ingestion_artifacts
        self.stemmer = PorterStemmer()

    def load_data(self):
        train_data = pd.read_csv(self.data_ingestion_artifacts.train_csv_file_path, header=0,
                                            names=[self.data_transformation_config.CLASS, 
                                                    self.data_transformation_config.TITLE, 
                                                    self.data_transformation_config.DESCRIPTION])
        test_data = pd.read_csv(self.data_ingestion_artifacts.test_csv_file_path, header=0,
                                                    names=[self.data_transformation_config.CLASS, 
                                                            self.data_transformation_config.TITLE, 
                                                            self.data_transformation_config.DESCRIPTION])
        return train_data, test_data

    
    def clean_text(self, text_series: pd.Series) -> pd.Series:
        """
        Applies data cleaning transformations to a pandas Series of text data.
        """
        def remove_html_tags(text):
            return re.sub(r'<.*?>', '', text)
        
        def remove_urls(text):
            return re.sub(r'https?://\S+|www\.\S+', '', text)
        
        def tokenize(text):
            return re.findall(r"[\w']+", text.lower())
        
        def remove_stopwords(tokens):
            stop_words = set(stopwords.words('english'))
            return [word for word in tokens if word not in stop_words]
        
        def remove_punctuation(tokens):
            return [''.join(char for char in word if char not in string.punctuation) for word in tokens]
        
        def remove_numbers(tokens):
            return [word for word in tokens if not word.isdigit()]
        
        def stem_words(tokens):
            return [self.stemmer.stem(word) for word in tokens]
        
        def remove_extra_words(tokens):
            extra_words = ['href', 'lt', 'gt', 'ii', 'iii', 'ie', 'quot', 'com']
            return [word for word in tokens if word not in extra_words]

        # Applying transformations step by step
        text_series = text_series.apply(remove_html_tags)
        text_series = text_series.apply(remove_urls)
        text_series = text_series.apply(tokenize)
        text_series = text_series.apply(remove_stopwords)
        text_series = text_series.apply(remove_punctuation)
        text_series = text_series.apply(remove_numbers)
        text_series = text_series.apply(stem_words)
        text_series = text_series.apply(remove_extra_words)
        
        return text_series.apply(lambda tokens: ' '.join(tokens))


    def transform_data(self, train_data: pd.DataFrame, test_data: pd.DataFrame):
        """
        Transforms the train and test data by applying the cleaning pipeline and
        adjusting labels to start from zero.
        """
        # Combine title and description for full text and adjust labels
        train_x = self.clean_text(train_data[self.data_transformation_config.TITLE] + " " + 
                                  train_data[self.data_transformation_config.DESCRIPTION])
        test_x = self.clean_text(test_data[self.data_transformation_config.TITLE] + " " + 
                                 test_data[self.data_transformation_config.DESCRIPTION])
        train_y = train_data[self.data_transformation_config.CLASS] - 1
        test_y = test_data[self.data_transformation_config.CLASS] - 1

        # Create transformed dataframes
        df_train = pd.DataFrame({self.data_transformation_config.LABEL: train_y, self.data_transformation_config.TEXT: train_x})
        df_test = pd.DataFrame({self.data_transformation_config.LABEL: test_y, self.data_transformation_config.TEXT: test_x})
        
        return df_train, df_test
        
    
    def initiate_data_transformation(self) -> DataTransformationArtifacts:
        """
        Initiates data transformation and saves the transformed data as CSV files.
        """
        try:
            logging.info("Loading data for transformation")
            train_data, test_data = self.load_data()
            
            logging.info("Transforming train and test data")
            df_train, df_test = self.transform_data(train_data, test_data)

            logging.info("Saving transformed train and test data to CSV")
            os.makedirs(self.data_transformation_config.data_transformation_artifacts_dir, exist_ok=True)
            df_train.to_csv(self.data_transformation_config.df_train_path, index=False)
            df_test.to_csv(self.data_transformation_config.df_test_path, index=False)
            
            data_transformation_artifact = DataTransformationArtifacts(
                                    transformed_train_data_path=self.data_transformation_config.df_train_path,
                                    transformed_test_data_path=self.data_transformation_config.df_test_path
                                )

            logging.info("Data transformation complete")

            return data_transformation_artifact

        except Exception as e:
            raise CustomException(e, sys) from e