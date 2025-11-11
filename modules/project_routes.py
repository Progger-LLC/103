import os
import shutil
import yaml
import logging
from datetime import datetime
from typing import Dict, Any

logger = logging.getLogger(__name__)

def repair_project_config() -> None:
    """Repair the project.yaml configuration file."""
    config_file = 'project.yaml'
    backup_file = f'backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}_{config_file}'
    
    # Check if project.yaml exists
    if not os.path.exists(config_file):
        logger.error(f"{config_file} not found.")
        return
    
    # Create a backup before making changes
    shutil.copyfile(config_file, backup_file)
    logger.info(f"Backup created: {backup_file}")

    try:
        with open(config_file, 'r') as file:
            config = yaml.safe_load(file)
        
        # Fix YAML syntax errors if necessary
        if not isinstance(config, dict):
            logger.warning("Invalid configuration structure detected. Initializing defaults.")
            config = {}

        # Add missing required fields
        required_fields = {
            'template_version': '1.0',
            'dependencies': {}
        }

        for key, value in required_fields.items():
            if key not in config:
                config[key] = value

        # Load template version from templates.json if available
        if os.path.exists('templates.json'):
            with open('templates.json', 'r') as templates_file:
                templates = yaml.safe_load(templates_file)
                if 'template_version' in templates:
                    config['template_version'] = templates['template_version']
        
        # Save the modified configuration back to project.yaml
        with open(config_file, 'w') as file:
            yaml.dump(config, file)
        
        logger.info(f"{config_file} has been updated successfully.")
    
    except Exception as e:
        logger.error(f"Error during repair: {str(e)}. Restoring backup.")
        shutil.copyfile(backup_file, config_file)
        logger.info(f"Restored from backup: {backup_file}")