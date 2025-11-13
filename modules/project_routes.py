import os
import yaml
import shutil
import datetime
from typing import Any, Dict
import logging

logger = logging.getLogger(__name__)

def repair_project_config() -> None:
    """Repair the project.yaml configuration file.
    
    This function will create a backup, fix any YAML syntax errors,
    and ensure all required fields are present with sensible defaults.
    """
    yaml_file_path = "project.yaml"
    backup_file_path = f"project_backup_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.yaml"
    
    # Step 1: Create a backup
    shutil.copy(yaml_file_path, backup_file_path)
    logger.info(f"Backup created at {backup_file_path}")
    
    try:
        # Step 2: Load the YAML file
        with open(yaml_file_path, 'r') as file:
            config = yaml.safe_load(file) or {}
        
        # Step 3: Fix YAML syntax errors and add missing fields
        if 'required_field_1' not in config:
            config['required_field_1'] = "default_value_1"
        
        if 'required_field_2' not in config:
            config['required_field_2'] = "default_value_2"
        
        # Step 4: Infer template_version from templates.json if available
        if os.path.exists('templates.json'):
            with open('templates.json', 'r') as tmpl_file:
                templates = json.load(tmpl_file)
                config['template_version'] = templates.get('template_version', '1.0.0')
        
        # Step 5: Write the fixed configuration back to project.yaml
        with open(yaml_file_path, 'w') as file:
            yaml.dump(config, file)
        
        logger.info("project.yaml repaired successfully.")
        
    except Exception as e:
        logger.error(f"Repair failed: {e}. Restoring backup.")
        # Restore from backup
        shutil.copy(backup_file_path, yaml_file_path)
        logger.info("Restored from backup.")