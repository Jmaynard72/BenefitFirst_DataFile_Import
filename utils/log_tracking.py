import logging
from datetime import datetime 
import os

date_stamp = datetime.now().strftime('%Y%m%d')
log_file_name = f'{date_stamp}_log.txt'
log_path = os.getcwd()
full_path = log_path + '/Logs/' + log_file_name

def create_log():
   logging.basicConfig(level=logging.INFO, filename=full_path, filemode='w',format="%(asctime)s - %(levelname)s - %(message)s")

def write_log(msg : str,level: str = 'info'):
    logger = logging.getLogger(full_path)
    if level == 'info':
        logger.info(msg)
    elif level == 'warning':
        logger.warning(msg)
    elif level == 'error':
        logger.error(msg)
    elif level == 'critical':
        logger.critical(msg)

def read_log() -> str:
    with open(full_path,'r',encoding='utf-8') as file:
        return file.read()
    

if __name__ == '__main__':
    create_log()
