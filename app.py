from fastapi import FastAPI
from pydantic import BaseModel
from mlflow import MlflowClient
from dotenv import load_dotenv
import pandas as pd
import mlflow
import pickle as pkl
import dagshub
import uvicorn
import os
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


def load_processor(processor_path:str):
    """
    This fun is responsible for loading the processor.
    Input: input_path
    output: processor 
    """
    try:
        if os.path.exists(processor_path):
            with open (processor_path,"rb")as f:
                processor=pkl.load(f)
                return processor
        else:
            return f"{processor_path} does not found"
            
    except Exception as e:
        return str(e)


def load_model(model_name="Best_Model"):
    """
    This fun is responsible for loading the model.
    input: Modle Path
    output: Model
    """
    try:
        # in 2-3 days set the version is production
        client=MlflowClient()
        latest_version=client.get_model_version_by_alias(model_name, "champion").version
        if not latest_version:
            return (f"No versions available for model '{model_name}' with alais champion.")
        else:
            model_uri = f"models:/{model_name}@champion" 
            model = mlflow.sklearn.load_model(model_uri) 
        
        return model
    except FileNotFoundError as e:
        return str(e)

app = FastAPI()

class PredictionSentiment(BaseModel):
    text: str

@app.get("/")
def read_root():
    return {"Title": "Welcome to youtube comment Analysier"}

@app.post("/predict")
async def predict(comments: PredictionSentiment):
    try:
        # Convert the input data to a pandas DataFrame
        data = pd.DataFrame([comments.dict()],index=[0])

        input_data=data.rename(columns={"text": 'clean_comment'})
        print(input_data)
        processor = load_processor(processor_path='Models/transformer.pkl')

        # # transform the data
        final_data= processor.transform(input_data)
        # # load model
        model=load_model()

        # # prediction
        response=model.predict(final_data)

        if response==0:
            return "Negative"
        elif response==1:
            return "Neutral"
        elif response==2:
            return "Positive"

        return {"prediction":response}
    except Exception as e:
        return {"Error": str(e)}
