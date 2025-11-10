import os
import yaml
import logging
from datetime import datetime
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)

def repair_project_config(file_path: str) -> bool:
    """
    Repair the project.yaml configuration file by ensuring it is valid YAML
    and contains all required fields.

    Args:
        file_path (str): Path to the project.yaml file.

    Returns:
        bool: True if the repair was successful, False otherwise.
    """
    # Step 1: Create a timestamped backup
    backup_path = f"{file_path}.{datetime.now().strftime('%Y%m%d%H%M%S')}.bak"
    try:
        with open(file_path, 'r') as original_file:
            with open(backup_path, 'w') as backup_file:
                backup_file.write(original_file.read())
        logger.info(f"Backup created at {backup_path}")
    except Exception as e:
        logger.error(f"Failed to create backup: {e}")
        return False

    # Step 2: Attempt to read and repair the YAML file
    try:
        with open(file_path, 'r') as f:
            config = yaml.safe_load(f)

        if not isinstance(config, dict):
            logger.error("YAML file does not load as a dictionary.")
            return restore_backup(file_path, backup_path)

        # Step 3: Add missing required fields
        if 'template_version' not in config:
            config['template_version'] = "1.0"  # Set a sensible default
            logger.info("Added missing 'template_version' field.")

        # Step 4: Validate and write back the YAML
        with open(file_path, 'w') as f:
            yaml.safe_dump(config, f)

    except Exception as e:
        logger.error(f"Failed to repair project.yaml: {e}")
        return restore_backup(file_path, backup_path)
    
    logger.info("project.yaml successfully repaired.")
    return True

def restore_backup(file_path: str, backup_path: str) -> bool:
    """
    Restore the project.yaml file from a backup.

    Args:
        file_path (str): Path to the project.yaml file.
        backup_path (str): Path to the backup file.

    Returns:
        bool: True if restore was successful, False otherwise.
    """
    try:
        os.remove(file_path)  # Remove the corrupted file
        os.rename(backup_path, file_path)  # Restore from backup
        logger.info(f"Restored project.yaml from {backup_path}")
    except Exception as e:
        logger.error(f"Failed to restore backup: {e}")
        return False
    return True