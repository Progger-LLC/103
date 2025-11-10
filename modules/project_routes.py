import os
import shutil
import yaml
from datetime import datetime
from typing import Any, Dict, Optional
import logging

logger = logging.getLogger(__name__)

def repair_project_config(project_yaml_path: str, templates_json_path: str) -> None:
    """Repair the project.yaml configuration file."""
    
    # Step 1: Backup the existing project.yaml
    backup_path = f"{project_yaml_path}.{datetime.now().strftime('%Y%m%d%H%M%S')}.bak"
    shutil.copy(project_yaml_path, backup_path)
    logger.info(f"Backup created at {backup_path}")

    try:
        # Step 2: Load the existing YAML
        with open(project_yaml_path, 'r') as file:
            config = yaml.safe_load(file) or {}
        
        # Step 3: Check for required fields and add defaults
        if 'template_version' not in config:
            # Infer from templates.json if available
            template_version = infer_template_version(templates_json_path)
            config['template_version'] = template_version

        # Additional checks can be performed here for other required fields
        
        # Step 4: Save the fixed configuration back to project.yaml
        with open(project_yaml_path, 'w') as file:
            yaml.safe_dump(config, file)
        logger.info(f"project.yaml repaired successfully.")
    
    except Exception as e:
        # Step 5: Restore from backup if there is an error
        shutil.copy(backup_path, project_yaml_path)
        logger.error(f"Repair failed. Restored from backup. Error: {e}")

def infer_template_version(templates_json_path: str) -> Optional[str]:
    """Infer the template version from the templates.json file."""
    try:
        with open(templates_json_path, 'r') as file:
            templates = json.load(file)
            return templates.get('template_version')
    except Exception as e:
        logger.error(f"Could not infer template version: {e}")
        return None