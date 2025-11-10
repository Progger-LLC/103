import pytest
import os
import yaml
from unittest.mock import patch, mock_open
from modules.project_routes import repair_project_config
from src.exceptions import InvalidConfigError

@pytest.fixture
def mock_project_yaml():
    """Fixture to mock project.yaml content."""
    return {
        'dependencies': ['fastapi', 'uvicorn'],
    }

def test_repair_project_config_creates_backup(mock_project_yaml):
    """Test if backup is created before modifying project.yaml."""
    mock_yaml_content = yaml.dump(mock_project_yaml)
    with patch("builtins.open", mock_open(read_data=mock_yaml_content)):
        with patch("shutil.copyfile") as mock_copyfile:
            repair_project_config()
            mock_copyfile.assert_called_once()

def test_repair_project_config_adds_template_version(mock_project_yaml):
    """Test if missing template_version is added to project.yaml."""
    mock_yaml_content = yaml.dump(mock_project_yaml)
    with patch("builtins.open", mock_open(read_data=mock_yaml_content)):
        with patch("yaml.safe_dump") as mock_safe_dump:
            repair_project_config()
            assert 'template_version' in mock_project_yaml

def test_repair_project_config_invalid_yaml():
    """Test if InvalidConfigError is raised when YAML is invalid."""
    with patch("builtins.open", side_effect=Exception("File not found")):
        with pytest.raises(InvalidConfigError):
            repair_project_config()