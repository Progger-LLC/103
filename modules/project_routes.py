import os
import shutil
import yaml
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

def repair_project_config(file_path: str) -> None:
    """Repair project.yaml configuration issues.

    Args:
        file_path (str): The path to the project.yaml file.

    Raises:
        Exception: If the repair process fails.
    """
    backup_path = f"{file_path}.{int(os.path.getmtime(file_path))}.bak"
    try:
        # Step 1: Create a backup
        shutil.copy(file_path, backup_path)
        logger.info(f"Backup created at {backup_path}")

        with open(file_path, 'r') as file:
            config = yaml.safe_load(file) or {}

        # Step 2: Validate and fix the configuration
        if 'template_version' not in config:
            # Step 3: Add missing required fields with sensible defaults
            config['template_version'] = '1.0.0'
            logger.info("Added missing 'template_version' field.")

        # Step 4: Validate YAML syntax
        validate_yaml(config)

        # Step 5: Write the fixed configuration back to the file
        with open(file_path, 'w') as file:
            yaml.safe_dump(config, file)

        logger.info("project.yaml has been repaired successfully.")
    
    except Exception as e:
        logger.error(f"Repair failed: {e}. Restoring from backup.")
        if os.path.exists(backup_path):
            shutil.copy(backup_path, file_path)
            logger.info("Restored from backup.")
        raise

def validate_yaml(config: Dict[str, Any]) -> None:
    """Validate YAML configuration.

    Args:
        config (Dict[str, Any]): The configuration dictionary.

    Raises:
        ValueError: If the configuration is invalid.
    """
    # Example validation logic (add more checks as needed)
    if 'dependencies' not in config or not isinstance(config['dependencies'], dict):
        raise ValueError("Invalid dependencies format in project.yaml.")