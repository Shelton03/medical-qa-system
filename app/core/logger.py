import logging
import sys
from app.core.config import settings

def setup_logger():
    logger = logging.getLogger("medical_qa")
    logger.setLevel(settings.LOG_LEVEL)
    
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(settings.LOG_LEVEL)
    
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)
    
    if not logger.handlers:
        logger.addHandler(handler)
        
    return logger

logger = setup_logger()
