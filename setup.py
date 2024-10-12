from setuptools import find_packages,setup

def get_packages(file_path:str):
    """
    Reads the requirements.txt file and returns a list of required packages.

    Args:
        file_path (str): The path to the requirements.txt file.

    Returns:
        List[str]: A list of required packages mentioned in the file.
    """
    try:
        with open(file_path, "r") as f:
            # Read all packages from the file, excluding the '-e .' entry
            requirements = [line.strip() for line in f.readlines() if line.strip() and line.strip() != "-e ."]
        return requirements
    except Exception as e:
        raise FileNotFoundError(f"Error reading the requirements file: {str(e)}")




setup(
    name="youtube-comment-analysis",
    version="0.1.0",
    author="Samiullah",
    author_email="sami606713@gamil.com",
    description="A Python package for analyzing YouTube comments and performing sentiment analysis.",
    url="https://github.com/Sami606713/youtube_comment_analysis",  # Add your repository URL
    packages=find_packages(),  # Automatically discover and include all packages
    install_requires=get_packages("requirements.txt"),  # Install required packages
    license="MIT",  # Specify the license
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries",
    ],
    python_requires='>=3.10',  # Specify compatible Python versions
)