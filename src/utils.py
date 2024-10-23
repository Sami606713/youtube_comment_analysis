import yaml
import logging
import pickle as pkl
logging.basicConfig(level=logging.INFO)

def save_processor(model,output_path):
        """
        This function will save the model to the disk
        """
        try:
            logging.info("Saving the model")
            with open(output_path, 'wb') as file:
                pkl.dump(model, file)
        except Exception as e:
            logging.error(f"Error in saving the model: {e}")
            raise

def read_congif():
    """
    This fun is responsible for reading the configuration file.
    """
    try:
        with open('Config/config.yml', 'r') as file:
            config=yaml.safe_load(file)
        return config
    except Exception as e:
        return str(e)