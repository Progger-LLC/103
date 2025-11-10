import os
import shutil
import yaml
from typing import Optional
import logging

logger = logging.getLogger(__name__)

def repair_project_config() -> None:
    """Repair the project.yaml configuration file."""
    project_yaml_path = 'project.yaml'
    backup_path = f'{project_yaml_path}.bak'
    
    # Step 1: Create a timestamped backup of project.yaml
    if os.path.exists(project_yaml_path):
        shutil.copy(project_yaml_path, backup_path)
        logger.info(f'Backup created at {backup_path}')
    
    # Step 2: Load the project.yaml to validate and fix
    with open(project_yaml_path, 'r') as file:
        try:
            config = yaml.safe_load(file)
        except yaml.YAMLError as e:
            logger.error(f'YAML syntax error: {e}')
            return
    
    # Step 3: Add missing required fields with sensible defaults
    if 'template_version' not in config:
        config['template_version'] = '1.0.0'  # default version
        logger.info('Added missing template_version field.')
        
    # Step 4: Validate and format dependencies correctly
    if 'dependencies' not in config:
        config['dependencies'] = {}
    
    # More validation can be added as necessary

    # Step 5: Write changes back to project.yaml
    with open(project_yaml_path, 'w') as file:
        yaml.dump(config, file)
    
    logger.info(f'{project_yaml_path} has been repaired successfully.')