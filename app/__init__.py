from flask import Flask
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from loguru import logger

from app.database.connection import init_db
from app.utils.db import save_db_for_utils
from app.utils.logger import setup_logger
from app.routes import index, text_processing, history

setup_logger()
app_logger = logger.bind(name="app")

def app_init() -> Flask:
    """
    Initialize Flask application with database connection
    
    Returns:
        Flask: Configured Flask application
        
    Raises:
        ConnectionFailure: If database connection fails
        ValueError: If configuration is invalid
    """
    app_logger.info("Starting Flask application initialization...")
    
    app = Flask(__name__)
    
    try:
        app_logger.info("Initializing database connection...")
        mongo_client: MongoClient = init_db(app)
        save_db_for_utils(mongo_client)
        
        app.register_blueprint(index.bp)
        app.register_blueprint(text_processing.bp)
        app.register_blueprint(history.bp)
    except (ConnectionFailure, ValueError) as e:
        app_logger.error(f"Failed to initialize database: {e}")
        raise
    except Exception as e:
        app_logger.critical(f"Unexpected error during app initialization: {e}")
        raise
    
    
    app_logger.success("Flask application initialized successfully")
    return app