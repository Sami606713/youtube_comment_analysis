# This script is used to ingest data from the source and store it in the data lake.
import pandas as pd
import numpy as np
import os 
import logging
logging.basicConfig(level=logging.INFO)

class DataIngestion:
    def __init__(
                    self,data_url,output_path
                 ) -> None:
        
        self.url=data_url
        self.output_path=output_path
    
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

            logging.info("Rename the categories")
            df['category']=df['category'].map({
                                        -1:0,
                                        0:1,
                                        1:2
                                    })

            logging.info(df.head())
            logging.info('Data read successfully')

            logging.info('Saving the data')
            # Saving the data
            df.to_csv(self.output_path,index=False)
            logging.info('Data saved successfully')
            
        except Exception as e:
            return str(e)
        
if __name__=="__main__":
    url="https://raw.githubusercontent.com/Himanshu-1703/reddit-sentiment-analysis/refs/heads/main/data/reddit.csv"
    raw_output_path='data/raw/raw.csv'

    data=DataIngestion(data_url=url,output_path=raw_output_path)
    data.get_data()
    