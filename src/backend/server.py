import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.backend.api import APIClient
from utils.customlogger import CustomLogger

# Setting up custom logger
logger = CustomLogger(name="ServerLogger", log_file="server.log").get_logger()

# Global variable to hold api_client
api_client = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan event handler for startup and shutdown."""
    global api_client
    
    # Startup
    logger.info("FastAPI application startup initiated.")
    api_client = APIClient(app)
    logger.info("FastAPI application startup complete.")
    
    yield
    
    # Shutdown
    if api_client:
        api_client.shutdown()
    logger.info("FastAPI application shutdown complete.")


# Initialize FastAPI with lifespan
app = FastAPI(
    title="Patient Management System",
    lifespan=lifespan
)


def main() -> None:
    """Entry point for running FastAPI with uvicorn."""
    try:
        logger.info("Starting FastAPI server on http://127.0.0.1:8080 ...")
        uvicorn.run(
            "src.backend.server:app",  # Correct module path for uvicorn
            host="127.0.0.1",
            port=8000,
            reload=False
        )
    except Exception as e:
        logger.error(f"Error occurred while running server: {e}")


if __name__ == "__main__":
    main()