import os
import yaml
import datetime
from typing import Dict, Any
import shutil
import logging

logger = logging.getLogger(__name__)

def repair_project_config(file_path: str) -> None:
    """Repair the project configuration in the specified YAML file.
    
    This function creates a backup of the YAML file, fixes any configuration 
    issues, and ensures all required fields are present.

    Args:
        file_path (str): Path to the project.yaml file.

    Raises:
        Exception: If the repair fails, raises an exception.
    """
    # Step 1: Create a timestamped backup
    backup_file_path = f"{file_path}.{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.bak"
    shutil.copyfile(file_path, backup_file_path)
    logger.info(f"Backup created at {backup_file_path}")

    try:
        # Step 2: Load the current configuration
        with open(file_path, 'r') as file:
            config = yaml.safe_load(file)

        # Step 3: Check for missing required fields
        if 'template_version' not in config:
            config['template_version'] = '1.0.0'  # Set a default version
            logger.info("Added missing field 'template_version' with default value.")

        # Step 4: Validate dependencies formatting (example validation)
        if 'dependencies' in config and not isinstance(config['dependencies'], dict):
            raise ValueError("Dependencies must be a dictionary.")

        # Step 5: Save the updated configuration
        with open(file_path, 'w') as file:
            yaml.dump(config, file)
        logger.info("Project configuration updated successfully.")

    except Exception as e:
        logger.error(f"Repair failed: {e}. Restoring from backup.")
        shutil.copyfile(backup_file_path, file_path)
        logger.info("Restored original configuration from backup.")
        raise