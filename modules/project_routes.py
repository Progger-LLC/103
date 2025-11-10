import os
import shutil
import yaml
from datetime import datetime
from typing import Any, Dict, Optional

def repair_project_config(file_path: str) -> None:
    """Repairs the project.yaml configuration file.

    This function performs the following actions:
    1. Creates a backup of the original project.yaml
    2. Validates and fixes YAML syntax
    3. Adds missing required fields with sensible defaults
    4. Infers template_version from templates.json if available
    5. Restores from backup if repair fails.

    Args:
        file_path (str): Path to the project.yaml file.

    Raises:
        Exception: If the repair process fails.
    """
    # Step 1: Create a backup of the original project.yaml
    backup_path = f"{file_path}.{datetime.now().strftime('%Y%m%d%H%M%S')}.bak"
    shutil.copy(file_path, backup_path)

    try:
        # Step 2: Load the existing project.yaml
        with open(file_path, 'r') as f:
            data = yaml.safe_load(f) or {}

        # Step 3: Fix YAML syntax errors and add missing fields
        if 'template_version' not in data:
            data['template_version'] = '1.0.0'  # Default version

        # Add any default fields that are necessary
        # (Assuming more fields may be required, e.g., dependencies)
        if 'dependencies' not in data:
            data['dependencies'] = {}

        # Step 4: Infer template_version from templates.json if available
        template_version = infer_template_version()
        if template_version:
            data['template_version'] = template_version

        # Step 5: Write changes back to project.yaml
        with open(file_path, 'w') as f:
            yaml.safe_dump(data, f)

    except Exception as e:
        # Restore from backup if repair fails
        shutil.copy(backup_path, file_path)
        raise Exception(f"Repair failed, restored from backup: {str(e)}")

def infer_template_version() -> Optional[str]:
    """Infers template version from templates.json if available.

    Returns:
        Optional[str]: The inferred template version or None if not found.
    """
    try:
        with open('templates.json', 'r') as f:
            templates = json.load(f)
            return templates.get('template_version', None)
    except FileNotFoundError:
        return None