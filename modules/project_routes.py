import os
import yaml
import json
import logging
from datetime import datetime
from typing import Dict, Any

logger = logging.getLogger(__name__)

def repair_project_config() -> None:
    """Repair the project.yaml configuration file."""
    project_yaml_path = 'project.yaml'
    backup_path = f'project.yaml.bak.{datetime.now().strftime("%Y%m%d%H%M%S")}'
    
    if not os.path.exists(project_yaml_path):
        logger.error("project.yaml file not found.")
        return
    
    # Step 1: Create a backup of project.yaml
    os.rename(project_yaml_path, backup_path)
    logger.info(f"Backup created at {backup_path}")

    try:
        # Step 2: Load the existing YAML file
        with open(backup_path, 'r') as file:
            config = yaml.safe_load(file) or {}

        # Step 3: Fix YAML syntax errors and add missing required fields
        required_fields = ['template_version', 'dependencies']
        for field in required_fields:
            if field not in config:
                if field == 'template_version':
                    config[field] = infer_template_version()
                elif field == 'dependencies':
                    config[field] = {}

        # Step 4: Validate dependencies
        if 'dependencies' in config and not isinstance(config['dependencies'], dict):
            logger.error("Dependencies should be a dictionary.")
            raise ValueError("Dependencies should be a dictionary.")

        # Step 5: Write the fixed configuration back to project.yaml
        with open(project_yaml_path, 'w') as file:
            yaml.dump(config, file)
        logger.info("project.yaml successfully repaired.")

    except Exception as e:
        logger.exception("An error occurred while repairing project.yaml. Restoring from backup.")
        os.rename(backup_path, project_yaml_path)  # Restore from backup
        raise e  # re-raise for visibility

def infer_template_version() -> str:
    """Infer the template version from templates.json if available."""
    templates_path = 'templates.json'
    if os.path.exists(templates_path):
        with open(templates_path, 'r') as file:
            templates = json.load(file)
            return templates.get('latest_version', '1.0.0')  # Default version if not found
    return '1.0.0'  # Default version if templates.json does not exist