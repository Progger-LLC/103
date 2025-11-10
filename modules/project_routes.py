import os
import shutil
import yaml
import datetime
from typing import Dict, Any

def repair_project_config(file_path: str, templates_path: str) -> None:
    """Repair the project.yaml configuration file.

    This function will create a backup, fix any issues, and ensure that all required fields are present.

    Args:
        file_path (str): Path to the project.yaml file.
        templates_path (str): Path to the templates.json file.
    """
    # Step 1: Create a timestamped backup
    backup_path = f"{file_path}.{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.bak"
    shutil.copy(file_path, backup_path)

    try:
        # Step 2: Load the existing configuration
        with open(file_path, 'r') as file:
            config = yaml.safe_load(file) or {}

        # Step 3: Fix YAML errors and add missing fields
        if 'template_version' not in config:
            config['template_version'] = infer_template_version(templates_path)

        # Step 4: Validate and reformat dependencies if needed
        validate_dependencies(config)

        # Step 5: Write the fixed configuration back to project.yaml
        with open(file_path, 'w') as file:
            yaml.dump(config, file)

    except Exception as e:
        # Restore from backup if repair fails
        shutil.copy(backup_path, file_path)
        raise

def infer_template_version(templates_path: str) -> str:
    """Infer the template version from the templates.json file if available.

    Args:
        templates_path (str): Path to the templates.json file.

    Returns:
        str: The inferred template version or a default value.
    """
    try:
        with open(templates_path, 'r') as file:
            templates = json.load(file)
            return templates.get('version', '1.0.0')  # Default version if not found
    except FileNotFoundError:
        return '1.0.0'  # Default version if templates.json does not exist

def validate_dependencies(config: Dict[str, Any]) -> None:
    """Validate the dependencies section of the configuration.

    Args:
        config (Dict[str, Any]): The project configuration.
    
    Raises:
        ValueError: If dependencies are improperly formatted.
    """
    if 'dependencies' in config:
        if not isinstance(config['dependencies'], list):
            raise ValueError("Dependencies must be a list.")