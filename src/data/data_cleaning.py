# This class is responsible for cleaning the data. It has the following methods:
import pandas as pd
import numpy as np
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from tqdm import tqdm
import re
import logging
import os
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('punkt')
logging.basicConfig(level=logging.INFO)

class DataPreprocessing:
    def __init__(self,raw_data_path:str,output_path:str) -> None:
        self.df=pd.read_csv(raw_data_path)
        self.output_path=output_path

    def data_cleaning(self,df):
        """
        This fun is responsible for cleaning the data.
        """
        try:
            logging.info('Cleaning the data')
    
            # remove null comments
            df=df[~(df['clean_comment']==' ')]
            # Dropping the duplicates
            df.drop_duplicates(inplace=True)
          
            # Dropping the null values
            df=df.dropna()

            logging.info('Data Cleaning Successfully')
            return df
        except Exception as e:
            return str(e)
    
    def text_preprocess(self,text):
        """
        This fun is responsible for apply all the preprocessing steps.
        """
        try:
            # convert the text into lower case and also remove the unecessary spaces
            text=text.lower().strip()

            # remove the urls
            text=re.sub(r'http[s]?://\S+|www\.\S+','',text)

            # Remove the \n and \t with ""
            text=text.replace("\n"," ").replace("\t"," ")

            # Now get the only

            # Remove the unecessry stopwords
            stopword=set(stopwords.words('english')) - set(["not","but",'because','not','never','no',"about"])

            tokens=[word for word in text.split() if word not in stopword]

            # Apply lemitization
            lemmatizer=WordNetLemmatizer()
            final_token=[lemmatizer.lemmatize(token) for token in tokens]

            return " ".join(final_token)
        except Exception as e:
            return str(e)

    def process(self):
        """
        This fun is responsible for processing the data.
        """
        try:
            df=self.df
            # Cleaning the data
            df=self.data_cleaning(df)

            # Initialize tqdm for progress bar
            tqdm.pandas(desc="Processing comments")

            # Apply the text preprocessing
            df['clean_comment']=df['clean_comment'].progress_apply(lambda x: self.text_preprocess(x))

            # Saving the data
            df.to_csv(self.output_path,index=False)
            logging.info('Clean data saved successfully')
        except Exception as e:
            return str(e)

if __name__=="__main__":
    raw_data_path='data/raw/raw.csv'
    clean_data_path='data/processed/clean.csv'

    data=DataPreprocessing(raw_data_path=raw_data_path,output_path=clean_data_path)
    print(data.process())