# This script is responsible for applying the transformation on the data.
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import pickle as pkl
from scipy.sparse import hstack
import os
import logging

logging.basicConfig(level=logging.INFO)

class DataTransformation:
    def __init__(self,clean_data_path:str,train_output_path:str,
                 test_output_path:str,transformer_path:str) -> None:
        self.df=pd.read_csv(clean_data_path).dropna(subset=['clean_comment'])
        self.train_output_path=train_output_path
        self.test_output_path=test_output_path
        self.transformer_path=transformer_path

    def split_data(self,df):
        """
        This fun is responsible for splitting the data into train and test.
        """
        try:
            logging.info('saperate features and target')
            feature=df[['clean_comment']]
            target=df['category']
            
            logging.info('Splitting the data into train and test')
            
            x_train,x_test,y_train,y_test=train_test_split(feature,target,test_size=0.2,random_state=42)
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
                ('convert_text_vector',CountVectorizer(max_features=15000))
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
    
    def save_model(self,model,output_path):
        """
        This function will save the model to the disk
        """
        try:
            logging.info("Saving the model")
            with open(output_path, 'wb') as file:
                pkl.dump(model, file)
        except Exception as e:
            logging.error(f"Error in saving the model: {e}")
            raise

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
            
            logging.info("Concatenating the data")
            train_array = hstack([x_train_transform, y_train.values.reshape(-1, 1)]).tocsr()
            test_array = hstack([x_test_transform, y_test.values.reshape(-1, 1)]).tocsr()

            logging.info("Save the train and test array")
            np.save(file=self.train_output_path,arr=train_array.toarray())
            np.save(file=self.test_output_path,arr=test_array.toarray())

            logging.info(f"saving the transformer at {self.transformer_path}")
            self.save_model(transformer,self.transformer_path)
            logging.info("Data Transformation Completed......")
        except Exception as e:
            return str(e)


if __name__=="__main__":
    clean_data_path='data/processed/clean.csv'
    train_output_path='data/processed/train.npy'
    test_output_path='data/processed/test.npy'
    transformer_path='models/transformer.pkl'
    

    transformation=DataTransformation(clean_data_path,train_output_path,
                                      test_output_path,transformer_path)
    transformation.process()