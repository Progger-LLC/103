import os
import yaml
import logging
from datetime import datetime
from typing import Optional

logger = logging.getLogger(__name__)

def repair_project_config(yaml_file: str) -> bool:
    """Repairs the project.yaml configuration file.

    This function creates a backup of the original YAML file,
    fixes any syntax errors, adds missing required fields,
    and infers the template_version from templates.json if available.

    Args:
        yaml_file (str): Path to the project.yaml file.

    Returns:
        bool: True if repair was successful, False otherwise.
    """

    # Create a backup of the YAML file
    backup_file = f"{yaml_file}.{datetime.now().strftime('%Y%m%d%H%M%S')}.bak"
    try:
        with open(yaml_file, 'r') as original_file:
            with open(backup_file, 'w') as backup:
                backup.write(original_file.read())
        logger.info(f"Backup created: {backup_file}")
    except Exception as e:
        logger.error(f"Failed to create backup: {str(e)}")
        return False

    # Load the existing YAML configuration
    try:
        with open(yaml_file, 'r') as file:
            config = yaml.safe_load(file)
    except yaml.YAMLError as e:
        logger.error(f"YAML error: {str(e)}")
        return False

    # Ensure all required fields are present
    required_fields = {
        'template_version': '1.0.0',  # Default value
        'dependencies': {},
    }

    for key, default in required_fields.items():
        if key not in config:
            config[key] = default
            logger.warning(f"Missing field '{key}' added with default value '{default}'")

    # Check for dependencies formatting (example check)
    if 'dependencies' in config and not isinstance(config['dependencies'], dict):
        logger.error("Dependencies should be formatted as a dictionary.")
        return False

    # Infer template_version from templates.json if available
    templates_file = 'templates.json'
    if os.path.exists(templates_file):
        with open(templates_file, 'r') as file:
            templates = json.load(file)
            if 'template_version' in templates:
                config['template_version'] = templates['template_version']
                logger.info(f"Template version inferred: {config['template_version']}")

    # Save the repaired configuration
    try:
        with open(yaml_file, 'w') as file:
            yaml.dump(config, file)
        logger.info("Project configuration repaired successfully.")
    except Exception as e:
        logger.error(f"Failed to write updated configuration: {str(e)}")
        # Restore from backup if repair fails
        os.replace(backup_file, yaml_file)
        logger.info("Restored from backup.")
        return False

    return True