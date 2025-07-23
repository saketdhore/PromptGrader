from app.api.endpoints import grading as grading_router
from app.api.endpoints import consulting as consulting_router
from app.api.endpoints import engineering as engineering_router
from app.api.endpoints import refining as refining_router
from fastapi import FastAPI
import logging
import uvicorn
from dotenv import load_dotenv
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)
app = FastAPI(
    title= "PromptScore API",
    description= "API for grading and refining prompts",
    version= "1.0.0",
)

app.include_router(
    grading_router.router,
    prefix="/api/v1",
    tags=["grading"]
)

#add suggestions router
app.include_router(
    consulting_router.router,
    prefix="/api/v1",
    tags=["consulting"]
)

app.include_router(
    engineering_router.router,
    prefix="/api/v1",
    tags=["engineering"]
)

app.include_router(
    refining_router.router,
    prefix = "/api/v1",
    tags=["refining"]
)


@app.get("/")
async def root():
    """
    Root endpoint to check if the API is running.
    """
    return {"message": "Welcome to the Prompt Scorer API!"}

if __name__ == "__main__":
    logger.info("Loading environment variables...")
    load_dotenv()
    logger.info("Environment variables loaded successfully.")
    logger.info("Starting FastAPI application...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
    