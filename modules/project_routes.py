import os
import shutil
import yaml
from datetime import datetime
from typing import Dict, Any

def repair_project_config() -> None:
    """Repair project.yaml configuration issues."""
    project_yaml_path = "project.yaml"
    backup_path = f"{project_yaml_path}.{datetime.now().strftime('%Y%m%d%H%M%S')}.bak"

    # Step 1: Create a backup
    shutil.copy(project_yaml_path, backup_path)

    try:
        # Step 2: Load existing YAML
        with open(project_yaml_path, 'r') as file:
            config = yaml.safe_load(file)

        # Step 3: Validate and fix configuration
        if 'template_version' not in config:
            config['template_version'] = "1.0"  # Default version if not found

        # Additional checks for required fields can be added here
        # For example:
        required_fields = ['entry_point', 'dependencies']
        for field in required_fields:
            if field not in config:
                config[field] = [] if field == 'dependencies' else ""

        # Step 4: Write changes back to YAML
        with open(project_yaml_path, 'w') as file:
            yaml.dump(config, file)

    except Exception as e:
        # Restore from backup if any error occurs
        shutil.copy(backup_path, project_yaml_path)
        raise

    finally:
        # Clean up backup file if everything went well
        if os.path.exists(backup_path):
            os.remove(backup_path)