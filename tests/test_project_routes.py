import pytest
import os
from modules.project_routes import repair_project_config

def test_repair_project_config_creates_backup(mocker):
    """Test that a backup is created before repairing the project.yaml."""
    mock_backup = mocker.patch('shutil.copy')
    mock_load = mocker.patch('yaml.safe_load', return_value={})
    mock_dump = mocker.patch('yaml.dump')
    
    repair_project_config()
    
    assert mock_backup.called
    assert mock_load.called
    assert mock_dump.called

def test_repair_project_config_adds_missing_fields(mocker):
    """Test that missing fields are added to project.yaml."""
    mock_open = mocker.patch('builtins.open', mocker.mock_open(read_data=''))
    mock_dump = mocker.patch('yaml.dump')
    
    repair_project_config()
    
    mock_open.assert_called_with('project.yaml', 'r')
    mock_dump.assert_called_with({'template_version': '1.0', 'dependencies': []}, mocker.ANY)

def test_repair_project_config_invalid_yaml(mocker):
    """Test that invalid YAML raises an error and restores from backup."""
    mock_open = mocker.patch('builtins.open', side_effect=Exception("Error reading YAML"))
    mock_backup = mocker.patch('shutil.copy')
    
    with pytest.raises(Exception):
        repair_project_config()
        
    assert mock_backup.called