import os
import shutil
import yaml
from datetime import datetime
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

def repair_project_config() -> None:
    """Repair the project.yaml configuration file."""
    yaml_file_path = 'project.yaml'
    backup_file_path = f'project_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.yaml'
    
    # Step 1: Create a backup of project.yaml
    shutil.copy(yaml_file_path, backup_file_path)
    logger.info(f'Created backup of project.yaml at {backup_file_path}')

    try:
        # Step 2: Load the existing YAML
        with open(yaml_file_path, 'r') as file:
            config = yaml.safe_load(file) or {}

        # Step 3: Validate and repair the configuration
        if 'template_version' not in config:
            config['template_version'] = "1.0"  # Default version if not present
            logger.info('Added missing template_version field with default value.')

        # Ensure other required fields are present
        required_fields = ['entry_point', 'dependencies']
        for field in required_fields:
            if field not in config:
                config[field] = [] if field == 'dependencies' else ""
                logger.info(f'Added missing field: {field}.')

        # Step 4: Validate the dependencies format
        dependencies = config.get('dependencies', [])
        if not isinstance(dependencies, list):
            raise ValueError('Dependencies must be a list.')

        # Step 5: Save the repaired YAML
        with open(yaml_file_path, 'w') as file:
            yaml.dump(config, file)
        logger.info('Successfully repaired project.yaml.')

    except Exception as e:
        logger.error(f'Error occurred while repairing project.yaml: {e}')
        # Restore from backup if error occurs
        shutil.copy(backup_file_path, yaml_file_path)
        logger.info('Restored project.yaml from backup.')