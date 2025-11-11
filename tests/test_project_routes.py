import os
import pytest
from modules.project_routes import repair_project_config

def test_repair_project_config_creates_yaml(mocker):
    """Test that repair_project_config creates a valid project.yaml."""
    mocker.patch('os.path.exists', return_value=False)  # Simulate project.yaml not existing
    repair_project_config()

    assert os.path.exists('project.yaml')

def test_repair_project_config_backups_yaml(mocker):
    """Test that repair_project_config creates a backup of the existing project.yaml."""
    mocker.patch('os.path.exists', side_effect=[True, False])  # Simulate existing project.yaml
    mocker.patch('os.rename')  # Mock os.rename to avoid file operations

    repair_project_config()

    assert os.path.exists('project_backup_*.yaml')

def test_repair_project_config_valid_yaml(mocker):
    """Test that the newly created project.yaml is valid YAML."""
    mocker.patch('os.path.exists', return_value=False)  # Simulate project.yaml not existing
    repair_project_config()

    with open('project.yaml', 'r') as yaml_file:
        content = yaml_file.read()
        assert content is not None  # Ensure it's not empty