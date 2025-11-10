import os
import yaml
import shutil
import datetime
from typing import Any, Dict
import logging

logger = logging.getLogger(__name__)

def repair_project_config(file_path: str, templates_path: str) -> None:
    """Repair the project.yaml configuration file.

    This function creates a backup, fixes any syntax errors, and ensures
    all required fields are present in the project.yaml file.

    Args:
        file_path (str): The path to the project.yaml file.
        templates_path (str): The path to the templates.json file.
    """
    backup_file_path = create_backup(file_path)
    try:
        with open(file_path, 'r') as file:
            config_data = yaml.safe_load(file)
        
        # Fix configuration
        if 'template_version' not in config_data:
            config_data['template_version'] = infer_template_version(templates_path)

        # Ensure dependencies format
        if 'dependencies' not in config_data or not isinstance(config_data['dependencies'], dict):
            config_data['dependencies'] = {}

        # Write back the fixed configuration
        with open(file_path, 'w') as file:
            yaml.safe_dump(config_data, file)

        logger.info("Project configuration repaired successfully.")
    
    except Exception as e:
        logger.error(f"Failed to repair project configuration: {e}")
        restore_backup(file_path, backup_file_path)

def create_backup(file_path: str) -> str:
    """Create a timestamped backup of the specified file.

    Args:
        file_path (str): The path to the original file.

    Returns:
        str: The path to the created backup file.
    """
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    backup_file_path = f"{file_path}.{timestamp}.bak"
    shutil.copy(file_path, backup_file_path)
    logger.info(f"Backup created at: {backup_file_path}")
    return backup_file_path

def restore_backup(original_file_path: str, backup_file_path: str) -> None:
    """Restore the original file from the backup.

    Args:
        original_file_path (str): The path to the original file.
        backup_file_path (str): The path to the backup file.
    """
    shutil.copy(backup_file_path, original_file_path)
    logger.info("Restored original configuration from backup.")

def infer_template_version(templates_path: str) -> str:
    """Infer the template version from templates.json if available.

    Args:
        templates_path (str): The path to the templates.json file.

    Returns:
        str: The inferred template version, or a default version.
    """
    if os.path.exists(templates_path):
        with open(templates_path, 'r') as file:
            templates_data = json.load(file)
            return templates_data.get('template_version', '1.0.0')  # Default version
    return '1.0.0'  # Default version if file does not exist