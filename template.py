import os
from pathlib import Path

# make folders
dir_ = [
    os.path.join("data", "raw"),
    os.path.join("data", "processed"),
    "Notebooks",
    "Models",
    "reports",
    "src",
    os.path.join("src", "data"),
    os.path.join("src", "models"),
    os.path.join("src", "tests"),
    "Config",
    "youtube-extension",                # New folder for Chrome extension
]

# Subfolders for Chrome extension
youtube_extension_subfolders = [
    "youtube-extension/assets",         # Assets like icons
    "youtube-extension/scripts",        # Extension scripts
    "youtube-extension/styles"          # Optional styles (CSS)
]

# Add subfolders for the extension
dir_.extend(youtube_extension_subfolders)

for folder in dir_:
    if not os.path.exists(folder):
        os.makedirs(folder)
        # add the .gitkeep file
        git_keep = os.path.join(folder, ".gitkeep")

        with open(git_keep, "w") as f:
            pass
    else:
        print(f"{folder} already exists")

# place files in each folder
files = [
    os.path.join("src", "__init__.py"),
    os.path.join("src", "utils.py"),
    os.path.join('src', 'data', "__init__.py"),
    os.path.join('src', 'data', "data_ingestion.py"),
    os.path.join('src', 'data', "data_cleaning.py"),
    os.path.join('src', 'data', "feature_engineering.py"),
    os.path.join('src', 'data', "data_transformation.py"),

    os.path.join('src', 'models', "__init__.py"),
    os.path.join('src', 'models', "train_model.py"),
    os.path.join('src', 'models', "evalute.py"),

    os.path.join('src', 'tests', "__init__.py"),
    os.path.join('src', 'tests', "test_model.py"),

    os.path.join('Config', "config.yml"),

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
    ".env",

    # Chrome Extension Files
    os.path.join("youtube-extension", "manifest.json"),
    os.path.join("youtube-extension/scripts", "content.js"),
    os.path.join("youtube-extension/scripts", "background.js"),
    os.path.join("youtube-extension", "popup.html"),
    os.path.join("youtube-extension/styles", "popup.css"),
    os.path.join("youtube-extension/assets", "icon.png")
]

for file in files:
    try:
        if not os.path.exists(file) or os.path.getsize(file) == 0:
            with open(file, "w") as f:
                pass
    except Exception as e:
        print(f"Error creating {file}: {str(e)}")
