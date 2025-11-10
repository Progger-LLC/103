import os
import shutil
import yaml
from datetime import datetime
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

def repair_project_config() -> None:
    """Repair the project.yaml configuration issues."""
    project_config_path = 'project.yaml'
    
    # Step 1: Create a timestamped backup of project.yaml
    backup_path = create_backup(project_config_path)
    
    try:
        # Step 2: Load the YAML file
        with open(project_config_path, 'r') as file:
            config = yaml.safe_load(file) or {}
        
        # Step 3: Validate and fix the configuration
        if 'template_version' not in config:
            config['template_version'] = "1.0.0"  # Default version
        
        # Check if dependencies are properly formatted
        if 'dependencies' not in config or not isinstance(config['dependencies'], dict):
            config['dependencies'] = {}
        
        # Step 4: Save the updated configuration back to project.yaml
        with open(project_config_path, 'w') as file:
            yaml.dump(config, file)
        
        logger.info("Successfully repaired project.yaml")
        
    except Exception as e:
        logger.error(f"Error repairing project.yaml: {e}")
        restore_backup(backup_path, project_config_path)
        logger.info("Restored project.yaml from backup.")
        raise

def create_backup(original_file: str) -> str:
    """Create a backup of the original YAML file."""
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    backup_file = f"{original_file}.{timestamp}.backup"
    shutil.copy2(original_file, backup_file)
    logger.info(f"Backup created: {backup_file}")
    return backup_file

def restore_backup(backup_file: str, original_file: str) -> None:
    """Restore the original file from a backup."""
    shutil.copy2(backup_file, original_file)
    logger.info(f"Restored {original_file} from {backup_file}")