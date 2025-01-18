import os
import logging
import streamlit as st

def cleanup_log_file(log_file_path, max_lines=500):
    """
    Cleanup log file if it exceeds the maximum number of lines.
    
    Args:
        log_file_path (str): Path to the log file
        max_lines (int): Maximum number of lines to keep in the log file
    """
    try:
        # Check if log file exists
        if not os.path.exists(log_file_path):
            return

        # Read the log file
        with open(log_file_path, 'r') as log_file:
            lines = log_file.readlines()

        # If lines exceed max_lines, keep the last max_lines
        if len(lines) > max_lines:
            lines = lines[-max_lines:]

            # Write back the truncated lines
            with open(log_file_path, 'w') as log_file:
                log_file.writelines(lines)

    except Exception as e:
        print(f"Error cleaning up log file: {e}")

def setup_logging(module_name=None, max_log_lines=500):
    """
    Set up and configure logging for the application.
    
    Args:
        module_name (str, optional): Name of the module to create a logger for.
                                     If None, returns the root logger.
        max_log_lines (int, optional): Maximum number of lines to keep in log file
    
    Returns:
        logging.Logger: Configured logger instance
    """
    # Create logs directory if it doesn't exist
    logs_dir = st.secrets.get('LOGS_DIR', 'logs')
    os.makedirs(logs_dir, exist_ok=True)

    # Configure logging format
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    # Log file path
    log_file_path = os.path.join(logs_dir, 'etl_app.log')

    # Cleanup log file if it gets too large
    cleanup_log_file(log_file_path, max_log_lines)

    # Configure logging if not already configured
    if not logging.getLogger().handlers:
        logging.basicConfig(
            level=logging.INFO,
            format=log_format,
            handlers=[
                # Console handler
                logging.StreamHandler(),
                # File handler
                logging.FileHandler(log_file_path)
            ]
        )

    # Return logger for specific module or root logger
    return logging.getLogger(module_name) if module_name else logging.getLogger()