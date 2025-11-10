import os
import shutil
import yaml
from datetime import datetime
from modules.project_routes import repair_project_config
import logging

logger = logging.getLogger(__name__)

def fix_project_yaml(file_path: str, templates_file: str) -> None:
    """Fix the project.yaml configuration issues."""
    # Step 1: Create a backup of project.yaml
    backup_path = f"{file_path}.{datetime.now().strftime('%Y%m%d%H%M%S')}.bak"
    shutil.copy(file_path, backup_path)
    logger.info(f"Backup created at {backup_path}")

    try:
        # Step 2: Use the existing repair function to fix the project.yaml
        repair_project_config(file_path, templates_file)

        # Step 3: Validate the repaired YAML
        with open(file_path, 'r') as f:
            yaml.safe_load(f)  # This will raise an error if the YAML is invalid
            
        logger.info(f"{file_path} has been repaired successfully.")
    
    except Exception as e:
        logger.error(f"Repair failed: {e}. Restoring from backup.")
        shutil.copy(backup_path, file_path)  # Restore from backup
        logger.info(f"{file_path} restored from {backup_path}")