import os
import yaml
import shutil
from datetime import datetime
from typing import Optional
import logging

logger = logging.getLogger(__name__)

def repair_project_config() -> None:
    """Repairs the project.yaml configuration file by creating a backup, fixing issues, and restoring if needed."""
    yaml_file_path = 'project.yaml'
    backup_file_path = f'project_{datetime.now().strftime("%Y%m%d%H%M%S")}.yaml'

    # Step 1: Create a backup of project.yaml if it exists
    if os.path.exists(yaml_file_path):
        shutil.copy(yaml_file_path, backup_file_path)
        logger.info(f"Backup of '{yaml_file_path}' created at '{backup_file_path}'.")

    # Step 2: Prepare to fix the YAML configuration
    try:
        project_config = {}
        
        # Check if the YAML file exists
        if os.path.exists(yaml_file_path):
            with open(yaml_file_path, 'r') as file:
                project_config = yaml.safe_load(file) or {}

        # Step 3: Fix YAML syntax errors and add missing fields
        project_config.setdefault('template_version', '1.0')
        project_config.setdefault('dependencies', {})
        project_config['dependencies'] = {**project_config.get('dependencies', {}), 'default-package': 'latest'}

        # Step 4: Write back to project.yaml
        with open(yaml_file_path, 'w') as file:
            yaml.dump(project_config, file)
            logger.info(f"'{yaml_file_path}' has been updated successfully.")
    
    except Exception as e:
        logger.error(f"Error repairing '{yaml_file_path}': {str(e)}")
        # Step 5: Restore from backup if repair fails
        if os.path.exists(backup_file_path):
            shutil.copy(backup_file_path, yaml_file_path)
            logger.info(f"Restored '{yaml_file_path}' from backup.")
        raise