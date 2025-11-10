import os
import shutil
import yaml
from typing import Dict, Any, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

def repair_project_config() -> None:
    """Repair the project.yaml configuration file."""
    project_yaml_path = 'project.yaml'
    backup_path = f'backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}_{project_yaml_path}'
    
    # Step 1: Backup project.yaml
    shutil.copyfile(project_yaml_path, backup_path)
    logger.info(f'Backup created: {backup_path}')
    
    try:
        # Step 2: Load the existing YAML
        with open(project_yaml_path, 'r') as file:
            data = yaml.safe_load(file) or {}
        
        # Step 3: Fix YAML syntax errors (if any)
        # Step 4: Add missing required fields
        if 'template_version' not in data:
            logger.warning('template_version field is missing. Adding default.')
            data['template_version'] = '1.0.0'  # Default value
        
        # You can add further checks and fixes here if needed.

        # Step 5: Write the updated YAML back to file
        with open(project_yaml_path, 'w') as file:
            yaml.dump(data, file)
        
        logger.info('project.yaml configuration repaired successfully.')
    
    except Exception as e:
        logger.error(f'Error during repair: {e}. Restoring from backup.')
        shutil.copyfile(backup_path, project_yaml_path)  # Restore from backup
        logger.info('Restored project.yaml from backup.')