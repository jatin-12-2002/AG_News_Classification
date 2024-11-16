from celery import Celery
from train import training as start_training
from news.pipeline.prediction_pipeline import PredictionPipeline

# Configure Celery with Redis broker and backend
celery_app = Celery(
    "celery_app",
    broker="redis://localhost:6379/0",  # Redis URL
    backend="redis://localhost:6379/0",  # Results stored in Redis
)

@celery_app.task
def train_model_task():
    """
    Run the training process as a Celery task.
    """
    try:
        start_training()  # Call the actual training function
        return {"status": "success", "message": "Training completed successfully."}
    except Exception as e:
        return {"status": "failure", "message": str(e)}

@celery_app.task
def predict_task(text: str):
    """
    Run the prediction process as a Celery task.
    """
    try:
        prediction_pipeline = PredictionPipeline()
        predictions = prediction_pipeline.run_pipeline([text])  # Single input
        return predictions[0]  # Return the prediction
    except Exception as e:
        return {"status": "failure", "message": str(e)}