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
import bentoml
import time
import yaml
import warnings
import bentoml
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
        self.config=read_congif()
    
    
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
            with mlflow.start_run(run_name="Final Model"):
                # model=self.stack_model()
                 # Logistic Regression params
                lr_params = self.config['model_params']['logistic_regression']
                model=LogisticRegression(**lr_params, max_iter=1000)
                # Log the parameters
                model_params = model.get_params()
                mlflow.log_params(model_params)

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

                # log and save the model
                mlflow.sklearn.log_model(model, "model")

                # Save the run details (this will generate a unique run ID)
                run_id = mlflow.active_run().info.run_id

                # register the model
                mlflow.register_model(f"runs:/{run_id}/model", "Best_Model")
                self.set_model_alias("Best_Model",model)
                # Save model using BentoML

                bentoml.mlflow.save_model("best_model", model)
                print("Model saved to BentoML store!")

        except Exception as e:
            logging.error(f"Error in training the model: {e}")
            raise
    
    def stack_model(self):
        """
        This fun can build the hybrid model.
        base model: 3
        meta learner: 1
        """
        try:
            # Random Forest
            random_forest_params = self.config['model_params']['random_forest']

            # XGBoost Params
            xgboost_params = self.config['model_params']['xgboost']

            # SVM Params
            svm_params = self.config['model_params']['svm']

            # Logistic Regression params
            lr_params = self.config['model_params']['logistic_regression']

            # knn parameter
            knn_params = self.config['model_params']['knn']
            # Base Model
            base_models = [
                ('Logistic Regression', LogisticRegression(**lr_params, max_iter=1000)),
                ('RandomForest', RandomForestClassifier(**random_forest_params)),
                ('XGBoost', xgb.XGBClassifier(**xgboost_params)),
                ('SVM', SVC(**svm_params))
            ]

            # Meta-learner
            meta_learner = KNeighborsClassifier(**knn_params)

            # Create stacking classifier
            stacking_classifier = StackingClassifier(estimators=base_models, final_estimator=meta_learner)

            return stacking_classifier
        except Exception as e:
            return str(e)
    
    def set_model_alias(self, model_name, model):
        """
        This function will register the model with an alias.
        """
        try:
            logging.info("Registering the model.")
            client = MlflowClient()
            latest_version = model.version

            # Transition the latest version to alias as 'dev'
            logging.info(f"Model version {latest_version}")
            client.set_registered_model_alias(model_name, "dev", version=latest_version)

        except Exception as e:
            logging.error(f"Error in registering the model: {e}")


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