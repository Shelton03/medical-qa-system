import torch
from transformers import pipeline, AutoTokenizer, AutoModelForQuestionAnswering
from app.core.logger import logger

qa_pipeline = None

def initialize_qa_pipeline():
    """
    Loads the BioBERT QA model and tokenizer, and sets up the transformers pipeline.
    This should be called once on application startup.
    Detects and uses the best available hardware (CUDA, MPS, CPU).
    """
    global qa_pipeline
    if qa_pipeline is None:
        logger.info("Initializing BioBERT Question-Answering pipeline...")
        try:
            device = "cpu"
            if torch.cuda.is_available():
                device = "cuda"
            elif torch.backends.mps.is_available():
                device = "mps"
            
            logger.info(f"Using device: {device}")

            # Using a specific model for medical QA
            model_name = "dmis-lab/biobert-large-cased-v1.1-squad"
            
            # The device can be passed directly to the pipeline in newer versions
            # For broader compatibility, device_map can be used, or send model to device manually.
            # pipeline() handles this well. Specifying device is the modern way.
            qa_pipeline = pipeline(
                "question-answering",
                model=model_name,
                tokenizer=model_name,
                device=device if device != "cpu" else -1 # device=-1 is for CPU
            )

            logger.info("BioBERT QA pipeline initialized successfully.")
        except Exception as e:
            logger.error(f"An error occurred during BioBERT QA pipeline initialization: {e}")
            qa_pipeline = None

def get_qa_pipeline():
    """
    Returns the loaded BioBERT QA pipeline instance.
    """
    return qa_pipeline
