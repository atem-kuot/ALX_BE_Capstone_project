import logging

# Create a logger instance
logger = logging.getLogger('pharmacy')

def log_error(message, exc_info=None, extra=None):
    """Log an error message with optional exception info."""
    logger.error(message, exc_info=exc_info, extra=extra or {})

def log_info(message, extra=None):
    """Log an info message."""
    logger.info(message, extra=extra or {})

def log_warning(message, extra=None):
    """Log a warning message."""
    logger.warning(message, extra=extra or {})
