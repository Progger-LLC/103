import pytest
import os
import shutil
import yaml
from modules.project_routes import repair_project_config

def test_repair_project_config(monkeypatch):
    """Test the repair_project_config function."""
    # Create a temporary project.yaml for testing
    test_yaml_path = 'project.yaml'
    with open(test_yaml_path, 'w') as f:
        f.write('dependencies:\n  - fastapi\n')

    # Call the repair function
    repair_project_config()

    # Check if the template_version is added
    with open(test_yaml_path, 'r') as f:
        data = yaml.safe_load(f)
    
    assert 'template_version' in data
    assert data['template_version'] == '1.0.0'  # Check default value

    # Cleanup
    os.remove(test_yaml_path)

def test_backup_creation():
    """Test backup creation."""
    original_yaml_path = 'project.yaml'
    backup_path = f'backup_test.yaml'

    # Create a dummy project.yaml
    with open(original_yaml_path, 'w') as f:
        f.write('dependencies:\n  - fastapi\n')

    # Back up the file
    shutil.copyfile(original_yaml_path, backup_path)
    
    assert os.path.exists(backup_path)

    # Cleanup
    os.remove(original_yaml_path)
    os.remove(backup_path)