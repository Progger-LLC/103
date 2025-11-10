import pytest
import os
import shutil
from modules.project_routes import repair_project_config
from src.exceptions import ConfigurationError
import yaml

def create_test_yaml(content: dict, filename='test_project.yaml'):
    """Helper function to create a test YAML file."""
    with open(filename, 'w') as file:
        yaml.dump(content, file)

def remove_test_yaml(filename='test_project.yaml'):
    """Helper function to remove the test YAML file."""
    if os.path.exists(filename):
        os.remove(filename)

def test_repair_project_config_missing_template_version():
    """Test the repair_project_config function when template_version is missing."""
    create_test_yaml({'dependencies': ['fastapi==0.104.1']}, 'test_project.yaml')
    
    try:
        repair_project_config()
        with open('test_project.yaml', 'r') as file:
            config = yaml.safe_load(file)
        assert config['template_version'] == "1.0.0"
    finally:
        remove_test_yaml('test_project.yaml')

def test_repair_project_config_invalid_yaml():
    """Test the repair_project_config function with invalid YAML."""
    create_test_yaml("invalid_yaml", 'test_project.yaml')
    
    with pytest.raises(ConfigurationError):
        repair_project_config()
    
    remove_test_yaml('test_project.yaml')

def test_repair_project_config_backup_creation():
    """Test that a backup is created before changes."""
    create_test_yaml({'dependencies': ['fastapi==0.104.1']}, 'test_project.yaml')
    
    assert not os.path.exists('backup/')  # Ensure backup does not exist yet
    repair_project_config()
    assert os.path.exists('backup/')  # Backup should now exist
    remove_test_yaml('test_project.yaml')
    shutil.rmtree('backup/')  # Clean up backup directory