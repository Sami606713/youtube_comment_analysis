# youtube_comment_analysis
- Let's do something new! Let's build a YouTube comments analyzer.

## Folder Structure

| Folder/Files               | Description                                                                 |
|----------------------------|-----------------------------------------------------------------------------|
| `data/raw`                  | Contains the raw, unprocessed data.                                          |
| `data/processed`            | Contains the cleaned and processed data ready for analysis.                  |
| `Notebooks`                 | Jupyter notebooks for experimentation and data analysis.                    |
| `Models`                    | Saved models and related artifacts.                                         |
| `reports`                   | Reports generated during the analysis or after training.                    |
| `src`                       | Source code for the project.                                                |
| `src/data`                  | Scripts related to data ingestion, cleaning, and feature engineering.       |
| `src/models`                | Scripts for model training, evaluation, and selection.                      |
| `src/tests`                 | Unit tests for different modules of the project.                            |
| `Config`                    | Configuration files for project settings.                                   |
| `README.md`                 | Project overview and folder structure (this file).                          |
| `requirements.txt`          | Required Python packages for running the project.                          |
| `.gitignore`                | Specifies files to be ignored by git.                                       |
| `LICENSE`                   | License file for the project.                                               |
| `setup.py`                  | Script for installing the project as a Python package.                      |
| `Dockerfile`                | Dockerfile for containerizing the project.                                  |
| `.dockerignore`             | Specifies files to be ignored by Docker.                                    |
| `test_environment.py`       | Script for testing the environment configuration.                           |
| `dvc.yaml`                  | Data version control configuration.                                         |
| `app.py`                    | Entry point for any web or API services related to the project.             |
| `.env`                      | Environment variables for configuring the project.                          |



# Data Ingestion
* In this stage we will get the data from the given source. After getting the data we can save them in data folder we will also split the data into train and test set. 
Here is the script
```python
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
    url="URL of the data"
    raw_output_path='raw data path'
    train_output_path='train data path'
    test_output_path='test data path'
    random_state=43

    data=DataIngestion(data_url=url,output_path=raw_output_path,test_path=test_output_path,
                       train_path=train_output_path,random_state=random_state)
    data.get_data()
```