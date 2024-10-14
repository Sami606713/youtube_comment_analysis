# This script is responsible for training the models
import numpy as np
from sklearn.metrics import r2_score,mean_absolute_error,mean_squared_error
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score
from sklearn.metrics import (
    accuracy_score,precision_score,recall_score,
    confusion_matrix,classification_report
)
from src.data.data_transformation import DataTransformation
import matplotlib.pyplot as plt
import seaborn as sns
import mlflow
import mlflow.sklearn
from mlflow import MlflowClient
import numpy as np
import pandas as pd
import pickle as pkl
import logging
import dagshub
from dotenv import load_dotenv
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


# =================================Model Training=====================================#
class ModelTraining:
    def __init__(self,x_train,x_test,y_train,y_test) -> None:
        self.x_train=x_train
        self.x_test=x_test
        self.y_train=y_train
        self.y_test=y_test
    
    
    def train_model(self):
        """
        This fun is responsible for training the model
        input: x_train,y_train
        output: model
        """
        try:
            x_train=self.x_train
            x_test=self.x_test
            y_train=self.y_train
            y_test=self.y_test

            # Train the best model again and track them using mlflow
            with mlflow.start_run(run_name="Trial Model"):
                model=LogisticRegression()
                # Fit the pipeline
                logging.info('Fit the model')
                model.fit(x_train, y_train)

                # Generate the prediction
                y_pred = model.predict(x_test)

                # Calculate the accuracy, precision, recall, confusion matrix
                accuracy = accuracy_score(y_test, y_pred)
                precision = precision_score(y_test, y_pred, average='weighted')
                recall = recall_score(y_test, y_pred, average='weighted')
                confusion_mat = confusion_matrix(y_test, y_pred)
                classification_rep = classification_report(y_test, y_pred, output_dict=True)

                # Log metrics on MLflow
                mlflow.log_metric("Accuracy", accuracy)
                mlflow.log_metric("Precision", precision) 
                mlflow.log_metric("Recall", recall)

                # Log detailed metrics from classification report
                for label, metrics in classification_rep.items():
                    if isinstance(metrics, dict):  # for each class or average type
                        for metric_name, metric_value in metrics.items():
                            mlflow.log_metric(f"{label} {metric_name}", metric_value)

                # Log the model
                mlflow.sklearn.log_model(model, "Model")

                # Log the parameters
                mlflow.log_params({"model":model.get_params()})

                # Log the confusion matrix plot
                plt.figure(figsize=(8, 6))
                sns.heatmap(confusion_mat, annot=True, fmt='d', cmap='Blues',
                            xticklabels=['Negative', 'Neutral', 'Positive'],
                            yticklabels=['Negative', 'Neutral', 'Positive'])
                plt.xlabel('Predicted Labels')
                plt.ylabel('True Labels')
                plt.title('Confusion Matrix')

                # Save the plot to a file and log it
                plt.savefig("reports/confusion_matrix.png")
                plt.close()
                mlflow.log_artifact("reports/confusion_matrix.png")

                # # Log the data as an artifact
                # mlflow.log_artifact("data/processed/clean.csv")

        except Exception as e:
            logging.error(f"Error in training the model: {e}")
            raise
    
    # def register_model(self,model_name,final_model):
    #     """
    #     This function will save the model to mlfow
    #     """
    #     try:
    #         logging.info("Register the model.")
    #         client = MlflowClient()
    #         latest_versions = final_model.version

    #         # Transition the latest version to alais as dev
    #         print(f"Model version {final_model.version}")
    #         client.set_registered_model_alias(model_name, "dev", version=latest_versions)

    #     except Exception as e:
    #         logging.error(f"Error in register the model: {e} with version {latest_versions}")
    

if __name__=="__main__":
    
    clean_data_path='data/processed/clean.csv'
    transformer_path='models/transformer.pkl'
    
    transformation=DataTransformation(clean_data_path,transformer_path)
    x_train,x_test,y_train,y_test=transformation.process()

    print(x_train.shape,x_test.shape,y_train.shape,y_test.shape)
    # Model training
    trainer=ModelTraining(x_train=x_train,x_test=x_test,
                                  y_train=y_train,y_test=y_test)
    trainer.train_model()