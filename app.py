from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse
from fastapi.responses import Response
from uvicorn import run as app_run
from train import training as start_training
from news.pipeline.prediction_pipeline import PredictionPipeline
from news.constants import APP_HOST, APP_PORT

# Initialize the FastAPI app
app = FastAPI()

# Allow cross-origin requests
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root endpoint to redirect to API docs
@app.get("/", tags=["authentication"])
async def index():
    return RedirectResponse(url="/docs")

# Endpoint for training the model
@app.get("/train", tags=["training"])
async def training():
    """
    Trigger the training pipeline to train the AG News classification model.
    """
    try:
        start_training()

        return Response("Training completed successfully!")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error occurred during training: {e}")

# Endpoint for making predictions
@app.post("/predict", tags=["prediction"])
async def predict_route(text: str):
    """
    Predict the label for the provided text input.
    """
    try:
        if not text.strip():
            raise HTTPException(status_code=400, detail="Input text cannot be empty.")

        prediction_pipeline = PredictionPipeline()
        predictions = prediction_pipeline.run_pipeline([text])  # Accepting a single input as a list
        return predictions[0]  # Returning the prediction for the first (and only) text
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error occurred during prediction: {e}")

# Main function to run the app
if __name__ == "__main__":
    app_run(app, host=APP_HOST, port=APP_PORT)