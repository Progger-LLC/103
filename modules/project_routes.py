import os
import shutil
import yaml
import json
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

def repair_project_config() -> None:
    """Repair the project.yaml configuration issues."""
    
    project_yaml_path = "project.yaml"
    backup_path = f"backup/project_backup_{int(time.time())}.yaml"
    templates_json_path = "templates.json"
    
    # Step 1: Create a timestamped backup of project.yaml
    if not os.path.exists("backup"):
        os.makedirs("backup")
    shutil.copy(project_yaml_path, backup_path)
    logger.info(f"Backup created at {backup_path}")
    
    try:
        # Step 2: Load existing project.yaml
        with open(project_yaml_path, 'r') as file:
            project_config = yaml.safe_load(file) or {}
        
        # Step 3: Fix missing template_version and other required fields
        if 'template_version' not in project_config:
            logger.warning("template_version field is missing, adding default.")
            project_config['template_version'] = "1.0.0"  # Sensible default
        
        # Step 4: Read templates.json to infer template_version if available
        if os.path.exists(templates_json_path):
            with open(templates_json_path, 'r') as templates_file:
                templates = json.load(templates_file)
                project_config['template_version'] = templates.get('version', project_config['template_version'])

        # Step 5: Save the updated project.yaml
        with open(project_yaml_path, 'w') as file:
            yaml.safe_dump(project_config, file)
        logger.info("project.yaml has been updated successfully.")
    
    except Exception as e:
        logger.error(f"Error during repair process: {e}. Restoring from backup.")
        shutil.copy(backup_path, project_yaml_path)  # Restore from backup
        logger.info("Restored project.yaml from backup.")