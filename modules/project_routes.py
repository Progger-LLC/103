import os
import shutil
import yaml
from datetime import datetime
from typing import Optional

def repair_project_config(project_file: str, templates_file: Optional[str] = None) -> None:
    """Repairs the project.yaml configuration by adding missing fields and fixing errors.

    Args:
        project_file (str): Path to the project.yaml file.
        templates_file (Optional[str]): Path to the templates.json file if available.

    Raises:
        Exception: If the repair process fails.
    """
    
    # Step 1: Create a timestamped backup of project.yaml
    backup_file = f"{project_file}.{datetime.now().strftime('%Y%m%d%H%M%S')}.bak"
    shutil.copyfile(project_file, backup_file)

    try:
        # Step 2: Load and fix the YAML file
        with open(project_file, 'r') as file:
            config = yaml.safe_load(file) or {}
        
        # Step 3: Add missing required fields with sensible defaults
        if 'template_version' not in config:
            if templates_file:
                # Infer template_version from templates.json if available
                with open(templates_file, 'r') as json_file:
                    templates = json.load(json_file)
                    config['template_version'] = templates.get('default_version', '1.0.0')
            else:
                config['template_version'] = '1.0.0'
        
        # Step 4: Validate YAML structure and dependencies formatting
        # Assuming dependencies is a list; add additional validation as needed
        if 'dependencies' not in config:
            config['dependencies'] = []
        
        # Step 5: Write the fixed config back to project.yaml
        with open(project_file, 'w') as file:
            yaml.dump(config, file)

    except Exception as e:
        # Restore from backup if repair fails
        shutil.copyfile(backup_file, project_file)
        raise Exception("Repair of project.yaml failed, restored from backup.") from e