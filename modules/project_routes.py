import os
import yaml
import json
import logging
from datetime import datetime
from typing import Optional

logger = logging.getLogger(__name__)

def repair_project_config() -> None:
    """Repair the project.yaml configuration by adding missing fields and validating syntax."""
    project_file = 'project.yaml'
    backup_file = f'backup_{datetime.now().strftime("%Y%m%d%H%M%S")}_{project_file}'
    
    # Step 1: Create a backup
    try:
        with open(project_file, 'r') as original_file:
            with open(backup_file, 'w') as backup:
                backup.write(original_file.read())
        logger.info(f'Backup created: {backup_file}')
    except Exception as e:
        logger.error(f'Failed to create backup: {e}')
        return
    
    # Step 2: Load the existing configuration
    try:
        with open(project_file, 'r') as file:
            config = yaml.safe_load(file)
    except yaml.YAMLError as e:
        logger.error(f'YAML syntax error: {e}')
        return

    # Step 3: Validate and fix the configuration
    if 'template_version' not in config:
        logger.info('Adding missing template_version field.')
        try:
            with open('templates.json', 'r') as templates_file:
                templates = json.load(templates_file)
                config['template_version'] = templates.get('version', '1.0.0')  # Default version
        except (FileNotFoundError, json.JSONDecodeError):
            logger.warning('templates.json not found or invalid. Setting default version to 1.0.0.')
            config['template_version'] = '1.0.0'

    # Validate dependencies format and ensure all required fields are present
    if 'dependencies' not in config or not isinstance(config['dependencies'], list):
        config['dependencies'] = []  # Default to empty list if not present

    # Step 4: Save the fixed configuration back to project.yaml
    try:
        with open(project_file, 'w') as file:
            yaml.dump(config, file)
        logger.info('project.yaml has been successfully repaired.')
    except Exception as e:
        logger.error(f'Failed to save configuration: {e}')
        # Restore from backup if repair fails
        os.replace(backup_file, project_file)
        logger.info('Restored from backup due to failure.')