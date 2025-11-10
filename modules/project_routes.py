import os
import shutil
import yaml
from typing import Optional, Dict

def repair_project_config() -> None:
    """Repair project.yaml configuration issues."""
    project_yaml_path = 'project.yaml'
    backup_path = f'project_backup_{int(time.time())}.yaml'
    
    # Step 1: Create a backup of project.yaml
    shutil.copyfile(project_yaml_path, backup_path)

    try:
        # Step 2: Load the existing project.yaml
        with open(project_yaml_path, 'r') as file:
            config = yaml.safe_load(file)

        # Step 3: Validate YAML and add missing fields
        if 'template_version' not in config:
            config['template_version'] = '1.0.0'  # Default value

        # Validate other required fields
        required_fields = ['entry_point', 'dependencies']
        for field in required_fields:
            if field not in config:
                config[field] = [] if field == 'dependencies' else ''

        # Step 4: Save the updated project.yaml
        with open(project_yaml_path, 'w') as file:
            yaml.dump(config, file)

    except Exception as e:
        # Step 5: Restore from backup if there is an error
        shutil.copyfile(backup_path, project_yaml_path)
        logger.error(f"Failed to repair project.yaml: {e}")
        raise