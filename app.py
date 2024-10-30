from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
from mlflow import MlflowClient
from dotenv import load_dotenv
import pandas as pd
import mlflow
import pickle as pkl
import dagshub
import uvicorn
from typing import List
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import requests
import io
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

# set app origins
# Define allowed origins, including your Chrome extension ID
origins = [
    "chrome-extension://jbimockbemodbcghgmichmnnblnkfclc",  # Replace with your actual extension ID
    "http://127.0.0.1",  # Localhost, in case you're testing on the browser
    "http://localhost"    # For localhost as well
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)


class PredictionSentiment(BaseModel):
    text: list[str]

class CloudRequest(BaseModel):
    text: str

@app.get("/")
def read_root():
    return {"Title": "Welcome to youtube comment Analysier"}

@app.post("/predict")
async def predict(comments: PredictionSentiment):
    try:
        # Convert input data to DataFrame
        data = pd.DataFrame(comments.text, columns=["clean_comment"])
        print(data)
        processor = load_processor(processor_path='Models/transformer.pkl')

        # # transform the data
        final_data= processor.transform(data)
        # # load model
        model=load_model()

        # # prediction
        response=model.predict(final_data)

        # Prepare structured results
        results = []
        for comment, sentiment in zip(comments.text, response):
            sentiment_label = {0: "Negative", 1: "Neutral", 2: "Positive"}.get(sentiment, "Unknown")
            results.append({"comment": comment, "sentiment": sentiment_label})

        return {"predictions": results}  # Return structured predictions

    except Exception as e:
        return {"Error": str(e)}

@app.post("/generate_wordcloud/")
async def generate_wordcloud(request:CloudRequest):
    try:
        text = request.text  
        print(text)
        # Generate word cloud
        wordcloud = WordCloud(width=800, height=400).generate(text)

        # Save the word cloud image to an in-memory file
        img_io = io.BytesIO()
        wordcloud.to_image().save(img_io, format="PNG")
        img_io.seek(0)

        return StreamingResponse(img_io, media_type="image/png")
    except Exception as e:
        return {"Error": str(e)}


@app.post("/generate_summary/")
async def generate_summary(text: str):
    API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
    headers = {"Authorization": "Bearer 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"}

    def query(payload):
        response = requests.post(API_URL, headers=headers, json=payload)
        try:
            response_data = response.json()
            # Check if summary is available in the response
            if 'summary_text' in response_data[0]:
                return response_data[0]['summary_text']
            else:
                return {"error": "Summarization model did not return a summary"}
        except (ValueError, IndexError) as e:
            return {"error": f"Failed to parse response: {str(e)}"}

    # Use the provided 'text' as input for the summarization query
    output = query({"inputs": text})
    
    # Raise an exception if there's an error
    if isinstance(output, dict) and "error" in output:
        raise HTTPException(status_code=500, detail=output["error"])
    
    return {"summary": output}
