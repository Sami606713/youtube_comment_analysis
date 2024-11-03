# This script is responsible for applying the transformation on the data.
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from src.utils import read_congif,save_processor
from sklearn.pipeline import Pipeline
import pickle as pkl
from scipy.sparse import hstack
import os
import logging
import yaml

logging.basicConfig(level=logging.INFO)

class DataTransformation:
    def __init__(
                self,clean_data_path:str,
                transformer_path:str
            ) -> None:
        self.df=pd.read_csv(clean_data_path).dropna(subset=['clean_comment'])
        self.transformer_path=transformer_path
        self.config=read_congif()

    def split_data(self,df):
        """
        This fun is responsible for splitting the data into train and test.
        """
        try:
            logging.info('saperate features and target')
            feature=df[['clean_comment']]
            target=df['category']
            
            logging.info(f"Splitting the data into train and test {self.config['data_split']}")
            
            x_train,x_test,y_train,y_test=train_test_split(feature,target,test_size=self.config['data_split']['split_ratio'],
                                                           random_state=self.config['data_split']['random_state'])
            logging.info('Data split successfully')
            
            return x_train,x_test,y_train,y_test
        except Exception as e:
            return str(e)
    
    def build_transformer(self):
        """
        This fun is responsible for transforming the data.
        """
        try:
            pipe=Pipeline(steps=[
                ('convert_text_vector',CountVectorizer(ngram_range=(1, 1), max_features=15000))
            ])

            # build a transformer
            logging.info("Building Transformer")
            transfomer=ColumnTransformer(transformers=[
                ("tranform",pipe,'clean_comment')
            ],remainder='passthrough')

            # Build the final pipeline
            logging.info("Building Final pipelines")
            final_pipe=Pipeline(steps=[
                ('process',transfomer)
            ])
            return final_pipe
        except Exception as e:
            return str(e)

    def process(self):
        """
        This fun is responsible for processing the data.
        """
        try:
            logging.info('Processing the data')
            x_train,x_test,y_train,y_test=self.split_data(self.df)
            
            # load the transformer
            transformer=self.build_transformer()

            # fit the transformer
            logging.info("Fitting the transformer")
            x_train_transform=transformer.fit_transform(x_train)
            x_test_transform=transformer.transform(x_test)

            # Concatenate sparse matrices with targets
            logging.info(f"saving the transformer at {self.transformer_path}")
            if not os.path.exists(self.transformer_path):
                os.makedirs(self.transformer_path,exist_ok=True)

            save_processor(transformer,self.transformer_path)
            logging.info("Data Transformation Completed......")

            return x_train_transform,x_test_transform,y_train,y_test
            
        except Exception as e:
            return str(e)


if __name__=="__main__":
    clean_data_path='data/processed/clean.csv'
    transformer_path='models/transformer.pkl'
    

    transformation=DataTransformation(clean_data_path,transformer_path)
    x_train,x_test,y_train,y_test=transformation.process()