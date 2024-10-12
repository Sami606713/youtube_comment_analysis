# This script is used to ingest data from the source and store it in the data lake.
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np
import os 
import logging
logging.basicConfig(level=logging.INFO)

class DataIngestion:
    def __init__(
                    self,data_url,output_path,random_state,
                    train_path,test_path
                 ) -> None:
        
        self.url=data_url
        self.output_path=output_path
        self.random_state=random_state
        self.train_data_path=train_path
        self.test_data_path=test_path
    
    def get_data(self):
        """
        This fun is responsible for getting the data and save them.
        Args:
        URL (str): Url of the data.

        Returns:
        DataFrame: pandas dataframe
        """
        try:
            logging.info('Reading the data')
            df=pd.read_csv(self.url)
            logging.info(df.head())

            # split the data
            x_train,x_test=self.split_data(df=df)
            # Saving the data
            df.to_csv(self.output_path,index=False)
            
            # save train data
            x_train.to_csv(self.train_data_path,index=False)
            # save test data
            x_test.to_csv(self.test_data_path,index=False)
        except Exception as e:
            return str(e)
    
    def split_data(self,df):
        """
        This fun can split the data into train and test set
        """
        try:
            x_train,x_test=train_test_split(df,test_size=0.2,random_state=self.random_state)
            return x_train,x_test
        except Exception as e:
            print(str(e))
        
if __name__=="__main__":
    url="https://raw.githubusercontent.com/Himanshu-1703/reddit-sentiment-analysis/refs/heads/main/data/reddit.csv"
    raw_output_path='data/raw/raw.csv'
    train_output_path='data/raw/train.csv'
    test_output_path='data/raw/test.csv'
    random_state=43

    data=DataIngestion(data_url=url,output_path=raw_output_path,test_path=test_output_path,
                       train_path=train_output_path,random_state=random_state)
    data.get_data()
    
