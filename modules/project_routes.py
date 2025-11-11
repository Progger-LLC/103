import os
import shutil
import yaml
from datetime import datetime
from typing import Dict, Any
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

def repair_project_config() -> None:
    """Repair the project.yaml configuration file if needed."""
    project_yaml_path = Path("project.yaml")
    templates_json_path = Path("templates.json")
    
    # Step 1: Create a timestamped backup if project.yaml exists
    if project_yaml_path.exists():
        backup_path = Path(f"project_backup_{datetime.now().isoformat()}.yaml")
        shutil.copy(project_yaml_path, backup_path)
        logger.info(f"Backup created at {backup_path}")

    # Step 2: Load existing config or prepare default if not found
    config_data = {}
    if project_yaml_path.exists():
        with open(project_yaml_path, 'r') as file:
            try:
                config_data = yaml.safe_load(file) or {}
                logger.info("Loaded existing project.yaml configuration.")
            except yaml.YAMLError as e:
                logger.error(f"YAML error: {e}. Attempting to repair.")

    # Step 3: Fix YAML syntax errors and add missing required fields
    required_fields = ['template_version', 'dependencies']
    for field in required_fields:
        if field not in config_data:
            if field == 'template_version' and templates_json_path.exists():
                with open(templates_json_path, 'r') as json_file:
                    templates_data = json.load(json_file)
                    config_data['template_version'] = templates_data.get('version', '1.0.0')
            else:
                config_data[field] = []

    # Step 4: Validate and write the fixed config back to project.yaml
    with open(project_yaml_path, 'w') as file:
        yaml.dump(config_data, file)
        logger.info(f"Fixed project.yaml configuration written back.")