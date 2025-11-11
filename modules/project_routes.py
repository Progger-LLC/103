import os
import yaml
import logging
from datetime import datetime
from typing import Dict, Any

logger = logging.getLogger(__name__)

def create_backup(file_path: str) -> None:
    """Create a timestamped backup of the specified file."""
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    backup_path = f"{file_path}.{timestamp}.bak"
    with open(file_path, 'r') as original_file:
        with open(backup_path, 'w') as backup_file:
            backup_file.write(original_file.read())
    logger.info(f"Backup created at {backup_path}")

def fix_project_yaml() -> None:
    """Fix project.yaml configuration issues."""
    project_yaml_path = 'project.yaml'
    
    # Check if the project.yaml exists
    if not os.path.exists(project_yaml_path):
        logger.warning(f"{project_yaml_path} not found. Creating a new one.")
        with open(project_yaml_path, 'w') as f:
            yaml.dump({'dependencies': [], 'template_version': '1.0.0'}, f)
        logger.info(f"Created new {project_yaml_path} with defaults.")
        return
    
    # Create a backup of the existing project.yaml
    create_backup(project_yaml_path)

    # Load existing configuration
    with open(project_yaml_path, 'r') as f:
        try:
            config = yaml.safe_load(f) or {}
        except yaml.YAMLError as e:
            logger.error(f"Error loading YAML: {e}")
            return

    # Ensure required fields are present
    required_fields = {
        'dependencies': [],
        'template_version': config.get('template_version', '1.0.0'),
    }

    for field, default_value in required_fields.items():
        if field not in config:
            config[field] = default_value
            logger.info(f"Added missing field: {field}")

    # Write the corrected configuration back to project.yaml
    with open(project_yaml_path, 'w') as f:
        yaml.dump(config, f)
    logger.info(f"Updated {project_yaml_path} with required fields.")