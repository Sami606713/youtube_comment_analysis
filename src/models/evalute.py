# This script is responsible for training the models
from sklearn.metrics import r2_score,mean_absolute_error,mean_squared_error
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import StackingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import cross_val_score
from sklearn.metrics import (
    accuracy_score,precision_score,recall_score,
    confusion_matrix,classification_report
)
from src.data.data_transformation import DataTransformation
from src.utils import read_congif
import matplotlib.pyplot as plt
from dotenv import load_dotenv
import seaborn as sns
import xgboost as xgb
import mlflow
import mlflow.sklearn
from mlflow import MlflowClient
import numpy as np
import pandas as pd
import pickle as pkl
import dagshub
import time
import yaml
import warnings
import logging
import os
warnings.filterwarnings('ignore')
logging.basicConfig(level=logging.INFO)
load_dotenv()
dagshub_token = os.getenv('DAGSHUB_TOKEN')

if dagshub_token:
    os.environ['MLFlow_TRACKING_USERNAME']=dagshub_token
    os.environ['MLFlow_TRACKING_PASSWORD']=dagshub_token
    # Set up the MLflow tracking URI with authentication using the token
    mlflow.set_tracking_uri(f'https://{dagshub_token}:@dagshub.com/Sami606713/youtube_comment_analysis.mlflow')

    print("DagsHub login successful!")
else:
    print("DagsHub token not found. Please set the DAGSHUB_TOKEN environment variable.")


# =================================Model Evulation=====================================#
class EvulateModel:
    def __init__(self,x_test,y_test):
        self.x_test=x_test
        self.y_test=y_test
        self.model_name = "Best_Model"
        self.alais="dev"
    
    def load_model(self):
        """
        This fun is responsible for loading the model.
        input: Modle Path
        output: Model
        """
        try:
            logging.info("Set the client")

            client=MlflowClient()
            logging.info("get the version")

            latest_version=client.get_model_version_by_alias(self.model_name, "dev").version
            print(latest_version)
            if not latest_version:
                return (f"No versions available for model '{self.model_name}' with alais champion.")
            else:
                model_uri = f"models:/{self.model_name}@dev" 
                model = mlflow.sklearn.load_model(model_uri) 
            
            return model
        except FileNotFoundError as e:
            return str(e)
    
    def evulate(self):
        """
        This fun is reponsible for loading the model and perform evulation
        """
        try:
            logging.info("Loading Model")
            model=self.load_model()

            logging.info("Preediction..")
            y_pred=model.predict(self.x_test)
            
            logging.info("Cross Validation")
            test_score=cross_val_score(model,self.x_test,self.y_test,cv=5,scoring="accuracy").mean()

            print(f"Test Score: {test_score}")
            if test_score*100>70:
                self.prompote_model()
        except Exception as e:
            return str(e)
        
    def prompote_model(self):
        """
        This fun is responsible for prompte the model staging --> production.
        """
        try:
            logging.info("Promoting Models")
            client=MlflowClient()
            latest_version=client.get_model_version_by_alias(self.model_name, self.alais).version
            if not latest_version:
                logging.error(f"No versions available for model '{self.model_name}' in alais '{self.alais}'.")

            # Prompte  the model
            print(f"{self.model_name} loaded with version {latest_version}")
            client.set_registered_model_alias(self.model_name,
                                              "champion", 
                                              version=latest_version)
            print("Model Prompted successfully.....")
        except Exception as e:
            return str(e)
        
if __name__=="__main__":
    clean_data_path='data/processed/clean.csv'
    transformer_path='models/transformer.pkl'
    
    transformation=DataTransformation(clean_data_path,transformer_path)
    _,x_test,_,y_test=transformation.process()

    logging.info("Evulate Model")
    evulate=EvulateModel(x_test=x_test,y_test=y_test)
    evulate.evulate()