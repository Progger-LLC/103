import os
import yaml
import logging
from datetime import datetime
from typing import Optional

logger = logging.getLogger(__name__)

def repair_project_config(config_path: str, templates_path: Optional[str] = None) -> None:
    """Repair the project configuration in project.yaml."""
    # Step 1: Create a timestamped backup of project.yaml
    backup_path = f"{config_path}.{datetime.now().strftime('%Y%m%d%H%M%S')}.bak"
    os.rename(config_path, backup_path)
    
    try:
        # Step 2: Load the existing configuration
        with open(backup_path, 'r') as file:
            config = yaml.safe_load(file)

        # Step 3: Check and fix configuration issues
        if 'template_version' not in config:
            logger.info("Adding missing 'template_version' field.")
            config['template_version'] = "1.0.0"  # Default value

        # Step 4: Validate YAML format (this step assumes the structure is correct)
        yaml.dump(config, open(config_path, 'w'))

    except Exception as e:
        logger.error("Repair failed, restoring from backup.")
        os.rename(backup_path, config_path)  # Restore from backup
        raise e  # Raise the original exception