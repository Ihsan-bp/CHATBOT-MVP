import logging


def setup_logging():
    """
    Setup the logging configuration for the application.

    Configures the logging to log INFO level messages or higher, with a 
    specific format including timestamp, logger name, and log level. 
    Logs are written to both a file ('app.log') and the console (stream handler).
    """
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler("app.log"),
            logging.StreamHandler(),
        ],
    )


def get_logger(name):
    """
    Get a logger with the specified name.

    Args:
        name (str): The name of the logger, usually the module name.

    Returns:
        logging.Logger: The logger object for the specified name.
    """
    return logging.getLogger(name)