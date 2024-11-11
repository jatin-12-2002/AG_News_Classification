import os
import sys
from news.exception import CustomException
from news.pipeline.train_pipeline import TrainPipeline

from news.constants import *


def training():
    try:
        train_pipeline = TrainPipeline()

        train_pipeline.run_pipeline()

    except Exception as e:
        raise CustomException(e, sys) from e


if __name__ == "__main__":
    training()