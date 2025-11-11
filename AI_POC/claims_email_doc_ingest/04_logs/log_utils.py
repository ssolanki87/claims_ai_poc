import logging
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional
import json

class CustomFormatter(logging.Formatter):
    """Custom formatter with colors for console output"""
    
    grey = "\x1b[38;21m"
    blue = "\x1b[38;5;39m"
    yellow = "\x1b[38;5;226m"
    red = "\x1b[38;5;196m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    
    FORMATS = {
        logging.DEBUG: grey + "%(asctime)s - %(name)s - %(levelname)s - %(message)s" + reset,
        logging.INFO: blue + "%(asctime)s - %(name)s - %(levelname)s - %(message)s" + reset,
        logging.WARNING: yellow + "%(asctime)s - %(name)s - %(levelname)s - %(message)s" + reset,
        logging.ERROR: red + "%(asctime)s - %(name)s - %(levelname)s - %(message)s" + reset,
        logging.CRITICAL: bold_red + "%(asctime)s - %(name)s - %(levelname)s - %(message)s" + reset
    }
    
    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt, datefmt='%Y-%m-%d %H:%M:%S')
        return formatter.format(record)

class LogUtils:
    """Centralized logging utilities"""
    
    @staticmethod
    def setup_logger(
        name: str,
        log_level: str = "INFO",
        log_dir: Optional[str] = None
    ) -> logging.Logger:
        """Setup logger with file and console handlers"""
        
        logger = logging.getLogger(name)
        logger.setLevel(getattr(logging, log_level.upper()))
        
        # Remove existing handlers
        logger.handlers.clear()
        
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(CustomFormatter())
        logger.addHandler(console_handler)
        
        # File handler
        if log_dir:
            log_path = Path(log_dir)
            log_path.mkdir(parents=True, exist_ok=True)
            
            log_file = log_path / f"{name}_{datetime.now().strftime('%Y%m%d')}.log"
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(logging.DEBUG)
            file_formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            file_handler.setFormatter(file_formatter)
            logger.addHandler(file_handler)
        
        return logger
    
    @staticmethod
    def log_pipeline_start(logger: logging.Logger, pipeline_name: str, params: dict):
        """Log pipeline start with parameters"""
        logger.info(f"{'='*80}")
        logger.info(f"Starting pipeline: {pipeline_name}")
        logger.info(f"Parameters: {json.dumps(params, indent=2)}")
        logger.info(f"{'='*80}")
    
    @staticmethod
    def log_pipeline_end(logger: logging.Logger, pipeline_name: str, stats: dict):
        """Log pipeline end with statistics"""
        logger.info(f"{'='*80}")
        logger.info(f"Pipeline completed: {pipeline_name}")
        logger.info(f"Statistics: {json.dumps(stats, indent=2)}")
        logger.info(f"{'='*80}")
    
    @staticmethod
    def log_error_with_context(logger: logging.Logger, error: Exception, context: dict):
        """Log error with additional context"""
        logger.error(f"Error occurred: {str(error)}")
        logger.error(f"Context: {json.dumps(context, indent=2)}")
        logger.exception(error)
