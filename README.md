﻿# youtube_comment_analysis
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
* In this stage we will get the data from the give soucre in this case we have a data url where we can get the data.
    - Here is the data link https://raw.githubusercontent.com/Himanshu-1703/reddit-sentiment-analysis/refs/heads/main/data/reddit.csv.
    - The data we will get in the raw form so we can clean the data by applying some transformation in this way so that data is ready for model use.
# Data Transformation
* In this step we will apply the transformation on data But we can apply those transformetin that we will give best result in our experiment stage.

# Model Building
* In this stage we will build the model.
