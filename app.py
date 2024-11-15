from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from uvicorn import run as app_run
from train import training as start_training
from news.pipeline.prediction_pipeline import PredictionPipeline
from news.constants import *

# Initialize the FastAPI app
app = FastAPI()

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Allow cross-origin requests
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", response_class=HTMLResponse)
async def home():
    """
    Serve the frontend HTML file.
    """
    return FileResponse("templates/index.html")

# Endpoint for training the model
@app.get("/train", tags=["training"])
async def training():
    """
    Trigger the training pipeline to train the AG News classification model.
    """
    try:
        start_training()

        return JSONResponse(content={"message": "Training started successfully!"})

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error occurred during training: {e}")

# Endpoint for making predictions
@app.post("/predict", tags=["prediction"])
async def predict_route(request: Request):
    """
    Predict the label for the provided text input.
    """
    try:
        data = await request.json()
        text = data.get("text", "").strip()

        if not text.strip():
            raise HTTPException(status_code=400, detail="Input text cannot be empty.")

        prediction_pipeline = PredictionPipeline()
        prediction = prediction_pipeline.run_pipeline([text])[0]  # Single input prediction
        return JSONResponse(content=prediction)  # Returning the prediction for the first (and only) text
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error occurred during prediction: {e}")

# Main function to run the app
if __name__ == "__main__":
    app_run(app, host=APP_HOST, port=APP_PORT)