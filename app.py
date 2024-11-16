from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from uvicorn import run as app_run
from train import training as start_training
from celery.result import AsyncResult
from celery_app import train_model_task, predict_task
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
        task = train_model_task.delay()  # Trigger the Celery task

        return JSONResponse(content={"task_id": task.id, "message": "Training started in the background."})

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error occurred during training: {e}")


@app.get("/train-status/{task_id}", tags=["training"])
async def train_status(task_id: str):
    """
    Check the status of a training task.
    """
    try:
        task_result = AsyncResult(task_id, app=train_model_task)
        if task_result.state == "PENDING":
            return {"task_id": task_id, "status": "Pending", "message": "Task is still in the queue."}
        elif task_result.state == "SUCCESS":
            return {"task_id": task_id, "status": "Success", "result": task_result.result}
        elif task_result.state == "FAILURE":
            return {"task_id": task_id, "status": "Failure", "error": str(task_result.info)}
        else:
            return {"task_id": task_id, "status": task_result.state}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error checking task status: {e}")
    

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

        task = predict_task.delay(text)  # Trigger the Celery task for prediction
        return JSONResponse(content={"task_id": task.id, "message": "Prediction started in the background."})
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error occurred during prediction: {e}")
    
@app.get("/predict-status/{task_id}", tags=["prediction"])
async def predict_status(task_id: str):
    """
    Check the status of a prediction task.
    """
    try:
        task_result = AsyncResult(task_id, app=predict_task)
        if task_result.state == "PENDING":
            return {"task_id": task_id, "status": "Pending", "message": "Task is still in the queue."}
        elif task_result.state == "SUCCESS":
            return {"task_id": task_id, "status": "Success", "result": task_result.result}
        elif task_result.state == "FAILURE":
            return {"task_id": task_id, "status": "Failure", "error": str(task_result.info)}
        else:
            return {"task_id": task_id, "status": task_result.state}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error checking task status: {e}")

# Main function to run the app
if __name__ == "__main__":
    app_run(app, host=APP_HOST, port=APP_PORT)