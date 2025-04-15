import logging
import os
from datetime import datetime

class Logger:
    @staticmethod
    def get_logger(name):
        logger = logging.getLogger(name)
        
        if not logger.handlers:
            logger.setLevel(logging.INFO)
            
            # Create logs directory if it doesn't exist
            log_dir = "logs"
            if not os.path.exists(log_dir):
                os.makedirs(log_dir)
            
            # Create file handler
            current_date = datetime.now().strftime('%Y-%m-%d')
            file_handler = logging.FileHandler(f"{log_dir}/test_execution_{current_date}.log")
            file_handler.setLevel(logging.INFO)
            
            # Create console handler
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO)
            
            # Create formatter
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            file_handler.setFormatter(formatter)
            console_handler.setFormatter(formatter)
            
            # Add handlers to logger
            logger.addHandler(file_handler)
            logger.addHandler(console_handler)
        
        return logger