import os
import pytest
import yaml
from modules.project_routes import repair_project_config

@pytest.fixture
def setup_temp_yaml(tmp_path):
    """Fixture to create a temporary project.yaml file for testing."""
    yaml_content = """
    name: Example Project
    dependencies:
      - package1: 1.0
    """
    yaml_file = tmp_path / "project.yaml"
    with open(yaml_file, 'w') as f:
        f.write(yaml_content)
    return yaml_file

def test_repair_project_config(setup_temp_yaml):
    """Tests the repair_project_config function for valid YAML."""
    yaml_file = setup_temp_yaml

    # Invoke the repair function
    repair_project_config(str(yaml_file))

    # Check that the template_version is added
    with open(yaml_file, 'r') as f:
        data = yaml.safe_load(f)
        assert 'template_version' in data
        assert data['template_version'] == '1.0.0'  # Default value

def test_backup_on_failure(setup_temp_yaml, mocker):
    """Tests that a backup is created on failure."""
    yaml_file = setup_temp_yaml
    mocker.patch('yaml.safe_load', side_effect=Exception("Forced error"))
    
    with pytest.raises(Exception):
        repair_project_config(str(yaml_file))

    # Check for backup file creation
    assert os.path.exists(f"{yaml_file}.bak")