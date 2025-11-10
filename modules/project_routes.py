import os
import shutil
import yaml
from datetime import datetime
from typing import Dict, Any
from src.exceptions import ConfigurationError
import logging

logger = logging.getLogger(__name__)

def repair_project_config() -> None:
    """Repair the project.yaml configuration file."""
    project_config_path = "project.yaml"
    backup_path = f"backup/project_{datetime.now().strftime('%Y%m%d_%H%M%S')}.yaml"

    # Step 1: Create a backup of project.yaml
    os.makedirs(os.path.dirname(backup_path), exist_ok=True)
    shutil.copy(project_config_path, backup_path)
    logger.info(f"Backup created at {backup_path}")

    try:
        with open(project_config_path, 'r') as file:
            config = yaml.safe_load(file)

        # Step 2: Fix YAML syntax errors (if any)
        if not isinstance(config, dict):
            raise ConfigurationError("YAML structure is not a valid dictionary.")

        # Step 3: Ensure required fields are present
        if 'template_version' not in config:
            config['template_version'] = "1.0.0"  # Default value
            logger.info("Added missing 'template_version' with default value.")

        # Additional sensible defaults can be added here

        # Step 4: Validate dependencies formatting (if applicable)
        if 'dependencies' in config and not isinstance(config['dependencies'], list):
            raise ConfigurationError("Dependencies must be a list.")

        # Step 5: Write the fixed configuration back to project.yaml
        with open(project_config_path, 'w') as file:
            yaml.dump(config, file)
        logger.info("Successfully repaired project.yaml")

    except Exception as e:
        logger.error(f"Repairing project.yaml failed: {e}. Restoring from backup.")
        shutil.copy(backup_path, project_config_path)
        raise ConfigurationError("Failed to repair project.yaml, restored from backup.")