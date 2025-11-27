"""
DAQ System Launcher - Main entry point for the packaged .exe
This script manages both backend (FastAPI) and frontend (Tkinter) components.
"""

import sys
import os
import subprocess
import time
import threading
import tkinter as tk
from tkinter import messagebox
from pathlib import Path
import logging
import signal
import importlib.util

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('daq_system.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class DAQSystemLauncher:
    def __init__(self):
        self.backend_process = None
        self.uvicorn_server = None
        self.uvicorn_thread = None
        self.backend_ready = False
        self.root = None
        self.backend_thread = None
        self.is_running = True
        
    def get_resource_path(self, relative_path):
        """Get path to resource - works both in development and when bundled as exe"""
        if getattr(sys, 'frozen', False):
            # Running as exe
            base_path = sys._MEIPASS
        else:
            # Running as script
            base_path = os.path.dirname(os.path.abspath(__file__))
        
        return os.path.join(base_path, relative_path)
    
    def start_backend(self):
        """Start FastAPI backend server in a separate process"""
        try:
            backend_dir = self.get_resource_path('backend')
            
            if not os.path.exists(backend_dir):
                logger.error(f"Backend directory not found: {backend_dir}")
                return False
            
            # Instead of spawning a separate Python process (which extracts the
            # bundled exe again and can lock temporary files), start the Uvicorn
            # server programmatically in a background thread. This keeps everything
            # in-process and avoids multiple visible consoles and temp-dir locks.
            logger.info(f"Starting backend server from {backend_dir} (in-process)")

            # Ensure backend package path is importable
            if backend_dir not in sys.path:
                sys.path.insert(0, backend_dir)

            # Import the backend app module
            import importlib
            try:
                backend_main = importlib.import_module('main')
            except Exception:
                # try loading as package.backend.main if structure differs
                backend_main = importlib.import_module('backend.main')

            app_obj = getattr(backend_main, 'app')

            # Start uvicorn programmatically
            import uvicorn

            config = uvicorn.Config(app=app_obj, host='127.0.0.1', port=8000, log_level='info')
            server = uvicorn.Server(config=config)

            def run_server():
                try:
                    server.run()
                except Exception as e:
                    logger.error(f"Uvicorn server error: {e}")

            self.uvicorn_server = server
            self.uvicorn_thread = threading.Thread(target=run_server, daemon=True)
            self.uvicorn_thread.start()

            # Give the server time to start
            time.sleep(2)
            self.backend_ready = True
            logger.info("Backend server started (in-process)")
            return True
            
        except Exception as e:
            logger.error(f"Failed to start backend: {e}")
            return False
    
    def stop_backend(self):
        """Stop the backend server gracefully"""
        # If we started an in-process uvicorn server, request shutdown
        if self.uvicorn_server:
            try:
                logger.info("Stopping backend server...")
                # Signal the server to exit
                self.uvicorn_server.should_exit = True
                # Wait for thread to exit
                if self.uvicorn_thread and self.uvicorn_thread.is_alive():
                    self.uvicorn_thread.join(timeout=5)
                logger.info("Backend stopped successfully")
            except Exception as e:
                logger.error(f"Error stopping backend: {e}")
                try:
                    # Fallback: clear references
                    self.uvicorn_server = None
                except Exception:
                    pass
        elif self.backend_process:
            try:
                logger.info("Stopping backend server...")
                self.backend_process.terminate()
                self.backend_process.wait(timeout=5)
                logger.info("Backend stopped successfully")
            except subprocess.TimeoutExpired:
                logger.warning("Backend did not stop gracefully, killing process...")
                self.backend_process.kill()
            except Exception as e:
                logger.error(f"Error stopping backend: {e}")
    
    def start_frontend(self):
        """Start the Tkinter frontend application"""
        try:
            frontend_dir = self.get_resource_path('frontend')
            
            if not os.path.exists(frontend_dir):
                logger.error(f"Frontend directory not found: {frontend_dir}")
                return False
            
            logger.info(f"Starting frontend from {frontend_dir}")

            # Ensure frontend package path is importable so top-level imports like
            # `from pages import element_information` work when frozen.
            if frontend_dir not in sys.path:
                sys.path.insert(0, frontend_dir)

            # Import and run the frontend app using importlib to avoid resolution issues
            import importlib.util
            spec = importlib.util.spec_from_file_location("app", os.path.join(frontend_dir, "app.py"))
            app_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(app_module)

            # Call the main() function from the app module
            app_module.main()
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to start frontend: {e}")
            messagebox.showerror("Error", f"Failed to start frontend: {e}")
            return False
    
    def on_closing(self):
        """Handle application closing"""
        logger.info("Closing DAQ System...")
        self.is_running = False
        self.stop_backend()
        if self.root:
            self.root.quit()
    
    def run(self):
        """Main entry point - start backend and frontend"""
        logger.info("=" * 60)
        logger.info("DAQ System Starting")
        logger.info("=" * 60)
        
        # Start backend in a separate thread
        self.backend_thread = threading.Thread(target=self.start_backend, daemon=True)
        self.backend_thread.start()
        
        time.sleep(1)  # Give backend a moment to start
        
        if not self.backend_ready:
            logger.warning("Backend may not have started properly, but continuing...")
        
        # Start frontend (blocking call)
        try:
            self.start_frontend()
        except KeyboardInterrupt:
            logger.info("Interrupted by user")
        finally:
            self.on_closing()
        
        logger.info("DAQ System Stopped")


def main():
    """Entry point for the application"""
    launcher = DAQSystemLauncher()
    launcher.run()


if __name__ == "__main__":
    main()
