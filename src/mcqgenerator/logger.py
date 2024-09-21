import logging
import os
from datetime import datetime

LOG_FILE = f"{datetime.now().strftime("%Y-%m-%d_%H%_M_%S")}.log"

log_path = os.path.join(os.getcwd(),"log")

os.mkdir(log_path,)

LOG_FILE_PATH = os.path.join(log_path,LOG_FILE)

logging.basicConfig(level=logging.INFO, 
                    filename=LOG_FILE_PATH,
                    format = "[%(asctime)s] - %(lineno)s - %(name)s - %(levelname)s - %(message)s ")