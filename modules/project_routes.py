import os
import yaml
import shutil
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

def repair_project_config() -> None:
    """Repair the project.yaml configuration file."""
    project_yaml_path = "project.yaml"
    backup_path = f"{project_yaml_path}.bak.{datetime.now().strftime('%Y%m%d%H%M%S')}"

    # Step 1: Backup project.yaml
    if os.path.exists(project_yaml_path):
        shutil.copy2(project_yaml_path, backup_path)
        logger.info(f"Backup created at {backup_path}")
    else:
        logger.warning("project.yaml not found, creating a new one.")

    # Step 2: Create or read project.yaml
    if not os.path.exists(project_yaml_path):
        # Initialize with default values
        project_config = {
            "entry_point": "main.py",
            "dependencies": [],
            "template_version": "1.0.0"  # Default version if not inferred
        }
    else:
        with open(project_yaml_path, 'r') as file:
            try:
                project_config = yaml.safe_load(file)
            except yaml.YAMLError as e:
                logger.error(f"YAML error: {e}")
                return

    # Step 3: Fix configuration issues (add defaults, check dependencies)
    project_config.setdefault("entry_point", "main.py")
    project_config.setdefault("dependencies", [])
    project_config.setdefault("template_version", "1.0.0")

    # Step 4: Save the corrected configuration
    try:
        with open(project_yaml_path, 'w') as file:
            yaml.dump(project_config, file)
        logger.info("project.yaml has been repaired and saved.")
    except Exception as e:
        logger.error(f"Failed to save project.yaml: {e}")
        # Restore from backup
        if os.path.exists(backup_path):
            shutil.copy2(backup_path, project_yaml_path)
            logger.info("Restored project.yaml from backup.")