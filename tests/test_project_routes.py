import pytest
import os
from modules.project_routes import repair_project_config

def test_repair_project_config_success(mocker):
    mock_open = mocker.patch("builtins.open", mocker.mock_open(read_data="valid_yaml: true"))
    mocker.patch("os.rename")
    mocker.patch("os.remove")
    
    result = repair_project_config("project.yaml")
    
    assert result is True
    mock_open.assert_called()
    assert os.path.exists("project.yaml")

def test_repair_project_config_backup_creation(mocker):
    mock_open = mocker.patch("builtins.open", mocker.mock_open(read_data="valid_yaml: true"))
    mocker.patch("os.rename")
    mocker.patch("os.remove")
    
    result = repair_project_config("project.yaml")
    
    assert result is True
    assert os.path.exists("project.yaml.bak")

def test_repair_project_config_failure(mocker):
    mock_open = mocker.patch("builtins.open", side_effect=IOError("File not found"))
    
    result = repair_project_config("project.yaml")
    
    assert result is False