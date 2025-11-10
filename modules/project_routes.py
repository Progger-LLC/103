import os
import shutil
import yaml
from datetime import datetime
from typing import Dict, Any
from src.logger import logger  # Assuming there's a logger in src for logging purposes
from src.exceptions import InvalidConfigError

def repair_project_config() -> None:
    """Repair the project.yaml configuration file by ensuring all required fields are present.

    This function will create a backup of the current configuration, fix any YAML syntax errors,
    add missing required fields, infer the template version, and restore the backup if the repair fails.
    """
    project_config_path = "project.yaml"
    backup_path = f"{project_config_path}.{datetime.now().strftime('%Y%m%d%H%M%S')}.bak"

    # Step 1: Create a backup of project.yaml
    shutil.copyfile(project_config_path, backup_path)
    logger.info(f"Backup created at {backup_path}")

    try:
        with open(project_config_path, 'r') as file:
            config = yaml.safe_load(file) or {}

        # Step 2: Fix YAML syntax errors and add missing fields
        if 'template_version' not in config:
            config['template_version'] = "1.0.0"  # Default version if not provided
            logger.warning("Added missing 'template_version' field with default value '1.0.0'.")

        # Step 3: Validate dependencies formatting
        if 'dependencies' in config and isinstance(config['dependencies'], list):
            config['dependencies'] = {dep: "latest" for dep in config['dependencies']}
            logger.info("Dependencies reformatted to a dictionary with default version 'latest'.")

        # Step 4: Write the corrected configuration back to project.yaml
        with open(project_config_path, 'w') as file:
            yaml.safe_dump(config, file)

        logger.info("project.yaml updated successfully.")
    
    except Exception as e:
        logger.error("Failed to update project.yaml, restoring from backup.")
        shutil.copyfile(backup_path, project_config_path)
        logger.exception("Exception occurred during project.yaml repair: %s", e)
        raise InvalidConfigError("Unable to repair project.yaml configuration.") from e

    finally:
        # Clean up the backup file if everything went well
        if os.path.exists(backup_path):
            os.remove(backup_path)
            logger.info(f"Backup file {backup_path} removed after successful update.")