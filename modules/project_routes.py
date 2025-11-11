import os
import yaml
import json
import logging
from datetime import datetime
from typing import Dict

logger = logging.getLogger(__name__)

def repair_project_config() -> None:
    """Repair the project.yaml configuration file by ensuring it is valid and complete."""
    project_yaml_path = 'project.yaml'
    backup_yaml_path = f'project_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.yaml'
    
    # Create a backup of the existing project.yaml if it exists
    if os.path.exists(project_yaml_path):
        os.rename(project_yaml_path, backup_yaml_path)
        logger.info(f"Backup created: {backup_yaml_path}")

    # Create default project.yaml structure
    project_config = {
        'template_version': None,  # Will fill this in later
        'dependencies': {
            'web_framework': 'fastapi==0.104.1',
            'database': 'sqlalchemy==2.0.23',
            'testing': 'pytest==7.4.3'
        }
    }
    
    # Attempt to infer template_version from templates.json
    if os.path.exists('templates.json'):
        with open('templates.json', 'r') as templates_file:
            templates = json.load(templates_file)
            project_config['template_version'] = templates.get('version', '1.0.0')

    # Write the validated configuration back to project.yaml
    with open(project_yaml_path, 'w') as yaml_file:
        yaml.dump(project_config, yaml_file, default_flow_style=False)

    logger.info("project.yaml has been repaired and updated.")