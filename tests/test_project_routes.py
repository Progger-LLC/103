import pytest
import os
import modules.project_routes as project_routes
import yaml

def test_create_backup():
    """Test the backup creation functionality."""
    original_file = 'project.yaml'
    backup_file = project_routes.create_backup(original_file)
    
    assert os.path.exists(backup_file)
    # Cleanup
    os.remove(backup_file)

def test_repair_project_config(mocker):
    """Test the repair functionality."""
    mocker.patch('builtins.open', new_callable=mocker.mock_open, read_data='dependencies: {}')
    
    project_routes.repair_project_config()
    
    with open('project.yaml', 'r') as file:
        config = yaml.safe_load(file)
    
    assert 'template_version' in config
    assert config['template_version'] == "1.0.0"
    assert isinstance(config['dependencies'], dict)