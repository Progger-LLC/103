import os
import shutil
import yaml
import json
from datetime import datetime
from modules.project_routes import repair_project_config
from typing import Dict, Any

def backup_project_yaml(file_path: str) -> str:
    """Create a timestamped backup of the project.yaml file."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file_path = f"{file_path}.{timestamp}.bak"
    shutil.copy(file_path, backup_file_path)
    return backup_file_path

def infer_template_version(templates_file: str) -> str:
    """Infer template_version from templates.json if available."""
    if os.path.exists(templates_file):
        with open(templates_file, 'r') as f:
            templates = json.load(f)
            return templates.get("template_version", "1.0.0")  # Default version if not found
    return "1.0.0"  # Default version

def repair_project_yaml(file_path: str, templates_file: str) -> None:
    """Repair project.yaml by fixing issues and adding missing fields."""
    backup_path = backup_project_yaml(file_path)
    
    try:
        with open(file_path, 'r') as f:
            config = yaml.safe_load(f) or {}

        # Fixing YAML syntax and adding required fields
        if 'template_version' not in config:
            config['template_version'] = infer_template_version(templates_file)

        # Ensure other required fields are present (add defaults if necessary)
        required_fields = ["entry_point", "dependencies"]
        for field in required_fields:
            if field not in config:
                config[field] = [] if field == "dependencies" else ""

        # Write back the fixed configuration
        with open(file_path, 'w') as f:
            yaml.dump(config, f)

    except Exception as e:
        # Restore from backup if repair fails
        shutil.copy(backup_path, file_path)
        raise e  # Raise the original exception

    # If everything is fine, remove backup
    os.remove(backup_path)