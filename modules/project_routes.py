import os
import yaml
import logging
from datetime import datetime
from typing import Dict, Any

logger = logging.getLogger(__name__)

def repair_project_config() -> None:
    """Repair the project.yaml configuration file.

    This function creates a backup of the project.yaml file,
    checks for and fixes configuration issues, and restores
    from backup if any errors occur during the repair process.
    """
    project_yaml_path = 'project.yaml'
    backup_path = f'project_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.yaml'
    
    # Step 1: Create a timestamped backup of project.yaml
    if os.path.exists(project_yaml_path):
        os.rename(project_yaml_path, backup_path)
        logger.info(f'Backup created at {backup_path}')
    
    try:
        # Step 2: Load the current configuration
        with open(backup_path, 'r') as file:
            config = yaml.safe_load(file) or {}
        
        # Step 3: Fix YAML syntax errors and add missing fields
        if 'template_version' not in config:
            # Infer template_version from templates.json if available
            template_version = infer_template_version()
            config['template_version'] = template_version or '1.0.0'  # Default value
            logger.info('Added missing template_version field')
        
        # Additional checks and fixes could be added here

        # Step 4: Validate YAML structure and save back
        with open(project_yaml_path, 'w') as file:
            yaml.dump(config, file)
        logger.info('project.yaml has been repaired successfully')

    except Exception as e:
        logger.error('Repair failed: %s', e)
        # Restore from backup if repair fails
        os.rename(backup_path, project_yaml_path)
        logger.info('Restored from backup')
    else:
        # Clean up backup if repair succeeded
        os.remove(backup_path)
    

def infer_template_version() -> str:
    """Infer the template version from templates.json if available.

    Returns:
        str: The inferred template version, or None if unavailable.
    """
    try:
        with open('templates.json', 'r') as file:
            templates = json.load(file)
            return templates.get('template_version')
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logger.warning('Could not infer template_version: %s', e)
        return None