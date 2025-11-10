import os
import shutil
import yaml
from datetime import datetime
from typing import Dict, Any

def repair_project_config() -> None:
    """Repair project.yaml configuration issues."""
    project_yaml_path = 'project.yaml'
    backup_path = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{project_yaml_path}"
    
    # Step 1: Create a timestamped backup
    shutil.copy(project_yaml_path, backup_path)
    
    try:
        # Step 2: Load existing project.yaml
        with open(project_yaml_path, 'r') as f:
            config = yaml.safe_load(f)

        # Step 3: Validate and fix YAML syntax
        if not isinstance(config, dict):
            raise ValueError("Invalid YAML format: expected a dictionary.")

        # Step 4: Ensure all required fields are present
        if 'template_version' not in config:
            config['template_version'] = '1.0.0'  # Default version
        if 'dependencies' not in config:
            config['dependencies'] = {}

        # Step 5: Load template version from templates.json if available
        if os.path.exists('templates.json'):
            with open('templates.json', 'r') as f:
                templates = json.load(f)
                if 'template_version' in templates:
                    config['template_version'] = templates['template_version']

        # Step 6: Save fixed project.yaml
        with open(project_yaml_path, 'w') as f:
            yaml.safe_dump(config, f)

    except Exception as e:
        # Restore from backup if repair fails
        shutil.copy(backup_path, project_yaml_path)
        raise e