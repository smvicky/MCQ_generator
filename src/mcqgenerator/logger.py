import logging
import os
from datetime import datetime

LOG_FILE = f"{datetime.now().strftime("%Y-%m-%d_%H%_M_%S")}.log"

log_path = os.path.join(os.getcwd(),"log")

if not os.path.exists(log_path):
    os.mkdir(log_path)
else:
    print(f"Directory '{log_path}' already exists. Using it for logs.")

LOG_FILE_PATH = os.path.join(log_path,LOG_FILE)

logging.basicConfig(level=logging.INFO, 
                    filename=LOG_FILE_PATH,
                    format = "[%(asctime)s] - %(lineno)s - %(name)s - %(levelname)s - %(message)s ")