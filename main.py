import time
import threading
import subprocess
import platform
from utils.customlogger import CustomLogger

# Setting up custom logger
logger = CustomLogger(name="MainLogger", log_file="main.log").get_logger()


def run_surrealdb_new_terminal() -> None:
    """Run the SurrealDB server in a new terminal window."""
    try:
        logger.info("Launching SurrealDB in a new terminal...")
        if platform.system() == "Windows":
            # Launch in new PowerShell window
            subprocess.Popen(
                [
                    "start",
                    "powershell",
                    "-NoExit",
                    "-Command",
                    "surreal start --log trace --username root --password root --bind 127.0.0.1:8001",
                ],
                shell=True,
            )
        else:
            # macOS / Linux: open a new terminal tab/window
            subprocess.Popen(
                [
                    "gnome-terminal",
                    "--",
                    "bash",
                    "-c",
                    "surreal start --log trace --username root --password root --bind 127.0.0.1:8001; exec bash",
                ]
            )
    except Exception as e:
        logger.error(f"Failed to start SurrealDB in new terminal: {e}")


def run_backend() -> None:
    """Run the FastAPI backend server."""
    try:
        logger.info("Starting FastAPI backend server...")
        subprocess.run(["python", "-m", "src.backend.server"], check=True)
    except subprocess.CalledProcessError as e:
        logger.error(f"Backend server failed: {e}")
    except KeyboardInterrupt:
        logger.info("Backend server stopped by user.")


def run_frontend() -> None:
    """Run the Flet frontend application."""
    try:
        time.sleep(3)  # give backend time
        logger.info("Starting Flet frontend application...")
        subprocess.run(["python", "-m", "src.frontend.client"], check=True)
    except subprocess.CalledProcessError as e:
        logger.error(f"Frontend application failed: {e}")
    except KeyboardInterrupt:
        logger.info("Frontend application stopped by user.")


def main() -> None:
    try:
        logger.info("Starting Patient Management System...")

        # Start SurrealDB in a new terminal window
        run_surrealdb_new_terminal()

        # Wait a little so SurrealDB has time to boot
        time.sleep(5)

        # Start backend in a separate thread
        backend_thread = threading.Thread(target=run_backend, daemon=True)
        backend_thread.start()

        # Start frontend in main thread
        run_frontend()
    except Exception as e:
        logger.error(f"Error occurred in main: {e}")


if __name__ == "__main__":
    main()
