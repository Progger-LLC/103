import os
import shutil
import time
import yaml
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

def repair_project_config(config_file: str = 'project.yaml') -> None:
    """Repair project configuration by fixing YAML issues and adding missing fields."""
    
    # Step 1: Create a timestamped backup of project.yaml
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    backup_file = f"{config_file}.{timestamp}.bak"
    shutil.copyfile(config_file, backup_file)
    logger.info(f"Backup created: {backup_file}")

    # Step 2: Load the current configuration
    try:
        with open(config_file, 'r') as f:
            config: Dict[str, Any] = yaml.safe_load(f) or {}
    except Exception as e:
        logger.error(f"Failed to load {config_file}: {e}")
        return

    # Step 3: Add missing required fields with sensible defaults
    if 'template_version' not in config:
        config['template_version'] = '1.0.0'  # Default version

    # Additional checks for other required fields can be added here

    # Step 4: Save the modified configuration back to project.yaml
    try:
        with open(config_file, 'w') as f:
            yaml.safe_dump(config, f)
        logger.info(f"Configuration updated and saved to {config_file}")
    except Exception as e:
        logger.error(f"Failed to save {config_file}: {e}")
        # Restore from backup if save fails
        shutil.copyfile(backup_file, config_file)
        logger.info(f"Restored backup from {backup_file} to {config_file}")