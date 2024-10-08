import os 
from pathlib import Path

# make folders
dir_=[
    os.path.join("data","raw"),
    os.path.join("data","processed"),
    "Notebooks",
    "Models",
    "reports",
    "src",
    os.path.join("src","data"),
    os.path.join("src","models"),
    os.path.join('src',"tests"),
    "Config"
]

for folder in dir_:
    if not os.path.exists(folder):
        os.makedirs(folder)
        # add the .git keep file
        git_keep = os.path.join(folder,".gitkeep")

        with open(git_keep,"w") as f:
            pass
    else:
        print(f"{folder} already exists")

# place files in each folder
files=[
    os.path.join("src","__init__.py"),
    os.path.join("src","utils.py"),
    os.path.join('src','data',"__init__.py"),
    os.path.join('src','data',"data_ingestion.py"),
    os.path.join('src','data',"data_cleaning.py"),
    os.path.join('src','data',"feature_engineering.py"),
    os.path.join('src','data',"data_transformation.py"),

    os.path.join('src','models',"__init__.py"),
    os.path.join('src','models',"train_model.py"),
    os.path.join('src','models',"find_best_model.py"),

    os.path.join('src','tests',"__init__.py"),
    os.path.join('src','tests',"test_model.py"),

    os.path.join('Config',"config.yml"),
    
    "README.md",
    "requirements.txt",
    ".gitignore",
    "LICENSE",
    "setup.py",
    "Dockerfile",
    ".dockerignore",
    "test_environment.py",
    "dvc.yaml",
    "app.py",
    ".env"
]

for file in files:
    try:
        if not os.path.exists(file) or os.path.getsize(file)==0:
            with open(file,"w") as f:
                pass
    except Exception as e:
        print(f"Error creating {file}: {str(e)}")