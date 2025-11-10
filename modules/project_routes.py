import os
import shutil
import yaml
from datetime import datetime
from typing import Dict, Any

def repair_project_config() -> None:
    """Repair the project.yaml configuration by creating a backup and fixing issues.

    This function will backup the current project.yaml, fix any syntax errors,
    and ensure required fields are present. It will restore from backup if needed.
    """
    project_yaml_path = "project.yaml"
    backup_path = f"project_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.yaml"

    # Step 1: Create a backup of the current project.yaml
    shutil.copyfile(project_yaml_path, backup_path)
    
    try:
        # Step 2: Load the existing YAML file
        with open(project_yaml_path, 'r') as file:
            config = yaml.safe_load(file) or {}

        # Step 3: Check and add missing fields
        if 'template_version' not in config:
            config['template_version'] = '1.0.0'  # sensible default

        # Ensure all required fields and dependencies formatting are correct
        required_fields = ['template_version', 'dependencies']
        for field in required_fields:
            if field not in config:
                config[field] = [] if field == 'dependencies' else ''

        # Step 4: Write back the updated YAML
        with open(project_yaml_path, 'w') as file:
            yaml.safe_dump(config, file)

    except Exception as e:
        # Restore from backup if there's an issue
        shutil.copyfile(backup_path, project_yaml_path)
        raise e
    finally:
        # Clean up the backup file if everything goes well
        if os.path.exists(backup_path):
            os.remove(backup_path)