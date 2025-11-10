import os
import shutil
import yaml
from datetime import datetime
from typing import Optional

def repair_project_config(project_file: str, templates_file: str) -> None:
    """Repair the project.yaml configuration file.

    Args:
        project_file (str): Path to the project.yaml file.
        templates_file (str): Path to the templates.json file.

    Raises:
        Exception: If the repair process fails.
    """
    # Create a timestamped backup
    backup_file = f"{project_file}.{datetime.now().strftime('%Y%m%d%H%M%S')}.bak"
    shutil.copyfile(project_file, backup_file)

    try:
        # Load the existing project configuration
        with open(project_file, 'r') as file:
            project_config = yaml.safe_load(file)

        # Ensure template_version is present
        if 'template_version' not in project_config:
            project_config['template_version'] = infer_template_version(templates_file)

        # Validate the project_config
        validate_project_config(project_config)

        # Write the fixed configuration back to the file
        with open(project_file, 'w') as file:
            yaml.dump(project_config, file)

    except Exception as e:
        # Restore from backup if any error occurs
        shutil.copyfile(backup_file, project_file)
        raise e

def infer_template_version(templates_file: str) -> Optional[str]:
    """Infer the template version from templates.json.

    Args:
        templates_file (str): Path to the templates.json file.

    Returns:
        Optional[str]: The inferred template version or None.
    """
    if os.path.exists(templates_file):
        with open(templates_file, 'r') as file:
            templates = json.load(file)
            return templates.get('template_version', None)
    return None

def validate_project_config(config: dict) -> None:
    """Validate the project configuration structure.

    Args:
        config (dict): The project configuration dictionary.

    Raises:
        ValueError: If the validation fails.
    """
    required_fields = ['template_version', 'dependencies']
    for field in required_fields:
        if field not in config:
            raise ValueError(f"Missing required field: {field}")