import os
import yaml
import logging
from datetime import datetime
from typing import Dict, Any

# Initialize logger
logger = logging.getLogger(__name__)

def repair_project_config() -> None:
    """Repair the project.yaml configuration file."""
    project_yaml_path = 'project.yaml'
    backup_path = f'project_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.yaml'
    
    # Step 1: Create a backup of project.yaml
    try:
        with open(project_yaml_path, 'r') as original_file:
            with open(backup_path, 'w') as backup_file:
                backup_file.write(original_file.read())
        logger.info(f"Backup created at {backup_path}")
    except Exception as e:
        logger.error(f"Failed to create backup: {e}")
        return

    # Step 2: Load the existing project.yaml
    try:
        with open(project_yaml_path, 'r') as file:
            config = yaml.safe_load(file) or {}
    except yaml.YAMLError as e:
        logger.error(f"YAML syntax error: {e}")
        return
    
    # Step 3: Validate and set required fields
    if 'template_version' not in config:
        config['template_version'] = infer_template_version()
        logger.info("Added missing 'template_version' field.")
    
    # Step 4: Validate dependencies are properly formatted
    validate_dependencies(config.get('dependencies', {}))

    # Step 5: Write the updated config back to project.yaml
    try:
        with open(project_yaml_path, 'w') as file:
            yaml.dump(config, file)
        logger.info("project.yaml updated successfully.")
    except Exception as e:
        logger.error(f"Failed to write to project.yaml: {e}")
        # Step 6: Restore from backup if repair fails
        restore_backup(backup_path, project_yaml_path)
        return

def infer_template_version() -> str:
    """Infer template_version from templates.json if available."""
    # Logic to read templates.json (if available) and return template version
    # Placeholder for actual implementation
    return "1.0.0"  # Default version

def validate_dependencies(dependencies: Dict[str, Any]) -> None:
    """Validate that dependencies are properly formatted."""
    for dep_name, dep_version in dependencies.items():
        if not isinstance(dep_name, str) or not isinstance(dep_version, str):
            logger.error(f"Invalid dependency format: {dep_name}: {dep_version}")

def restore_backup(backup_path: str, original_path: str) -> None:
    """Restore the original project.yaml from backup."""
    try:
        with open(backup_path, 'r') as backup_file:
            with open(original_path, 'w') as original_file:
                original_file.write(backup_file.read())
        logger.info(f"Restored original configuration from {backup_path}")
    except Exception as e:
        logger.error(f"Failed to restore from backup: {e}")