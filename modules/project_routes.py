import os
import shutil
import yaml
from datetime import datetime
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

def repair_project_config() -> None:
    """Repair the project.yaml configuration file."""
    
    config_path = "project.yaml"
    
    # Step 1: Create a timestamped backup of project.yaml
    backup_path = f"project_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.yaml"
    shutil.copyfile(config_path, backup_path)
    logger.info(f"Backup created at {backup_path}")
    
    try:
        # Step 2: Load existing configuration
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file) or {}

        # Step 3: Validate and fix YAML
        if 'template_version' not in config:
            config['template_version'] = "1.0.0"  # Default version

        # Additional validation for dependencies
        if 'dependencies' not in config:
            config['dependencies'] = {}

        # Step 4: Save the fixed configuration
        with open(config_path, 'w') as file:
            yaml.dump(config, file)
        logger.info("project.yaml has been repaired and saved successfully.")

    except Exception as e:
        logger.error("Repair failed, restoring from backup.", exc_info=e)
        shutil.copyfile(backup_path, config_path)
        logger.info(f"Restored from backup: {backup_path}")