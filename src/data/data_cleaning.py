# This class is responsible for cleaning the data. It has the following methods:
import pandas as pd
import numpy as np
import logging
import os

logging.basicConfig(level=logging.INFO)

class DataPreprocessing:
    def __init__(self,train_data_path,test_data_path) -> None:
        self.train_data=pd.read_csv(train_data_path)
        self.test_data=pd.read_csv(test_data_path)
    
    def data_cleaning(self):
        """
        This fun is responsible for cleaning the data.
        """
        try:
            logging.info('Cleaning the data')
            self.train_data=self.train_data.dropna()
            self.test_data=self.test_data.dropna()
        except Exception as e:
            return str(e)