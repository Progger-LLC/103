import os
import shutil
import yaml
from typing import Optional
import logging

logger = logging.getLogger(__name__)

def repair_project_config() -> None:
    """Repair project.yaml configuration issues."""
    project_yaml_path = 'project.yaml'
    backup_yaml_path = f'project.yaml.bak'
    
    # Step 1: Create a backup of project.yaml
    shutil.copyfile(project_yaml_path, backup_yaml_path)
    
    try:
        # Step 2: Load project.yaml
        with open(project_yaml_path, 'r') as file:
            config = yaml.safe_load(file) or {}

        # Step 3: Check for required fields and fix YAML syntax errors
        if 'template_version' not in config:
            # Step 4: Infer template_version from templates.json if available
            template_version = get_template_version()
            if template_version:
                config['template_version'] = template_version
            else:
                config['template_version'] = '1.0.0'  # Default version

        # Additional required fields could be checked and added here
        if 'dependencies' not in config:
            config['dependencies'] = {}

        # Step 5: Save the repaired configuration back to project.yaml
        with open(project_yaml_path, 'w') as file:
            yaml.dump(config, file)

    except Exception as e:
        logger.error("Failed to repair project.yaml: %s", str(e))
        # Restore from backup if repair fails
        shutil.copyfile(backup_yaml_path, project_yaml_path)
        logger.info("Restored project.yaml from backup.")
    finally:
        # Clean up the backup file
        if os.path.exists(backup_yaml_path):
            os.remove(backup_yaml_path)

def get_template_version() -> Optional[str]:
    """Get the template version from templates.json if available."""
    try:
        with open('templates.json', 'r') as file:
            templates_config = json.load(file)
            return templates_config.get('template_version')
    except (FileNotFoundError, json.JSONDecodeError):
        return None