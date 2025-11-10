import pytest
import os
import yaml
from modules.project_routes import repair_project_config

def test_repair_project_config_valid_yaml():
    """Test that the repair_project_config function works correctly."""
    # Prepare a test project.yaml
    test_yaml_content = """
    entry_point: main.py
    dependencies:
      - fastapi
    """
    
    with open('project.yaml', 'w') as file:
        file.write(test_yaml_content)
    
    # Call the repair function
    repair_project_config()

    # Check if template_version is added
    with open('project.yaml', 'r') as file:
        config = yaml.safe_load(file)
        assert 'template_version' in config
        assert config['template_version'] == '1.0.0'

def test_repair_project_config_backup_created():
    """Test that a backup file is created before changes are made."""
    test_yaml_content = """
    entry_point: main.py
    dependencies:
      - fastapi
    """
    
    with open('project.yaml', 'w') as file:
        file.write(test_yaml_content)

    repair_project_config()

    # Check if backup file exists
    assert os.path.exists('project_backup_*.yaml')  # Check for backup file pattern