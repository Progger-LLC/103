import yaml
import os
import shutil
import logging
from datetime import datetime
from typing import Optional

logger = logging.getLogger(__name__)

def repair_project_config(file_path: str) -> None:
    """Repair project.yaml configuration issues."""
    # Create a backup of the original project.yaml
    backup_file = f"{file_path}.{datetime.now().strftime('%Y%m%d%H%M%S')}.bak"
    shutil.copy(file_path, backup_file)
    logger.info(f"Backup created at {backup_file}")

    try:
        with open(file_path, 'r') as file:
            config = yaml.safe_load(file)

        # Ensure template_version is present
        if 'template_version' not in config:
            config['template_version'] = "1.0.0"  # Set a sensible default
            logger.info("Added missing field: template_version")

        # Additional validation and formatting can be added here
        # For example, ensuring dependencies are properly formatted

        # Write the updated configuration back to project.yaml
        with open(file_path, 'w') as file:
            yaml.dump(config, file)
            logger.info("Successfully updated project.yaml")

    except Exception as e:
        # Restore from backup if repair fails
        shutil.copy(backup_file, file_path)
        logger.error(f"Repair failed, restored from backup: {e}")